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
                                      persona_rpm=60_000, persona_max_tokens=100, repetitions=1)
            files = {name: (HERE / name).read_text() for name in ("persona-prompt.md", set_file)}
            ts.persona_control(args, files, {role: "notes" for role in ts.ROLES}, out, {})
            written = sorted(p.name for p in out.glob("*.json"))
            self.assertEqual(written, [f"{mode}.json"], mode)
            asked = json.loads((out / f"{mode}.json").read_text())
            expected = ts.parse_control(files[set_file], set_file)
            self.assertEqual({r: [a["id"] for a in reps[0]["answers"]] for r, reps in asked.items()},
                             {r: [q["id"] for q in qs] for r, qs in expected.items()}, mode)


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
                 ["--persona-model", "m", "--repetitions", "0"]]
        for i, extra in enumerate(cases):
            out = HERE.parent / "runs" / "track-s" / f"test-invalid-settings-{i}-should-not-exist"
            result = subprocess.run([sys.executable, "-I", str(SCRIPT), "persona-control", *extra, "--out", str(out)],
                                    capture_output=True, text=True, env=env)
            self.assertNotEqual(result.returncode, 0, extra)
            self.assertFalse(out.exists(), extra)


if __name__ == "__main__":
    unittest.main(verbosity=2)
