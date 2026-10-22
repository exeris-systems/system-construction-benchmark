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
| `runs/track-s/2026-10-22-persona-control-ministral-14b-2512` | `ministral-14b-2512` | `b1cdf006…943` (draft 2) | **fail** |
| `runs/track-s/2026-10-22-persona-control-8b-draft3` | `ministral-8b-2512` | `47c4d4fd…f4c` (draft 3) | **fail** |
| `runs/track-s/2026-10-22-persona-control-8b-f2f7fd73` | `ministral-8b-2512` | `f2f7fd73…563` (draft 3) | **fail** |
| `runs/track-s/2026-10-22-persona-control-8b-7d40bed8` | `ministral-8b-2512` | `7d40bed8…0c0` (draft 3, frozen) | **fail** |
| `runs/track-s/2026-10-22-persona-holdout` (held-out set `c3160a5e…`) | `ministral-8b-2512` | `7d40bed8…0c0` (draft 3, frozen) | **fail** |

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
modes that its slice does not give, against an explicit instruction.

### `2026-10-22-persona-control-ministral-14b-2512` — fail

The draft 2 prompt on the next larger model, at 25 requests per minute. 72 calls, no error or retry,
every answer finished with `stop`; the rate-limit headers report 937,500 tokens and 30 requests per
minute and no daily or monthly limit.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 31 of 42 | T1 ×3: speaks for the customers or estimates fleet sizes. T4 ×3: a restart in flight gains failure modes. A4 ×3: estimates a restart frequency. D1 ×2: adds what the software suggests and what the dispatcher checks. |
| `outside` (7 questions) | 11 of 21 | T7 ×3: someone other than the dispatcher picks the drone. D6 ×3: invents connector types, among them product names. T6 ×2: guesses "from what I've heard" how closures are set. D7 ×1: invents yesterday's disrupted jobs. A5 ×1: estimates fleet sizes. |
| `no-design` (3 questions) | 7 of 9 | A8 ×2: says closures are kept on the single server without a database. |
| total | 49 of 72 | |

The larger model scores as the smaller one did on the same prompt, with longer answers and more
invented detail. The next revisions keep `ministral-8b-2512` and change the prompt (D-50).

### `2026-10-22-persona-control-8b-draft3` — fail

The prompt rewritten in draft 3: the notes in a delimited read-only block, then numbered rules —
answer only from the notes and never invent, estimate or round; "I don't know" when the notes are
silent; one organisation; no events, causes or consequences the notes do not describe; nothing about
how a system works; two to four sentences. 72 calls, no error or retry, every answer finished with
`stop`; the same per-minute limits as the earlier `ministral-8b-2512` runs.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 39 of 42 | T1 ×3: the technician speaks of "each company I work for", as if working for the platform. |
| `outside` (7 questions) | 21 of 21 | |
| `no-design` (3 questions) | 7 of 9 | T8 ×2: lists screens and buttons when asked for them. |
| total | 67 of 72 | |

Revised: the persona works for exactly one organisation, named in its first sentence, and does not
describe screens, buttons or features even when asked for them.

### `2026-10-22-persona-control-8b-f2f7fd73` — fail

72 calls, no error or retry, every answer finished with `stop`; the same per-minute limits.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 42 of 42 | |
| `outside` (7 questions) | 18 of 21 | D6 ×3: "I don't know", then says the platform company manages the charging equipment, contradicting 3.b2 of the dispatcher's slice. |
| `no-design` (3 questions) | 9 of 9 | |
| total | 69 of 72 | |

Revised: the persona names someone who would know only when its notes say that person or team does
that work.

### `2026-10-22-persona-control-8b-7d40bed8` — fail

The prompt frozen by D-50. 72 calls, no error or retry, every answer finished with `stop`; the same
per-minute limits.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 40 of 42 | A2 ×2: "I don't know", and refers to a business team of the platform that its notes do not name. |
| `outside` (7 questions) | 17 of 21 | D6 ×3: unchanged, the platform company manages the charging equipment. A6 ×1: refers to a technical team its notes do not name. |
| `no-design` (3 questions) | 9 of 9 | A8 ×3 also refers to a technical team its notes do not name; no design, so the answers pass. |
| total | 66 of 72 | |

The last revision did not remove D6, and moved invented referrals to other questions. The control
set has now shaped the prompt across five runs; the held-out set decides (D-50).

### `2026-10-22-persona-holdout` — fail

The held-out set (`persona-holdout.yaml`, SHA-256 `c3160a5e…`), run once with the frozen prompt, as
D-50 sets out. 72 calls, no error or retry, every answer finished with `stop`; the same per-minute
limits.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 38 of 42 | HT1 ×1: says it manages maintenance schedules. HT2 ×2: "I don't know" whether anyone outside can ask, against 3.b3; one adds that the platform handles what is shared with regulators. HD4 ×1: invents who reports a ready load. |
| `outside` (7 questions) | 14 of 21 | HD7 ×3: "I don't know", then guesses what the desk does after entering a closure. HA6 ×2: says the companies' billing systems need nothing. HT6 ×1: refers to a team its notes do not name. HD6 ×1: speaks of the drone operating companies as if it worked for none of them. |
| `no-design` (3 questions) | 5 of 9 | HD8 ×3: asks for the service to notify it automatically. HT8 ×1: lists what the service should let it log. |
| total | 57 of 72 | |

The persona fails on both criteria of D-50. 57 of 72 is below the threshold of 65, and one `fact`
answer contradicts its slice: HT2 in its third repetition says the platform handles what is shared
with regulators, where 3.b3 has the regulators ask the company. The other `fact` failures add what
the slice does not give, or answer "I don't know" where it answers, without asserting the opposite.
Counting the borderline failures as passing (HT1, HD4, HT6) gives 60. Against 66 of 72 on the
control set, the prompt kept its gains on the questions it was revised against and lost them on new
ones.
