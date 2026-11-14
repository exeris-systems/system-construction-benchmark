#!/usr/bin/env python3
"""Cost of each Track S subject run, from the token usage its run record holds.

Reads every run under runs/track-s/ and prices each call with analysis/prices.json at the date the
call was made. A subject run's cost counts the subject's own calls only (in S-instructed, the
interviewer and the analyst); the persona answers for every subject alike and is left out. Judge and
follow-up runs are priced separately, as the cost of measuring, never as the subject's.

The score beside each run is the recall of its scored judgement against the brief-level reference
(trackS/brief-requirements.yaml). Attempts are grouped by run: `-r2`, `-r3`, ... are further
attempts at the same run, and a failed attempt costs what it spent.

Usage: python3 -I analysis/track-s-cost.py [--runs runs/track-s] [--prices analysis/prices.json] [--json]
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SUBJECT_MODES = {"subject-naive": "S-naive", "subject-instructed": "S-instructed"}
ATTEMPT = re.compile(r"^(?P<base>.+?)(?:-r(?P<n>\d+))?$")
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def price_for(prices, model, day):
    """The price entry for a model on a day: the first entry whose `until` is on or after it."""
    entries = prices["models"].get(model)
    if not entries:
        raise KeyError(f"no price for model {model}")
    for entry in entries:
        if "until" not in entry or day <= entry["until"]:
            return entry
    raise KeyError(f"no price for model {model} on {day}")


def call_cost(prices, call):
    """USD for one call, from the provider's own usage report."""
    usage, model, day = call.get("usage") or {}, call["model"], call["time"][:10]
    entry = price_for(prices, model, day)
    if "promptTokenCount" in usage or "candidatesTokenCount" in usage:  # Gemini
        cached = usage.get("cachedContentTokenCount", 0)
        prompt = usage.get("promptTokenCount", 0) - cached
        output = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
        tokens = {"input": prompt, "cache_read": cached, "output": output}
    else:  # Anthropic: output_tokens already include thinking
        if usage.get("cache_creation_input_tokens"):
            raise ValueError(f"{model}: cache writes have no price in prices.json")
        tokens = {"input": usage.get("input_tokens", 0),
                  "cache_read": usage.get("cache_read_input_tokens", 0),
                  "output": usage.get("output_tokens", 0)}
    rate = dict(entry)
    long_prompt = entry.get("long_prompt")
    if long_prompt and tokens["input"] + tokens["cache_read"] > long_prompt["above"]:
        rate.update(input=long_prompt["input"], output=long_prompt["output"])
    if tokens["cache_read"] and "cache_read" not in rate:
        raise ValueError(f"{model}: cache reads have no price in prices.json")
    return sum(tokens[k] * rate.get(k, 0) for k in tokens) / 1e6, tokens


def run_cost(prices, run, role):
    """USD and tokens of a run's calls by one role ('subject', 'judge')."""
    usd, totals = 0.0, defaultdict(int)
    for line in (run / "calls.jsonl").open():
        call = json.loads(line)
        if call.get("role") != role or call["call"] == "describe" or not call.get("usage"):
            continue
        cost, tokens = call_cost(prices, call)
        usd += cost
        for k, v in tokens.items():
            totals[k] += v
    return usd, dict(totals)


def load(runs):
    records = {}
    for path in sorted(runs.iterdir()):
        if (path / "run.json").is_file() and (path / "calls.jsonl").is_file():
            records[path] = json.loads((path / "run.json").read_text())
    return records


def scored_scores(records):
    """Subject run name -> score of its scored judgement against the brief-level reference."""
    scores = {}
    for path, record in records.items():
        if record.get("parameters", {}).get("mode") != "judge" or record.get("status") != "completed":
            continue
        if "trackS/brief-requirements.yaml" not in record.get("inputSha256", {}):
            continue  # judged against the construction reference, before D-61
        judgement = json.loads((path / "judgement.json").read_text())
        if judgement.get("scored"):
            scores[Path(judgement["judged"]["run"]).name] = judgement["score"]
    return scores


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--runs", default="runs/track-s")
    parser.add_argument("--prices", default="analysis/prices.json")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = parser.parse_args()
    runs, prices = Path(args.runs), json.loads(Path(args.prices).read_text())
    records = load(runs)
    scores = scored_scores(records)

    groups = defaultdict(list)
    for path, record in records.items():
        mode = record.get("parameters", {}).get("mode")
        if mode in SUBJECT_MODES:
            base = ATTEMPT.match(DATED.sub("", path.name)).group("base")
            groups[base].append((path, record))

    rows, measuring = [], defaultdict(float)
    for base, attempts in sorted(groups.items()):
        attempts.sort(key=lambda a: a[1].get("started", ""))
        params = attempts[0][1]["parameters"]
        usd, tokens = 0.0, defaultdict(int)
        completed = None
        for path, record in attempts:
            cost, used = run_cost(prices, path, "subject")
            usd += cost
            for k, v in used.items():
                tokens[k] += v
            if record.get("status") == "completed":
                completed = path
        score = scores.get(completed.name) if completed else None
        covered = score["covered"] if score else None
        rows.append({
            "run": base,
            "model": params.get("subject_model"),
            "variant": SUBJECT_MODES[params["mode"]],
            "attempts": len(attempts),
            "failed": sum(r.get("status") != "completed" for _, r in attempts),
            "completed": completed.name if completed else None,
            "usd": round(usd, 4),
            "tokens": dict(tokens),
            "recall": score["recall"] if score else None,
            "usd_per_covered": round(usd / covered, 4) if covered else None,
        })

    for path, record in records.items():
        mode = record.get("parameters", {}).get("mode")
        if mode in ("judge", "follow-up"):
            cost, _ = run_cost(prices, path, "judge")
            measuring[(mode, record["parameters"].get("judge_model"))] += cost

    if args.json:
        json.dump({"subject_runs": rows,
                   "measuring": [{"mode": m, "judge": j, "usd": round(c, 4)} for (m, j), c in sorted(measuring.items())]},
                  sys.stdout, indent=1)
        print()
        return
    print("| Run | Variant | Attempts (failed) | Subject USD | Recall (scored) | USD per covered |")
    print("| --- | --- | --- | --- | --- | --- |")
    for r in rows:
        recall_text = "unobtainable" if r["completed"] is None else ("-" if r["recall"] is None else f"{r['recall']:.2f}")
        per = "-" if r["usd_per_covered"] is None else f"{r['usd_per_covered']:.3f}"
        print(f"| {r['run']} | {r['variant']} | {r['attempts']} ({r['failed']}) | {r['usd']:.3f} | {recall_text} | {per} |")
    print()
    print("| Measuring | Judge | USD |")
    print("| --- | --- | --- |")
    for (mode, judge), usd in sorted(measuring.items()):
        print(f"| {mode} | {judge} | {usd:.3f} |")


if __name__ == "__main__":
    main()
