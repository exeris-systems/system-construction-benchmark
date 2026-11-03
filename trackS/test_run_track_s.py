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

    def test_check_keeps_only_the_kept_sentences(self):
        self.replies = [Reply(answer('{"verdicts": ["KEEP", "DROP", "keep"]}', "stop"), headers())]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "technician", "notes", "s", "q",
                          "We have pads. The platform owns them.\nI worry about that.")
        self.assertEqual(result["sentences"], ["We have pads.", "The platform owns them.", "I worry about that."])
        self.assertEqual(result["answer"], "We have pads. I worry about that.")
        self.assertEqual(result["draft"], "We have pads. The platform owns them.\nI worry about that.")

    def test_check_that_drops_everything_leaves_i_do_not_know(self):
        self.replies = [Reply(answer('{"verdicts": ["DROP"]}', "stop"), headers())]
        result = ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "It keeps versions.")
        self.assertEqual(result["answer"], ts.NOTHING_LEFT)

    def test_check_reply_of_the_wrong_shape_fails_the_run(self):
        for reply in ('{"verdicts": ["KEEP"]}', '{"verdicts": ["KEEP", "MAYBE"]}', "KEEP KEEP", '["KEEP", "KEEP"]'):
            self.replies = [Reply(answer(reply, "stop"), headers())]
            with self.assertRaises(ts.RunFailed, msg=reply):
                ts.check(self.client, "{{ROLE}} {{NOTES}}", "desk", "notes", "s", "q", "One. Two.")

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
            return Reply(answer('{"verdicts": ["KEEP"]}' if checking else "I don't know.", "stop"), headers())
        ts.urllib.request.urlopen = reply
        out = pathlib.Path(tempfile.mkdtemp())
        args = argparse.Namespace(mode="persona-holdout-3", persona_provider="mistral", persona_model="m",
                                  persona_rpm=60_000, persona_max_tokens=100, repetitions=1,
                                  persona_temperature=0.0, persona_seed=1, persona_check=True)
        names = ("persona-prompt.md", "persona-holdout-3.yaml", ts.CHECK_FILE)
        files = {name: (HERE / name).read_text() for name in names}
        ts.persona_control(args, files, {role: "notes" for role in ts.ROLES}, out, {})
        first = json.loads((out / "persona-holdout-3.json").read_text())["technician"][0]["answers"][0]
        self.assertEqual((first["draft"], first["verdicts"], first["answer"]), ("I don't know.", ["KEEP"], "I don't know."))
        self.assertEqual(len((out / "calls.jsonl").read_text().splitlines()), 2 * 24)


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
