"""Diagnosis, outside the run series: does gemini-4-argon still end with MALFORMED_RESPONSE when the
earlier model turns of the conversation carry the parts it returned, thought signatures included?

Replays the failing request of a recorded S-naive run in two arms, N times each:
  A  "text-only"   - the request exactly as the script sent it (each model turn is its text alone);
  B  "signatures"  - the same request, with each model turn replaced by the parts that model turn
                     returned (text and thoughtSignature), read from the run's own responses.
Prints the finish reason of every call and a count per arm. Writes nothing into runs/.
The key comes from GEMINI_API_KEY and is never printed.

Usage: python3 -I diag_thought_signatures.py <run-dir> [N]
"""
import copy
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def load(run):
    calls = [json.loads(line) for line in (run / "calls.jsonl").open()]
    calls = [c for c in calls if c["call"] != "describe"]
    failing = calls[-1]
    if failing["role"] != "subject":
        sys.exit("the last call of the run is not a subject call")
    request = json.loads((run / "requests" / f"{failing['call']}.json").read_text())
    body = request.get("body", request)
    subject_parts = []
    for c in calls[:-1]:
        if c["role"] == "subject":
            response = json.loads((run / "responses" / f"{c['call']}.json").read_text())
            subject_parts.append(response["candidates"][0]["content"]["parts"])
    return failing["model"], body, subject_parts


def with_signatures(body, subject_parts):
    signed = copy.deepcopy(body)
    model_turns = [c for c in signed["contents"] if c["role"] == "model"]
    if len(model_turns) != len(subject_parts):
        sys.exit(f"{len(model_turns)} model turns in the request, {len(subject_parts)} recorded responses")
    for turn, parts in zip(model_turns, subject_parts):
        recorded = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        sent = "".join(p.get("text", "") for p in turn["parts"])
        if recorded != sent:
            sys.exit("a model turn differs from the response it was read from")
        turn["parts"] = parts
    return signed


def call(model, body, key):
    request = urllib.request.Request(URL.format(model=model), data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "x-goog-api-key": key})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        return f"HTTP {error.code}", ""
    candidate = (payload.get("candidates") or [{}])[0]
    parts = (candidate.get("content") or {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return candidate.get("finishReason"), text


def main():
    run = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY is not set")
    model, body, subject_parts = load(run)
    arms = {"A text-only": body, "B signatures": with_signatures(body, subject_parts)}
    tally = {arm: Counter() for arm in arms}
    for i in range(n):
        for arm, arm_body in arms.items():
            finish, text = call(model, arm_body, key)
            tally[arm][finish] += 1
            print(f"{arm:13} #{i + 1}: {finish:20} {text[:90]!r}", flush=True)
            time.sleep(13)  # stays under 5 requests per minute
    print()
    for arm, counts in tally.items():
        print(f"{arm:13} {dict(counts)}")


if __name__ == "__main__":
    main()
