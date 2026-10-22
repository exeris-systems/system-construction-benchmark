---
title: "Track S calibration log"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Track S calibration log

Each calibration of a Track S instrument, with the inputs it ran on and its verdict against the
criteria of [`procedure.md`](procedure.md). The run records themselves are under `runs/track-s/`,
unedited.

## Persona

| Run | Model | `persona-prompt.md` (SHA-256) | Verdict |
| --- | --- | --- | --- |
| `runs/track-s/2026-10-22-persona-control` | `ministral-8b-2512` | `0f180f10…bd9` | **fail** |

### `2026-10-22-persona-control` — fail

72 calls, no error or retry, every answer finished with `stop`. The rate-limit headers report
625,000 tokens and 188 requests per minute and no daily or monthly limit.

| Kind | Result | Findings |
| --- | --- | --- |
| `fact` (12) | 10 pass | T1: the technician speaks for all three customers and estimates their fleets at 50 and 80–90, against "a few hundred" in its slice. T4: a restart in flight becomes "flying in circles", against "carry on". |
| `outside` (8) | 3 pass | T7, all three repetitions: "the software picks the drone", contradicting §8 of the technician's slice. D6 invents connector names, different in each repetition. A5 and A7 estimate figures and causes instead of saying they do not know. |
| `no-design` (6) | 3 pass | A8, all three repetitions: says where closures should be stored. D8, one repetition: proposes how routes are stored. |
| consistency | weak | Invented details differ between repetitions, e.g. A4's restart frequency. |

The persona keeps to its slice where the slice answers, and invents where it is silent. Revised in
`persona-prompt.md`: one organisation only; "I don't know" instead of estimating numbers, names,
types or frequencies; nothing about how a system works or keeps information.
