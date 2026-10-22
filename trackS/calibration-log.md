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
criteria of [`procedure.md`](procedure.md). It records instrument calibrations only, never subject
runs. The run records themselves are under `runs/track-s/`, unedited.

## Persona

| Run | Model | `persona-prompt.md` (SHA-256) | Verdict |
| --- | --- | --- | --- |
| `runs/track-s/2026-10-22-persona-control` | `ministral-8b-2512` | `0f180f10…bd9` | **fail** |
| `runs/track-s/2026-10-22-persona-control-2` | `ministral-8b-2512` | `b1cdf006…943` (draft 2) | **fail** |

### `2026-10-22-persona-control` — fail

72 calls, no error or retry, every answer finished with `stop`. The rate-limit headers report
625,000 tokens and 188 requests per minute and no daily or monthly limit.

Counted per answer, from `persona-control.json`: each control question asked in three repetitions.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 32 of 42 | T1 ×3: speaks for all three customers and estimates their fleets at 50 and 80–90, against "a few hundred". T4 ×3: a restart in flight gains failure modes ("flying in circles", "drifting"), against "carry on". D3 ×1: invents "two drones at a time". A4 ×3: invents a restart frequency, different in each repetition. |
| `outside` (7 questions) | 10 of 21 | T7 ×3: "the software picks the drone", contradicting §8 of the technician's slice. D6 ×3: invents connector names, different in each repetition. A5 ×2 and A7 ×2: estimate fleet sizes and causes of delay. T6 ×1: guesses how the desk sets a closure's length. |
| `no-design` (3 questions) | 5 of 9 | A8 ×3: says where closures should be stored. D8 ×1: proposes how routes are stored. |
| total | 47 of 72 | |

The persona keeps to its slice where the slice answers, and invents where it is silent. Revised in
`persona-prompt.md`: one organisation only; "I don't know" instead of estimating numbers, names,
types or frequencies; nothing about how a system works or keeps information.

### `2026-10-22-persona-control-2` — fail

The persona revised in draft 2 (D-49). 72 calls, no error or retry, every answer finished with
`stop`; the rate-limit headers report the same per-minute limits and no daily or monthly limit.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 28 of 42 | T1 ×3: still speaks for the customers and estimates fleet sizes. T2 ×2: invents connector types and pad categories. T4 ×3: a restart in flight gains failure modes, against "carry on". D3 ×3: estimates the number of places or a spacing between take-offs, or says sites are shared between companies. A4 ×3: estimates a restart frequency. |
| `outside` (7 questions) | 15 of 21 | T7 ×2: says someone other than the dispatcher picks the drone. A7 ×2: guesses why reports are delayed. D6 ×1: invents connector types. A5 ×1: estimates fleet sizes. |
| `no-design` (3 questions) | 7 of 9 | A8 ×2: describes how the service keeps closures. |
| total | 50 of 72 | |

Against the first run, the revised prompt raised `outside` and `no-design` answers, where saying "I
don't know" suffices, but not `fact` answers: the persona still adds details, numbers and failure
modes that its slice does not give, against an explicit instruction. The next draft changes the
persona model (D-49), which amends D-48.
