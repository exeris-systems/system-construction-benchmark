---
title: "Analysis"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-11-14
---

# Analysis

Scripts that read committed run records and compute what the report gives. They are not instruments:
nothing here is called during a run, and nothing here changes a run record.

| File | What it computes |
| --- | --- |
| `track-s-cost.py` | The cost of each Track S subject run, from the subject's own calls; the cost of judging, separately |
| `prices.json` | Per-model token prices with the date range each holds for, and where they were read |
| `test_track_s_cost.py` | Tests of the pricing on synthetic calls: date bounds, long prompts, cached and thought tokens, unpriced kinds |

## Track S cost

```sh
python3 -I analysis/track-s-cost.py            # Markdown tables
python3 -I analysis/track-s-cost.py --json     # the same, as JSON
```

A subject run's cost counts only the calls whose role is `subject`: in S-naive the subject's
messages, in S-instructed the three interviews and the analyst. The persona answers every subject
alike and is left out. Each call is priced at the date in its `time` field, from the provider's own
usage report in `calls.jsonl`: for Gemini, prompt tokens at the input price and candidate plus
thought tokens at the output price; for Anthropic, input tokens at the input price and output
tokens, which include thinking, at the output price. A price the file does not hold, such as a cache
write, stops the script rather than counting as zero.

Attempts at one run (`-r2`, `-r3`, … under D-62) are grouped: the run's cost is what all its
attempts spent, failed ones included, and a run with no completed attempt is reported as
unobtainable. Recall is that of the run's scored judgement against `trackS/brief-requirements.yaml`;
judgements against the construction reference, made before D-61, are not used. Judge and follow-up
runs are summed per judge as the cost of measuring.

Prices change independently of the runs. `prices.json` records each price with the last date it
holds (`until`) and the source and date it was read. A new price is added as a new entry; the one
edit allowed to an existing entry is giving the open-ended one its `until`, the last day it held.

### What the figures do not cover

They are Track S subject runs only, at the standard (non-batch) price. A call with no usage report
is not priced. A run whose attempts all failed has a cost but no score, and a run with no scored
judgement against the brief-level reference has no recall. The prices are read by hand from the
sources `prices.json` names, so they can be wrong or out of date; the tests check the arithmetic,
not the prices.
