#!/usr/bin/env python3
"""Tests of run-track-s.py with a stubbed transport; no network, no API key.

Run from the repository root: python3 -I trackS/test_run_track_s.py
"""

import argparse
import email.message
import importlib.util
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
import urllib.error

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE / "run-track-s.py"
spec = importlib.util.spec_from_file_location("run_track_s", SCRIPT)
ts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ts)


class Reply:
    """A urlopen response carrying a JSON payload and headers."""

    def __init__(self, payload, headers):
        self.payload, self.headers = payload, headers

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def headers(**values):
    message = email.message.Message()
    for key, value in values.items():
        message[key.replace("_", "-")] = value
    return message


def http_error(code, body, hdrs):
    return urllib.error.HTTPError("https://example.invalid", code, "error", hdrs, io.BytesIO(body))


def answer(text, finish):
    return {"choices": [{"message": {"content": text}, "finish_reason": finish}], "id": "r", "model": "m"}


class ClientTest(unittest.TestCase):
    def setUp(self):
        os.environ["MISTRAL_API_KEY"] = "test-key"
        self.out = pathlib.Path(tempfile.mkdtemp()) / "run"
        self.out.mkdir()
        self.recorder = ts.Recorder(self.out)
        self.client = ts.Client("persona", "mistral", "ministral-8b-2512", 60_000, 100, self.recorder)
        self.replies = []
        self._urlopen, self._sleep = ts.urllib.request.urlopen, ts.time.sleep
        ts.urllib.request.urlopen = self._next
        ts.time.sleep = lambda seconds: None

    def tearDown(self):
        ts.urllib.request.urlopen, ts.time.sleep = self._urlopen, self._sleep
        self.recorder.calls.close()

    def _next(self, request, timeout=0):
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply

    def calls(self):
        self.recorder.calls.flush()
        return [json.loads(line) for line in (self.out / "calls.jsonl").read_text().splitlines()]

    def test_429_is_logged_with_body_and_headers_then_retried(self):
        limits = headers(x_ratelimit_remaining_tokens_month="999")
        self.replies = [http_error(429, b'{"message": "rate limit"}', limits), Reply(answer("hello", "stop"), limits)]
        self.assertEqual(self.client.call("s", "system", [("user", "q")]), "hello")
        first, second = self.calls()
        self.assertEqual(first["http"], 429)
        self.assertIn("rate limit", first["body"])
        self.assertEqual(first["rateLimitHeaders"], {"x-ratelimit-remaining-tokens-month": "999"})
        self.assertEqual(second["finish"], "stop")
        self.assertTrue((self.out / "requests" / "0001.json").exists())
        self.assertTrue((self.out / "responses" / "0001.json").exists())

    def test_reasoning_chunks_yield_only_the_text(self):
        reply = answer([{"type": "thinking", "thinking": [{"type": "text", "text": "hidden"}]},
                        {"type": "text", "text": "the answer"}], "stop")
        self.replies = [Reply(reply, headers())]
        self.assertEqual(self.client.call("s", "system", [("user", "q")]), "the answer")

    def test_sampling_is_sent_only_when_set(self):
        sent = []
        self.replies = [Reply(answer("a", "stop"), headers()), Reply(answer("b", "stop"), headers())]
        next_reply = self._next
        ts.urllib.request.urlopen = lambda request, timeout=0: (sent.append(json.loads(request.data)), next_reply(request))[1]
        self.client.call("s", "system", [("user", "q")])
        fixed = ts.Client("persona", "mistral", "m", 60_000, 100, self.recorder, temperature=0.0, seed=7)
        fixed.call("s", "system", [("user", "q")])
        self.assertNotIn("temperature", sent[0])
        self.assertNotIn("random_seed", sent[0])
        self.assertEqual((sent[1]["temperature"], sent[1]["random_seed"]), (0.0, 7))

    def test_json_reply_asks_for_a_json_object(self):
        sent = []
        next_reply = self._next
        ts.urllib.request.urlopen = lambda request, timeout=0: (sent.append(json.loads(request.data)), next_reply(request))[1]
        self.replies = [Reply(answer('{"verdicts": []}', "stop"), headers())]
        self.client.call("s", "system", [("user", "q")], json_reply=True)
        self.assertEqual(sent[0]["response_format"], {"type": "json_object"})

    def check_reply(self, *items):
        return Reply(answer(json.dumps({"sentences": [{"verdict": v, "source": src} for v, src in items]}), "stop"), headers())

    def test_check_keeps_only_kept_sentences_whose_source_holds(self):
        notes = "Each company has its own charging pads at its own sites."
        self.replies = [self.check_reply(("KEEP", "its own charging pads at"), ("DROP", None),
                                         ("KEEP", "FEELING"), ("KEEP", "pads are lent to anyone"))]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "technician", notes, "s", "q",
                          "We have our own pads. The platform owns them.\nI worry about that. Pads are lent to anyone.")
        self.assertEqual(result["answer"], "We have our own pads. I worry about that.")
        self.assertEqual([i["dropped"] for i in result["check"]],
                         [None, "check", None, "the source is not in the notes"])

    def test_source_must_be_long_enough_and_dont_know_must_say_so(self):
        notes = "Pads are never lent to another company."
        self.assertIsNone(ts.source_holds("x", "Pads are NEVER lent, to another", notes))
        self.assertEqual(ts.source_holds("x", "never lent", notes), "no source of at least 4 words")
        self.assertEqual(ts.source_holds("x", None, notes), "no source of at least 4 words")
        self.assertIsNone(ts.source_holds("I don\u2019t know.", "DONT_KNOW", notes))
        self.assertIsNotNone(ts.source_holds("The platform handles it.", "DONT_KNOW", notes))

    def test_check_asks_once_more_after_a_reply_of_the_wrong_shape(self):
        self.replies = [Reply(answer("KEEP", "stop"), headers()),
                        Reply(answer('{"sentences": [{"verdict": "KEEP", "source": "DONT_KNOW"}]}', "stop"), headers())]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "I don't know.")
        self.assertEqual(result["answer"], "I don't know.")
        self.assertEqual([c["session"] for c in self.calls()], ["s/check", "s/check-again"])

    def test_check_accepts_the_entries_without_the_object_around_them(self):
        self.replies = [Reply(answer('[{"verdict": "KEEP", "source": "DONT_KNOW"}, {"verdict": "DROP", "source": null}]',
                                     "stop"), headers())]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "I don't know. It keeps versions.")
        self.assertEqual(result["answer"], "I don't know.")

    def test_check_that_drops_everything_leaves_i_do_not_know(self):
        self.replies = [self.check_reply(("DROP", None))]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "It keeps versions.")
        self.assertEqual(result["answer"], ts.NOTHING_LEFT)

    def test_check_reply_of_the_wrong_shape_fails_the_run(self):
        bad = ('{"sentences": [{"verdict": "KEEP", "source": "a b c d"}]}',
               '{"sentences": [{"verdict": "MAYBE"}, {"verdict": "KEEP"}]}',
               '{"verdicts": ["KEEP", "KEEP"]}', "KEEP KEEP", '[1, 2]',
               '[{"sentences": [{"verdict": "DROP", "source": null}, {"verdict": "DROP", "source": null}]}]')
        for reply in bad:
            self.replies = [Reply(answer(reply, "stop"), headers()), Reply(answer(reply, "stop"), headers())]
            with self.assertRaises(ts.RunFailed, msg=reply):
                ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "One. Two.")

    def test_grade_reply_is_parsed_or_refused(self):
        self.assertEqual(ts.parse_grade('{"verdict": "pass", "contradicts": false, "reason": "r"}'),
                         {"verdict": "PASS", "contradicts": False, "reason": "r"})
        for reply in ('{"verdict": "PASS"}', '{"verdict": "OK", "contradicts": false}',
                      '{"verdict": "FAIL", "contradicts": "no"}', "PASS", "[]"):
            self.assertIsNone(ts.parse_grade(reply), reply)

    def test_summary_passes_only_at_the_threshold_without_contradiction(self):
        grades = [{"session": f"s{i}", "kind": "fact", "verdict": "PASS", "contradicts": False} for i in range(72)]
        self.assertTrue(ts.summarize(grades)["passes"])
        for g in grades[:8]:
            g["verdict"] = "FAIL"
        self.assertFalse(ts.summarize(grades)["passes"])
        self.assertEqual(ts.summarize(grades)["passing"], 64)
        grades[0].update(verdict="FAIL", contradicts=True)
        for g in grades[1:8]:
            g["verdict"] = "PASS"
        self.assertEqual(ts.summarize(grades)["contradictingFact"], ["s0"])
        self.assertFalse(ts.summarize(grades)["passes"])

    def test_non_natural_finish_fails_the_run(self):
        self.replies = [Reply(answer("cut", "length"), headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.call("s", "system", [("user", "q")])

    def test_client_error_is_not_retried(self):
        self.replies = [http_error(400, b'{"message": "invalid model"}', headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.call("s", "system", [("user", "q")])
        self.assertEqual(len(self.calls()), 1)

    def test_body_that_is_not_json_is_retried(self):
        class NotJson(Reply):
            def read(self):
                return b"<html>gateway</html>"
        self.replies = [NotJson(None, headers()), Reply(answer("hello", "stop"), headers())]
        self.assertEqual(self.client.call("s", "system", [("user", "q")]), "hello")
        self.assertIn("invalid JSON", self.calls()[0]["error"])

    def test_body_that_is_not_utf8_is_retried(self):
        class NotUtf8(Reply):
            def read(self):
                return b"\xff\xfe\xfa"
        self.replies = [NotUtf8(None, headers()), Reply(answer("hello", "stop"), headers())]
        self.assertEqual(self.client.call("s", "system", [("user", "q")]), "hello")
        self.assertIn("invalid JSON", self.calls()[0]["error"])

    def test_model_check_rejects_another_model(self):
        self.replies = [Reply({"id": "some-other-model"}, headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.describe()

    def test_model_check_body_that_is_not_json_is_a_run_failure(self):
        class NotJson(Reply):
            def read(self):
                return b"<html>gateway</html>"
        self.replies = [NotJson(None, headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.describe()

    def test_model_check_body_that_is_not_an_object_is_a_run_failure(self):
        self.replies = [Reply(["ministral-8b-2512"], headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.describe()

    def test_model_check_without_a_string_name_is_a_run_failure(self):
        for description in ({"name": 5}, {"name": None}, {}):
            self.replies = [Reply(description, headers())]
            with self.assertRaises(ts.RunFailed, msg=description):
                self.client.describe()

    def test_model_check_failure_is_a_run_failure(self):
        self.replies = [http_error(404, b'{"message": "not found"}', headers())]
        with self.assertRaises(ts.RunFailed):
            self.client.describe()


class AnthropicClientTest(unittest.TestCase):
    def setUp(self):
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        self.out = pathlib.Path(tempfile.mkdtemp()) / "run"
        self.out.mkdir()
        self.recorder = ts.Recorder(self.out)
        self.sent = []
        self._urlopen, self._sleep = ts.urllib.request.urlopen, ts.time.sleep
        ts.time.sleep = lambda seconds: None

    def tearDown(self):
        ts.urllib.request.urlopen, ts.time.sleep = self._urlopen, self._sleep
        self.recorder.calls.close()

    def reply_with(self, payload):
        def urlopen(request, timeout=0):
            self.sent.append((request, json.loads(request.data)))
            return Reply(payload, headers(anthropic_ratelimit_requests_remaining="9"))
        ts.urllib.request.urlopen = urlopen

    def test_body_carries_effort_and_schema_and_no_sampling(self):
        self.reply_with({"content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": '{"ok": 1}'}],
                         "stop_reason": "end_turn", "id": "msg", "model": "claude-opus-5-5", "usage": {}})
        judge = ts.Client("judge", "anthropic", "claude-opus-5-5", 60_000, 100, self.recorder, effort="high")
        self.assertEqual(judge.call("s", "system", [("user", "q")], json_reply=True, schema={"type": "object"}), '{"ok": 1}')
        request, body = self.sent[0]
        self.assertEqual(request.get_header("Anthropic-version"), ts.ANTHROPIC_VERSION)
        self.assertEqual(body["system"], "system")
        self.assertEqual(body["output_config"], {"effort": "high", "format": {"type": "json_schema", "schema": {"type": "object"}}})
        self.assertNotIn("temperature", body)
        self.assertTrue(request.full_url.endswith("/messages"))

    def test_refusal_is_not_a_natural_stop(self):
        self.reply_with({"content": [], "stop_reason": "refusal", "id": "msg", "model": "m"})
        judge = ts.Client("judge", "anthropic", "m", 60_000, 100, self.recorder)
        with self.assertRaises(ts.RunFailed):
            judge.call("s", "system", [("user", "q")])

    def test_sampling_and_effort_are_refused_where_they_do_not_apply(self):
        os.environ["GEMINI_API_KEY"] = "test-key"
        for kwargs in ({"temperature": 0.0}, {"seed": 1}):
            with self.assertRaises(ts.RunFailed):
                ts.Client("judge", "anthropic", "m", 60, 100, self.recorder, **kwargs)
        with self.assertRaises(ts.RunFailed):
            ts.Client("judge", "gemini", "m", 60, 100, self.recorder, effort="high")


class JudgeTest(unittest.TestCase):
    """The judge's inputs, the mutants built from judge-control.yaml, and how a judgement is compared."""

    def setUp(self):
        self.files = {name: (HERE / name).read_text() for name in (ts.JUDGE_FILE, ts.JUDGE_CONTROL_FILE)}
        self.files.update({name: (HERE.parent / name).read_text() for name in (ts.REFERENCE_FILE, ts.ANTI_FILE)})
        self.parameters, self.requirements = ts.parse_reference(self.files[ts.REFERENCE_FILE])
        self.ids = [i for i, _ in self.requirements]
        self.control = ts.parse_control(self.files[ts.JUDGE_CONTROL_FILE], ts.JUDGE_CONTROL_FILE)
        self.mutants = {m["id"]: m for m in ts.build_mutants(self.control)}

    def perfect(self, mutant):
        return {"requirements": {r: {"coverage": c, "items": []} for r, c in mutant["coverage"].items()},
                "items": {i["id"]: {"class": i["class"], "requirements": [i["covers"]] if i["covers"] else []}
                          for i in mutant["items"]}}

    def test_reference_is_read_whole(self):
        self.assertEqual(len(self.requirements), len(set(self.ids)))
        self.assertEqual(self.ids, [f"BR-{n:02d}" for n in range(1, 39)])
        self.assertTrue(all(text for _, text in self.requirements))
        self.assertEqual(self.parameters, [])
        out_of_scope, technical = ts.parse_anti(self.files[ts.ANTI_FILE])
        self.assertTrue(out_of_scope and technical)
        system = ts.judge_system(self.files[ts.JUDGE_FILE], self.files)
        self.assertNotIn("{{", system)
        self.assertIn("stand for these values:\n(none)", system)

    def test_base_covers_every_reference_requirement_once(self):
        self.assertEqual(sorted(b["covers"] for b in self.control["base"]), sorted(self.ids))

    def test_mutants_are_what_their_entries_make_them(self):
        def counts(m):
            return [list(m["coverage"].values()).count(c) for c in ts.COVERAGE]
        self.assertEqual(counts(self.mutants["M1"]), [len(self.ids), 0, 0])
        self.assertEqual(counts(self.mutants["M2"]), [len(self.ids) - 8, 0, 8])
        self.assertEqual(counts(self.mutants["M5"]), [len(self.ids) - 6, 6, 0])
        self.assertEqual((self.mutants["M6"]["items"], counts(self.mutants["M6"])), ([], [0, 0, len(self.ids)]))
        classes = [i["class"] for i in self.mutants["M4"]["items"]]
        self.assertEqual((classes.count("user_visible"), classes.count("technical")), (4, 3))
        self.assertEqual([i["class"] for i in self.mutants["M3"]["items"]].count("other"), 6)
        # Ids are renumbered, so a gap or a trailing item reveals nothing.
        for m in self.mutants.values():
            self.assertEqual([i["id"] for i in m["items"]], [f"DR-{n:02d}" for n in range(1, len(m["items"]) + 1)])

    def test_exact_judgement_has_no_disagreement_and_a_wrong_one_is_named(self):
        m = self.mutants["M4"]
        right = self.perfect(m)
        self.assertEqual(ts.disagreements(m, right), [])
        wrong = json.loads(json.dumps(right))
        wrong["requirements"]["BR-01"]["coverage"] = "partial"
        added = next(i["id"] for i in m["items"] if i["class"] == "user_visible")
        wrong["items"][added]["class"] = "other"
        self.assertEqual(len(ts.disagreements(m, wrong)), 2)
        self.assertEqual(ts.score(right)["outOfScope"], 4)

    def test_judgement_must_list_everything_exactly_once(self):
        m = self.mutants["M1"]
        def reply(requirements, items):
            return json.dumps({"requirements": [{"id": r, "coverage": "covered", "items": []} for r in requirements],
                               "items": [{"id": i, "class": "reference", "requirements": []} for i in items]})
        item_ids = [i["id"] for i in m["items"]]
        self.assertIsNotNone(ts.parse_judgement(reply(self.ids, item_ids), self.ids, item_ids))
        self.assertIsNone(ts.parse_judgement(reply(self.ids[1:], item_ids), self.ids, item_ids))
        self.assertIsNone(ts.parse_judgement(reply(self.ids + self.ids[:1], item_ids), self.ids, item_ids))
        self.assertIsNone(ts.parse_judgement(reply(self.ids, item_ids[1:]), self.ids, item_ids))
        self.assertIsNone(ts.parse_judgement("not json", self.ids, item_ids))
        unhashable = json.loads(reply(self.ids, item_ids))
        unhashable["items"][0]["id"] = ["DR-01"]
        self.assertIsNone(ts.parse_judgement(json.dumps(unhashable), self.ids, item_ids))

    def test_judge_control_passes_only_when_every_judgement_is_exact(self):
        os.environ["GEMINI_API_KEY"] = "test-key"
        _urlopen, _sleep = ts.urllib.request.urlopen, ts.time.sleep
        # Every requirement missing and every item other: right for the empty contract only.
        def urlopen(request, timeout=0):
            text = json.loads(request.data)["contents"][-1]["parts"][0]["text"]
            items = [line.split(": ", 1)[1] for line in text.splitlines() if line.startswith("- id: ")]
            judgement = {"requirements": [{"id": r, "coverage": "missing", "items": []} for r in self.ids],
                         "items": [{"id": i, "class": "other", "requirements": []} for i in items]}
            return Reply({"candidates": [{"content": {"parts": [{"text": json.dumps(judgement)}]}, "finishReason": "STOP"}]},
                         headers())
        ts.urllib.request.urlopen, ts.time.sleep = urlopen, (lambda seconds: None)
        try:
            out = pathlib.Path(tempfile.mkdtemp())
            judge = ts.Client("judge", "gemini", "j", 60_000, 100, ts.Recorder(out), 0.0, 1)
            ts.judge_control(argparse.Namespace(repetitions=2), self.files, out, {}, judge)
        finally:
            ts.urllib.request.urlopen, ts.time.sleep = _urlopen, _sleep
        summary = json.loads((out / "judge-control.json").read_text())["summary"]
        self.assertEqual(summary, {"exact": 2, "of": 12, "passes": False})

    def test_judgement_of_the_wrong_shape_fails_the_run_without_a_second_request(self):
        os.environ["GEMINI_API_KEY"] = "test-key"
        _urlopen, _sleep = ts.urllib.request.urlopen, ts.time.sleep
        calls = []
        def urlopen(request, timeout=0):
            calls.append(1)
            return Reply({"candidates": [{"content": {"parts": [{"text": "{}"}]}, "finishReason": "STOP"}]}, headers())
        ts.urllib.request.urlopen, ts.time.sleep = urlopen, (lambda seconds: None)
        try:
            judge = ts.Client("judge", "gemini", "j", 60_000, 100, ts.Recorder(pathlib.Path(tempfile.mkdtemp())))
            with self.assertRaises(ts.RunFailed):
                ts.judge_one(judge, "system", "M1/1", self.ids, self.mutants["M1"]["items"])
        finally:
            ts.urllib.request.urlopen, ts.time.sleep = _urlopen, _sleep
        self.assertEqual(len(calls), 1)


class SubjectTest(unittest.TestCase):
    """The subject modes with a stubbed transport: an Anthropic subject, a Gemini persona and judge."""

    CONTRACT = "```yaml\n- id: DR-01\n  requirement: >\n    The service keeps each drone's\n    battery level.\n```"

    def setUp(self):
        os.environ["ANTHROPIC_API_KEY"] = os.environ["GEMINI_API_KEY"] = "test-key"
        self._urlopen, self._sleep, self._describe = ts.urllib.request.urlopen, ts.time.sleep, ts.Client.describe
        ts.time.sleep = lambda seconds: None
        ts.Client.describe = lambda client: {"id": client.model}
        self.subject_replies, self.requests = [], []
        ts.urllib.request.urlopen = self.urlopen
        names = ["world-brief.md", "brief-slices.yaml", "persona-prompt.md", "subject-naive-prompt.md",
                 "subject-interviewer-prompt.md", "subject-analyst-prompt.md"]
        self.files = {name: (HERE / name).read_text() for name in names}
        self.args = argparse.Namespace(subject_provider="anthropic", subject_model="s", subject_rpm=60_000,
                                       subject_max_tokens=100, persona_provider="gemini", persona_model="p",
                                       persona_rpm=60_000, persona_max_tokens=100, persona_temperature=0.0,
                                       persona_seed=1)

    def tearDown(self):
        ts.urllib.request.urlopen, ts.time.sleep, ts.Client.describe = self._urlopen, self._sleep, self._describe

    def urlopen(self, request, timeout=0):
        body = json.loads(request.data)
        self.requests.append((request.full_url, body))
        if request.full_url.endswith("/messages"):
            text = self.subject_replies.pop(0) if self.subject_replies else self.CONTRACT
            return Reply({"content": [{"type": "thinking", "thinking": "", "signature": "sig"}, {"type": "text", "text": text}],
                          "stop_reason": "end_turn", "id": "m", "model": "s"}, headers())
        return Reply({"candidates": [{"content": {"parts": [{"text": "An answer."}]}, "finishReason": "STOP"}]}, headers())

    def persona_calls(self):
        return [b for url, b in self.requests if "generateContent" in url]

    def run_mode(self, mode):
        out = pathlib.Path(tempfile.mkdtemp())
        (ts.subject_naive if mode == "subject-naive" else ts.subject_instructed)(
            self.args, self.files, {role: "notes" for role in ts.ROLES}, out, {})
        return json.loads((out / "subject.json").read_text())

    def test_question_is_exactly_one_ask_line(self):
        self.assertEqual(ts.question("ASK Technician: How do you start?"), ("technician", "How do you start?"))
        self.assertIsNone(ts.question("Let me ask.\nASK technician: How do you start?"))
        self.assertIsNone(ts.question("ASK technician:"))
        self.assertIsNone(ts.question("- id: DR-01"))

    def test_contract_is_read_from_its_yaml_block_or_the_whole_message(self):
        self.assertEqual(ts.read_contract("Here it is:\n" + self.CONTRACT + "\nDone."),
                         [{"id": "DR-01", "requirement": "The service keeps each drone's battery level."}])
        inline = "- id: DR-01\n  requirement: \"Pads are never lent.\"\n- id: DR-02\n  note: no requirement"
        self.assertEqual(ts.read_contract(inline), [{"id": "DR-01", "requirement": "Pads are never lent."}])
        self.assertEqual(ts.read_contract("The service should manage drones."), [])

    def test_business_is_brief_section_1_without_its_heading(self):
        text = ts.business(self.files["world-brief.md"])
        self.assertTrue(text.startswith("A platform company"))
        self.assertNotIn("## ", text)

    def test_naive_relays_questions_and_reads_the_contract(self):
        self.subject_replies = ["ASK technician: What do you do first?", "ASK nobody: Hello?",
                                "ASK desk: What is a closure?"]
        result = self.run_mode("subject-naive")
        self.assertEqual([e["role"] for e in result["exchanges"]], ["technician", "nobody", "desk"])
        self.assertEqual(result["exchanges"][1]["answer"], ts.NAIVE_NO_ROLE)
        self.assertEqual(len(self.persona_calls()), 2)
        self.assertEqual(result["metrics"]["turns_before_first_artifact"], 3)
        self.assertTrue(result["metrics"]["elicitation_initiated"])
        self.assertEqual(len(result["items"]), 1)
        subject_requests = [b for url, b in self.requests if url.endswith("/messages")]
        # The subject's earlier turns go back with their thinking block unchanged.
        self.assertEqual(subject_requests[1]["messages"][1]["content"][0]["type"], "thinking")
        self.assertNotIn("temperature", subject_requests[0])
        self.assertNotIn("output_config", subject_requests[0])
        self.assertNotIn("{{", subject_requests[0]["system"])

    def test_naive_without_a_question_has_not_elicited(self):
        result = self.run_mode("subject-naive")
        self.assertEqual((result["metrics"]["elicitation_initiated"], result["metrics"]["turns_before_first_artifact"]),
                         (False, 0))

    def test_naive_limit_ends_the_questions_and_a_further_one_is_the_last_message(self):
        self.subject_replies = ["ASK dispatcher: And then?"] * (ts.MAX_QUESTIONS_NAIVE + 5)
        result = self.run_mode("subject-naive")
        self.assertEqual(len(self.persona_calls()), ts.MAX_QUESTIONS_NAIVE)
        self.assertTrue(result["metrics"]["limitReached"])
        self.assertTrue(result["unreadable"])
        last_turn = [b for url, b in self.requests if url.endswith("/messages")][-1]["messages"][-1]["content"]
        self.assertIn(ts.NAIVE_NO_MORE, last_turn)

    def test_instructed_interviews_each_role_then_the_analyst_sees_only_transcripts(self):
        self.subject_replies = ["What is your day like?", "Tell me more.", "END OF INTERVIEW"] * 3
        result = self.run_mode("subject-instructed")
        self.assertEqual(result["metrics"]["questions_per_interview"], {r: 2 for r in ts.ROLES})
        self.assertEqual({i["ending"] for i in result["interviews"].values()}, {"ended_by_interviewer"})
        analyst = [b for url, b in self.requests if url.endswith("/messages")][-1]
        self.assertIn("Interviewee: An answer.", analyst["system"])
        self.assertNotIn(ts.business(self.files["world-brief.md"]), analyst["system"])
        self.assertEqual(analyst["messages"], [{"role": "user", "content": ts.ANALYST_START}])
        self.assertEqual(len(result["items"]), 1)

    def test_instructed_interview_ends_at_its_limit(self):
        self.subject_replies = ["Another question?"] * (3 * ts.MAX_QUESTIONS_INTERVIEW)
        result = self.run_mode("subject-instructed")
        self.assertEqual(result["metrics"]["limitReached"], {r: True for r in ts.ROLES})
        self.assertEqual(len(self.persona_calls()), 3 * ts.MAX_QUESTIONS_INTERVIEW)

    def test_judge_scores_only_the_other_vendor_and_renumbers_the_items(self):
        files = {name: (HERE / name).read_text() for name in (ts.JUDGE_FILE,)}
        files.update({name: (HERE.parent / name).read_text() for name in (ts.REFERENCE_FILE, ts.ANTI_FILE)})
        ids = [i for i, _ in ts.parse_reference(files[ts.REFERENCE_FILE])[1]]
        files["judged-subject.json"] = json.dumps({"items": [{"id": "R-7", "requirement": "a"}, {"id": "R-7", "requirement": "b"}]})
        files["judged-run.json"] = json.dumps({"mode": "subject-naive", "instruments": {"subject": {"provider": "anthropic", "model": "s"}}})
        judgement = json.dumps({"requirements": [{"id": r, "coverage": "missing", "items": []} for r in ids],
                                "items": [{"id": i, "class": "other", "requirements": []} for i in ("DR-01", "DR-02")]})
        ts.urllib.request.urlopen = lambda request, timeout=0: Reply(
            {"candidates": [{"content": {"parts": [{"text": judgement}]}, "finishReason": "STOP"}]}, headers())
        for provider, scored in (("gemini", True), ("anthropic", False)):
            if provider == "anthropic":
                ts.urllib.request.urlopen = lambda request, timeout=0: Reply(
                    {"content": [{"type": "text", "text": judgement}], "stop_reason": "end_turn", "id": "m", "model": "j"}, headers())
            out = pathlib.Path(tempfile.mkdtemp())
            judge = ts.Client("judge", provider, "j", 60_000, 100, ts.Recorder(out))
            ts.judge_run(argparse.Namespace(judged="r"), files, out, {}, judge)
            result = json.loads((out / "judgement.json").read_text())
            self.assertEqual(result["scored"], scored)
            self.assertEqual([(i["id"], i["read"]) for i in result["items"]], [("DR-01", "R-7"), ("DR-02", "R-7")])


class FollowUpTest(unittest.TestCase):
    """The follow-up classifier's pairs, reply, calibration and scoring."""

    def setUp(self):
        os.environ["GEMINI_API_KEY"] = "test-key"
        self._urlopen, self._sleep = ts.urllib.request.urlopen, ts.time.sleep
        ts.time.sleep = lambda seconds: None
        self.files = {name: (HERE / name).read_text() for name in (ts.FOLLOW_UP_FILE, ts.FOLLOW_UP_CONTROL_FILE)}

    def tearDown(self):
        ts.urllib.request.urlopen, ts.time.sleep = self._urlopen, self._sleep

    def label_all(self, value):
        def urlopen(request, timeout=0):
            text = json.loads(request.data)["contents"][-1]["parts"][0]["text"]
            ids = [line for line in text.splitlines() if re.fullmatch(r"Q\d+", line)]
            reply = json.dumps({"questions": [{"id": i, "follow_up": value} for i in ids]})
            return Reply({"candidates": [{"content": {"parts": [{"text": reply}]}, "finishReason": "STOP"}]}, headers())
        ts.urllib.request.urlopen = urlopen

    def test_reply_must_label_every_question_exactly_once(self):
        ok = json.dumps({"questions": [{"id": "Q2", "follow_up": True}, {"id": "Q3", "follow_up": False}]})
        self.assertEqual(ts.parse_follow_ups(ok, ["Q2", "Q3"]), {"Q2": True, "Q3": False})
        self.assertIsNone(ts.parse_follow_ups(ok, ["Q2"]))
        self.assertIsNone(ts.parse_follow_ups('{"questions": [{"id": "Q2", "follow_up": "yes"}]}', ["Q2"]))

    def test_pairs_follow_each_role_in_both_variants(self):
        naive = {"variant": "S-naive", "exchanges": [
            {"role": "desk", "question": "a", "answer": "A"}, {"role": "technician", "question": "b", "answer": "B"},
            {"role": "desk", "question": "c", "answer": "C"}, {"role": "nobody", "question": "d", "answer": "D"}]}
        self.assertEqual(ts.subject_pairs(naive), {"desk": [{"id": "Q2", "previous": "A", "question": "c"}]})
        instructed = {"variant": "S-instructed", "interviews": {"technician": {"transcript": [
            {"question": "a", "answer": "A"}, {"question": "b", "answer": "B"}]}}}
        self.assertEqual(ts.subject_pairs(instructed), {"technician": [{"id": "Q2", "previous": "A", "question": "b"}]})

    def test_control_set_is_forty_labelled_pairs(self):
        conversations = ts.parse_control(self.files[ts.FOLLOW_UP_CONTROL_FILE], ts.FOLLOW_UP_CONTROL_FILE)
        pairs = [p for c in conversations.values() for p in c]
        self.assertEqual(len(pairs), 40)
        self.assertTrue(all(p["follow_up"] in ("true", "false") and p["previous"] and p["question"] for p in pairs))

    def test_control_passes_only_at_the_threshold_in_every_repetition(self):
        self.label_all(True)
        out = pathlib.Path(tempfile.mkdtemp())
        judge = ts.Client("judge", "gemini", "j", 60_000, 100, ts.Recorder(out), 0.0, 1)
        ts.follow_up_control(argparse.Namespace(repetitions=2), self.files, out, {}, judge)
        summary = json.loads((out / "follow-up-control.json").read_text())["summary"]
        trues = self.files[ts.FOLLOW_UP_CONTROL_FILE].count("follow_up: true")
        self.assertEqual(summary["agreeing"], {"1": trues, "2": trues})
        self.assertFalse(summary["passes"])

    def test_run_ratio_is_scored_by_the_other_vendor_only(self):
        self.label_all(True)
        subject = {"variant": "S-instructed", "interviews": {r: {"transcript": [
            {"question": "a", "answer": "A"}, {"question": "b", "answer": "B"}, {"question": "c", "answer": "C"}]}
            for r in ts.ROLES}}
        files = {**self.files, "judged-subject.json": json.dumps(subject),
                 "judged-run.json": json.dumps({"mode": "subject-instructed",
                                                "instruments": {"subject": {"provider": "anthropic", "model": "s"}}})}
        out = pathlib.Path(tempfile.mkdtemp())
        judge = ts.Client("judge", "gemini", "j", 60_000, 100, ts.Recorder(out), 0.0, 1)
        ts.follow_up_run(argparse.Namespace(judged="r"), files, out, {}, judge)
        result = json.loads((out / "follow-ups.json").read_text())
        self.assertEqual((result["followUps"], result["of"], result["follow_up_ratio"], result["scored"]), (6, 6, 1.0, True))


class ModeTest(unittest.TestCase):
    """Each persona mode asks every question of its own set and writes its answers under its name."""

    def setUp(self):
        os.environ["MISTRAL_API_KEY"] = "test-key"
        self._urlopen, self._sleep, self._describe = ts.urllib.request.urlopen, ts.time.sleep, ts.Client.describe
        ts.urllib.request.urlopen = lambda request, timeout=0: Reply(answer("I don't know.", "stop"), headers())
        ts.time.sleep = lambda seconds: None
        ts.Client.describe = lambda client: {"id": client.model}

    def tearDown(self):
        ts.urllib.request.urlopen, ts.time.sleep, ts.Client.describe = self._urlopen, self._sleep, self._describe

    def test_each_mode_writes_its_own_answers(self):
        for mode, set_file in ts.QUESTION_SETS.items():
            out = pathlib.Path(tempfile.mkdtemp())
            args = argparse.Namespace(mode=mode, persona_provider="mistral", persona_model="m",
                                      persona_rpm=60_000, persona_max_tokens=100, repetitions=1,
                                      persona_temperature=0.0, persona_seed=1, persona_check=False)
            files = {name: (HERE / name).read_text() for name in ("persona-prompt.md", set_file)}
            ts.persona_control(args, files, {role: "notes" for role in ts.ROLES}, out, {})
            written = sorted(p.name for p in out.glob("*.json"))
            self.assertEqual(written, [f"{mode}.json"], mode)
            asked = json.loads((out / f"{mode}.json").read_text())
            expected = ts.parse_control(files[set_file], set_file)
            self.assertEqual({r: [a["id"] for a in reps[0]["answers"]] for r, reps in asked.items()},
                             {r: [q["id"] for q in qs] for r, qs in expected.items()}, mode)


    def test_checked_mode_records_draft_and_verdicts(self):
        def reply(request, timeout=0):
            checking = "response_format" in json.loads(request.data)
            check = json.dumps({"sentences": [{"verdict": "KEEP", "source": "DONT_KNOW"}]})
            return Reply(answer(check if checking else "I don't know.", "stop"), headers())
        ts.urllib.request.urlopen = reply
        out = pathlib.Path(tempfile.mkdtemp())
        args = argparse.Namespace(mode="persona-holdout-3", persona_provider="mistral", persona_model="m",
                                  persona_rpm=60_000, persona_max_tokens=100, repetitions=1,
                                  persona_temperature=0.0, persona_seed=1, persona_check=True)
        names = ("persona-prompt.md", "persona-holdout-3.yaml", ts.CHECK_FILE)
        files = {name: (HERE / name).read_text() for name in names}
        ts.persona_control(args, files, {role: "notes" for role in ts.ROLES}, out, {})
        first = json.loads((out / "persona-holdout-3.json").read_text())["technician"][0]["answers"][0]
        self.assertEqual((first["draft"], first["check"][0]["dropped"], first["answer"]), ("I don't know.", None, "I don't know."))
        self.assertEqual(len((out / "calls.jsonl").read_text().splitlines()), 2 * 24)


    def test_grader_control_counts_agreement(self):
        ts.urllib.request.urlopen = lambda request, timeout=0: Reply(
            answer('{"verdict": "FAIL", "contradicts": false, "reason": "r"}', "stop"), headers())
        out = pathlib.Path(tempfile.mkdtemp())
        files = {name: (HERE / name).read_text() for name in (ts.GRADER_FILE, ts.GRADER_CONTROL_FILE)}
        grader = ts.Client("grader", "mistral", "g", 60_000, 100, ts.Recorder(out), 0.0, 1)
        ts.grader_control(None, files, {role: "notes" for role in ts.ROLES}, out, {}, grader)
        summary = json.loads((out / "grader-control.json").read_text())["summary"]
        self.assertEqual((summary["agreeing"], summary["of"]), (24, 36))
        self.assertEqual(summary["passedContradictions"], [])

    def test_grade_run_grades_every_answer_of_the_run(self):
        ts.urllib.request.urlopen = lambda request, timeout=0: Reply(
            answer('{"verdict": "PASS", "contradicts": false, "reason": "r"}', "stop"), headers())
        answers = {role: [{"repetition": 1, "answers": [{"id": "X1", "kind": "fact", "question": "q", "expect": "e",
                                                         "answer": "a"}]}] for role in ts.ROLES}
        files = {ts.GRADER_FILE: (HERE / ts.GRADER_FILE).read_text(),
                 "graded-run.json": json.dumps({"mode": "persona-holdout-4"}), "graded-answers.json": json.dumps(answers)}
        out = pathlib.Path(tempfile.mkdtemp())
        grader = ts.Client("grader", "mistral", "g", 60_000, 100, ts.Recorder(out), 0.0, 1)
        ts.grade_run(argparse.Namespace(graded="r"), files, {role: "notes" for role in ts.ROLES}, out, {}, grader)
        result = json.loads((out / "grades.json").read_text())
        self.assertEqual(len(result["grades"]), 3)
        self.assertFalse(result["summary"]["passes"])  # three answers are not a deciding run of 72


class InputTest(unittest.TestCase):
    def test_every_brief_unit_has_a_slice(self):
        units = ts.parse_brief((HERE / "world-brief.md").read_text())
        slices, _ = ts.parse_slices((HERE / "brief-slices.yaml").read_text())
        self.assertEqual(set(units), set(slices))

    def test_question_sets_cover_every_role(self):
        for name in ts.QUESTION_SETS.values():
            control = ts.parse_control((HERE / name).read_text(), name)
            self.assertEqual(set(control), set(ts.ROLES), name)
            for questions in control.values():
                for q in questions:
                    self.assertEqual(set(q), {"id", "kind", "question", "expect"}, name)
                    self.assertIn(q["kind"], {"fact", "outside", "no-design"}, name)

    def test_question_sets_share_no_question(self):
        def questions(name):
            sets = ts.parse_control((HERE / name).read_text(), name)
            return [q for qs in sets.values() for q in qs]
        names = sorted(ts.QUESTION_SETS.values())
        kinds = lambda qs: sorted(q["kind"] for q in qs)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                qa, qb = questions(a), questions(b)
                self.assertFalse({q["id"] for q in qa} & {q["id"] for q in qb}, (a, b))
                self.assertFalse({q["question"] for q in qa} & {q["question"] for q in qb}, (a, b))
                self.assertEqual(kinds(qa), kinds(qb), (a, b))

    def test_out_outside_runs_track_s_is_refused(self):
        env = {**os.environ, "MISTRAL_API_KEY": "test-key"}
        for out in (tempfile.mkdtemp() + "/run", str(HERE.parent / "runs" / "pilot" / "x")):
            result = subprocess.run(
                [sys.executable, "-I", str(SCRIPT), "persona-control", "--persona-model", "m", "--out", out],
                capture_output=True, text=True, env=env)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--out must be a new directory under", result.stderr)

    def test_missing_key_leaves_no_run_directory(self):
        env = {k: v for k, v in os.environ.items() if k != "MISTRAL_API_KEY"}
        out = HERE.parent / "runs" / "track-s" / "test-missing-key-should-not-exist"
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "persona-control", "--persona-model", "m", "--out", str(out)],
            capture_output=True, text=True, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISTRAL_API_KEY", result.stderr)
        self.assertFalse(out.exists())

    def test_grade_refuses_a_run_that_is_not_a_completed_persona_run(self):
        env = {**os.environ, "MISTRAL_API_KEY": "test-key"}
        graded = pathlib.Path(tempfile.mkdtemp())
        (graded / "run.json").write_text(json.dumps({"mode": "persona-control", "status": "failed", "inputSha256": {}}))
        (graded / "persona-control.json").write_text("{}")
        out = HERE.parent / "runs" / "track-s" / "test-grade-should-not-exist"
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), "grade", "--grader-model", "g",
                                 "--graded", str(graded), "--out", str(out)], capture_output=True, text=True, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("only a completed persona run is graded", result.stderr)
        self.assertFalse(out.exists())

    def test_non_positive_rate_is_refused(self):
        os.environ["MISTRAL_API_KEY"] = "test-key"
        with self.assertRaises(ts.RunFailed):
            ts.Client("persona", "mistral", "m", 0, 100, None)

    def test_invalid_settings_leave_no_run_directory(self):
        env = {**os.environ, "MISTRAL_API_KEY": "test-key"}
        cases = [["--persona-model", "m", "--persona-rpm", "0"],
                 ["--persona-model", "m", "--persona-rpm", "-5"],
                 ["--persona-model", "mistral-small-latest"],
                 ["--persona-model", "m", "--persona-provider", "nobody"],
                 ["--persona-model", "m", "--repetitions", "0"],
                 ["--persona-model", "m", "--persona-temperature", "-0.1"]]
        for i, extra in enumerate(cases):
            out = HERE.parent / "runs" / "track-s" / f"test-invalid-settings-{i}-should-not-exist"
            result = subprocess.run([sys.executable, "-I", str(SCRIPT), "persona-control", *extra, "--out", str(out)],
                                    capture_output=True, text=True, env=env)
            self.assertNotEqual(result.returncode, 0, extra)
            self.assertFalse(out.exists(), extra)


if __name__ == "__main__":
    unittest.main(verbosity=2)
