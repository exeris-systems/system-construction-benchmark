"""Tests of analysis/track-s-cost.py on synthetic calls and prices; no run record is read.

Run from the repository root: python3 -I analysis/test_track_s_cost.py
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("track_s_cost", Path(__file__).with_name("track-s-cost.py"))
cost = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cost)

PRICES = {"models": {
    "dated": [{"until": "2026-11-30", "input": 2.0, "output": 10.0, "cache_read": 0.1},
              {"input": 4.0, "output": 20.0, "cache_read": 0.2}],
    "haiku": [{"input": 0.1, "output": 0.5, "long_prompt": {"above": 100000, "input": 0.5, "output": 2.5}}],
    "nocache": [{"input": 1.0, "output": 1.0}],
}}


def gemini(model, day, prompt, candidates, thoughts=0, cached=0):
    usage = {"promptTokenCount": prompt, "candidatesTokenCount": candidates, "thoughtsTokenCount": thoughts}
    if cached:
        usage["cachedContentTokenCount"] = cached
    return {"model": model, "time": f"{day}T12:00:00+00:00", "usage": usage}


def anthropic(model, day, inp, out, cache_read=0, cache_write=0):
    usage = {"input_tokens": inp, "output_tokens": out,
             "cache_read_input_tokens": cache_read, "cache_creation_input_tokens": cache_write}
    return {"model": model, "time": f"{day}T12:00:00+00:00", "usage": usage}


class PriceTest(unittest.TestCase):
    def test_a_dated_price_holds_through_its_until_day(self):
        usd, _ = cost.call_cost(PRICES, gemini("dated", "2026-11-30", 1_000_000, 0))
        self.assertAlmostEqual(usd, 2.0)

    def test_the_next_price_holds_from_the_day_after(self):
        usd, _ = cost.call_cost(PRICES, gemini("dated", "2026-12-01", 1_000_000, 0))
        self.assertAlmostEqual(usd, 4.0)

    def test_a_model_with_no_price_stops(self):
        with self.assertRaises(KeyError):
            cost.call_cost(PRICES, gemini("unknown", "2026-11-14", 1, 1))


class GeminiTest(unittest.TestCase):
    def test_thoughts_are_priced_as_output_and_cached_tokens_as_cache_reads(self):
        usd, tokens = cost.call_cost(PRICES, gemini("dated", "2026-11-14", 1_000_000, 100_000, 400_000, cached=200_000))
        self.assertEqual(tokens, {"input": 800_000, "cache_read": 200_000, "output": 500_000})
        self.assertAlmostEqual(usd, 0.8 * 2.0 + 0.2 * 0.1 + 0.5 * 10.0)


class AnthropicTest(unittest.TestCase):
    def test_input_and_output_at_their_prices(self):
        usd, _ = cost.call_cost(PRICES, anthropic("haiku", "2026-11-14", 1_000_000 // 20, 1_000_000))
        self.assertAlmostEqual(usd, 0.05 * 0.1 + 1.0 * 0.5)

    def test_a_prompt_above_the_threshold_takes_the_long_prompt_price(self):
        usd, _ = cost.call_cost(PRICES, anthropic("haiku", "2026-11-14", 100_001, 0))
        self.assertAlmostEqual(usd, 100_001 * 0.5 / 1e6)

    def test_a_prompt_at_the_threshold_keeps_the_base_price(self):
        usd, _ = cost.call_cost(PRICES, anthropic("haiku", "2026-11-14", 100_000, 0))
        self.assertAlmostEqual(usd, 100_000 * 0.1 / 1e6)

    def test_a_cache_write_stops(self):
        with self.assertRaises(ValueError):
            cost.call_cost(PRICES, anthropic("dated", "2026-11-14", 1, 1, cache_write=10))

    def test_a_cache_read_without_a_price_stops(self):
        with self.assertRaises(ValueError):
            cost.call_cost(PRICES, anthropic("nocache", "2026-11-14", 1, 1, cache_read=10))


class RunTest(unittest.TestCase):
    def write_run(self, root, name, mode, status, calls, started):
        run = root / name
        run.mkdir()
        record = {"status": status, "started": started, "parameters": {"mode": mode, "subject_model": "dated"}}
        (run / "run.json").write_text(json.dumps(record))
        (run / "calls.jsonl").write_text("".join(json.dumps(c) + "\n" for c in calls))
        return run

    def test_attempts_are_grouped_and_all_their_costs_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            call = {"call": "0001", "role": "subject", **gemini("dated", "2026-11-14", 1_000_000, 0)}
            persona = {"call": "0002", "role": "persona", **gemini("dated", "2026-11-14", 1_000_000, 0)}
            self.write_run(root, "2026-11-14-subject-naive-dated-1", "subject-naive", "failed", [call, persona], "1")
            self.write_run(root, "2026-11-14-subject-naive-dated-1-r2", "subject-naive", "completed", [call], "2")
            records = cost.load(root)
            groups = cost.group_attempts(records)
            self.assertEqual(list(groups), ["subject-naive-dated-1"])
            scores = {"2026-11-14-subject-naive-dated-1-r2": {"recall": 0.5, "covered": 4}}
            row = cost.run_row(PRICES, scores, "subject-naive-dated-1", groups["subject-naive-dated-1"])
            self.assertEqual((row["attempts"], row["failed"]), (2, 1))
            self.assertAlmostEqual(row["usd"], 4.0)  # two subject calls; the persona's is left out
            self.assertAlmostEqual(row["usd_per_covered"], 1.0)

    def test_a_run_with_no_completed_attempt_is_unobtainable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            call = {"call": "0001", "role": "subject", **gemini("dated", "2026-11-14", 1, 1)}
            self.write_run(root, "2026-11-14-subject-naive-dated-1", "subject-naive", "failed", [call], "1")
            groups = cost.group_attempts(cost.load(root))
            row = cost.run_row(PRICES, {}, "subject-naive-dated-1", groups["subject-naive-dated-1"])
            self.assertIsNone(row["completed"])
            self.assertEqual(cost.recall_text(row), "unobtainable")


class PathTest(unittest.TestCase):
    def test_a_path_outside_the_root_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(SystemExit):
            cost.within(Path(tmp).resolve(), "../elsewhere")


if __name__ == "__main__":
    unittest.main()
