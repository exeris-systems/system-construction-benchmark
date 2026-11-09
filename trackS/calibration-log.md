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
| `runs/track-s/2026-10-22-persona-holdout-2` (held-out set 2 `616089c9…`) | `mistral-small-2603` | `7d40bed8…0c0` (draft 4) | **run failed** — no answer |
| `runs/track-s/2026-11-03-persona-holdout-2` (held-out set 2 `616089c9…`) | `ministral-14b-2512`, temperature 0, seed 1 | `7d40bed8…0c0` (draft 4) | **fail** |
| `runs/track-s/2026-11-03-persona-control-check` | `ministral-8b-2512`, temperature 0, seed 1, check pass | `7d40bed8…0c0`, check `9fd79962…` (draft 5) | 68 of 72, control set — does not decide |
| `runs/track-s/2026-11-03-persona-holdout-3` (held-out set 3 `e3c5ca02…`) | `ministral-8b-2512`, temperature 0, seed 1, check pass | `7d40bed8…0c0`, check `9fd79962…` (draft 5, frozen) | **fail** |
| `runs/track-s/2026-11-03-persona-control-sourced` | `ministral-8b-2512`, temperature 0, seed 1, sourced check | `7d40bed8…0c0`, check `084a1335…` (draft 6) | **run failed** — check reply of the wrong shape |
| `runs/track-s/2026-11-03-persona-control-sourced-2` | `ministral-8b-2512`, temperature 0, seed 1, sourced check | `7d40bed8…0c0`, check `d660c0fa…` (draft 6) | **run failed** — check entries without their object |
| `runs/track-s/2026-11-03-persona-control-sourced-3`, graded in `runs/track-s/2026-11-03-grade-persona-control-sourced-3` | `ministral-8b-2512`, temperature 0, seed 1, sourced check | `7d40bed8…0c0`, check `d660c0fa…` (draft 6) | 57 of 72 by the grader, control set — does not decide |
| `runs/track-s/2026-11-03-persona-control-check`, graded again in `runs/track-s/2026-11-03-grade-persona-control-check` | `ministral-8b-2512`, temperature 0, seed 1, check pass | `7d40bed8…0c0`, check `9fd79962…` (draft 5) | 57 of 72 by the grader, against 68 by hand — does not decide |
| `runs/track-s/2026-11-03-persona-control-a097ba45`, graded in `runs/track-s/2026-11-03-grade-persona-control-a097ba45` | `ministral-8b-2512`, temperature 0, seed 1, sourced check | `a097ba45…`, check `d660c0fa…` (draft 6) | 59 of 72 by the grader, control set — does not decide |
| `runs/track-s/2026-11-03-persona-control-flash-lite`, graded in `runs/track-s/2026-11-03-grade-persona-control-flash-lite` | `gemini-3.5-flash-lite`, temperature 0, seed 1, no check | `a097ba45…` (draft 6) | 66 of 72 by the grader, control set — does not decide |
| `runs/track-s/2026-11-03-persona-control-flash-lite-check`, graded in `runs/track-s/2026-11-03-grade-persona-control-flash-lite-check` | `gemini-3.5-flash-lite`, temperature 0, seed 1, sourced check | `a097ba45…`, check `d660c0fa…` (draft 6) | 57 of 72 by the grader, control set — does not decide |
| `runs/track-s/2026-11-03-persona-holdout-4` (held-out set 4 `377c6e99…`), graded in `runs/track-s/2026-11-03-grade-persona-holdout-4` | `gemini-3.5-flash-lite`, temperature 0, seed 1, no check | `a097ba45…` (draft 6, frozen) | **fail** — 63 of 72 by the grader |
| `runs/track-s/2026-11-03-persona-control-8e49283b`, graded in `runs/track-s/2026-11-03-grade-persona-control-8e49283b` | `gemini-3.5-flash-lite`, temperature 0, seed 1, no check | `8e49283b…` (draft 7) | 69 of 72 by the grader, control set — does not decide |
| `runs/track-s/2026-11-03-persona-holdout-5` (held-out set 5 `08aeb8cb…`), graded in `runs/track-s/2026-11-03-grade-persona-holdout-5` | `gemini-3.5-flash-lite`, temperature 0, seed 1, no check | `8e49283b…` (draft 7, frozen) | **pass** — 69 of 72 by the grader |

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

### `2026-10-22-persona-holdout-2` — run failed

Draft 4's deciding run. The model check passed: the provider describes `mistral-small-2603` as
"Mistral Small 4", with reasoning among its capabilities. The first question was refused with HTTP
429 on every one of eight attempts over ten minutes, and the run failed as an infrastructure error.
Each refusal reports `x-ratelimit-limit-req-minute: 0`: the key is allowed no requests to this
model, so the run records no answer and no verdict.

A second attempt on `mistral-small-2603` at temperature 0 and seed 1 met the same refusals, eight
calls with no answer, and was interrupted by hand. Its directory was not kept. `mistral-medium-2604`
answers with the same refusal and a limit of 0 requests per minute, so draft 4 moves to
`ministral-14b-2512` (D-51).

### `2026-11-03-persona-holdout-2` — fail

Draft 4's deciding run: the second held-out set, run once at temperature 0 and random seed 1, both
sent with every request. 72 calls; three were refused once with HTTP 429, "Not enough capacity
available", and answered on retry; every answer finished with `stop`. The rate-limit headers report
937,500 tokens and 30 requests per minute and no daily or monthly limit.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 31 of 42 | JT1 ×3: describes setting up a drone "so the system knows" its sensors and connector. JD1 ×3: adds that a delivery drone must return home. JT2 ×1: says a drone charges only at its home site. JT4 ×1: speaks of "each company we work with", as if working for the platform. JD2 ×1: says the authorities define the corridors. JD3 ×1: links a drained battery to a restart in flight. JA1 ×1: says these are the only customers. |
| `outside` (7 questions) | 12 of 21 | JD6 ×3: "I don't know", then names a technical team, an equipment team or the manufacturer. JD7 ×3: "I don't know", then says the company's own billing systems handle the platform's charge. JA7 ×2: says the desk or the service tracks where drones fly. JT6 ×1: says closures last a few minutes, taking them for restarts of the service. |
| `no-design` (3 questions) | 0 of 9 | JT8 ×3: the service should stop a drone going to the wrong pad. JD8 ×3: the service should show that a drone is taken. JA8 ×3: the service should record every version of a closure. |
| total | 43 of 72 | |

Below the threshold of 65; no `fact` answer contradicts its slice. JD5 ×3 also says the companies
handle weather in their own systems, which the slice does not say; counted as passing, the verdict
is the same either way. The answers often run past four sentences. At temperature 0 with a fixed
seed, no question received the same answer in all three repetitions: the provider's sampling is not
deterministic under these settings, so agreement across repetitions still tests the persona.

### `2026-11-03-persona-control-check` — 68 of 72, does not decide

Draft 5 on the control set: the answering pass, then the check pass (`persona-check-prompt.md`,
SHA-256 `9fd79962…`), both on `ministral-8b-2512` at temperature 0 and seed 1. 144 calls, no error
or retry, every answer and check finished with `stop`, and every check reply had one verdict per
sentence. The check dropped 40 of 152 sentences. Graded on the answers after the check.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 38 of 42 | T1 ×2: "I don't know how many drones the platform company runs", as if the platform ran drones; the check keeps a sentence that says the speaker does not know. T2 ×1: a drone charges only at its home site, kept by the check. A2 ×1: "I don't know", then only the desk's scope; the check dropped the referral that followed. |
| `outside` (7 questions) | 21 of 21 | |
| `no-design` (3 questions) | 9 of 9 | |
| total | 68 of 72 | |

Above the threshold of 65, but this is the control set, which does not decide. The check removed
every invented referral and every design that the same prompt produced on the control set before;
D6, which failed in every earlier run, is now "I don't know." three times. It also drops sentences
the slice supports: the places where radio coverage is patchy (T5), the connector types being
several and not interchangeable (D6), and in D5 the closure coming into force while drones fly,
leaving answers that are vague but not wrong. It keeps what it is told to keep, so a sentence that
says the speaker does not know passes even when it misplaces who runs the drones (T1).

### `2026-11-03-persona-holdout-3` — fail

Draft 5's deciding run: the third held-out set, run once with both prompts frozen. 144 calls, no
error or retry, every answer and check finished with `stop`, and every check reply had one verdict
per sentence. The check dropped 45 of 152 sentences. Graded on the answers after the check, under
the same rules as every earlier run.

| Kind | Answers passing | Failing answers |
| --- | --- | --- |
| `fact` (14 questions) | 38 of 42 | KT2 ×2: a drone returns to its home site when not in use or after jobs. KD1 ×2: adds checks the dispatcher makes before a flight — battery, sensors, connector, the load being ready — that the slice does not give. |
| `outside` (7 questions) | 19 of 21 | KA5 ×2: "I don't know", then says the platform company does not track or manage individual drones; the slice says only that the desk has no business looking into one company's operations. |
| `no-design` (3 questions) | 7 of 9 | KT8 ×2: "the service should tell me that a charging pad is offline", kept by the check against its own rule. |
| total | 64 of 72 | |

One answer below the threshold of 65; no `fact` answer contradicts its slice. The verdict rests on
judgement in a few answers, and they were graded as their like was in earlier runs: KT2 and KD1 as
HT1 and HD4 were, by what they add rather than what they get right. Every `outside` failure but
KA5, and every `no-design` failure but KT8, of the earlier held-out runs is absent: the check
dropped the referrals, guesses and designs. What remains is what the check kept — an added
consequence or duty inside a sentence that is otherwise in the notes, and one design.

### `2026-11-03-persona-control-sourced` — run failed

Draft 6's first control run, with the check that gives sources. The first check reply copied the
prompt's example instead of following it: four entries for two sentences, wrapped in a list, and a
source that began with the example's placeholder text. The run failed on that reply, as the
procedure sets out. Revised: the check prompt describes the reply in words instead of showing an
example, and the script states in each request how many sentences there are and asks for exactly
that many entries.

### `2026-11-03-persona-control-sourced-2` — run failed

The revised check prompt (`d660c0fa…`). The first check reply had the right number of entries, with
the right verdicts and a source found in the notes, but as a bare list without the object around it,
and the script refused that shape. Revised: the script takes the entries with or without the object
around them, and still requires one verdict and source per sentence.

### `2026-11-03-persona-control-sourced-3` — 57 of 72 by the grader, does not decide

The sourced check on the control set, graded by the calibrated grader (`gemini-3.8-flash`, grader
prompt `d691edd3…`) in `2026-11-03-grade-persona-control-sourced-3`. The persona run made 144
calls; one check was retried after a failed name lookup, and no check reply needed asking again.
The check dropped 63 of 139 sentences, every one of them by its own verdict: no kept sentence had a
source missing from the notes. The grading made 72 calls, no error, every grade `STOP`.

| Kind | Answers passing | Failing answers, with the grader's reason |
| --- | --- | --- |
| `fact` (14 questions) | 28 of 42 | D3 ×3, marked as contradicting: "No, each site has only so many places", where several flights can take off up to that number. A2 ×3: "I don't know", where the notes answer. T2 ×2: pads "set up for a specific connector type" or "for specific drone models". T4 ×2: a restarted drone "usually" carries on. T1 ×2: answers for the customers rather than for its own company. D5 ×1: a duty to keep drones flying safely instead of the fact. A1 ×1: the companies need the information "to operate safely". |
| `outside` (7 questions) | 20 of 21 | D6 ×1: states the connector facts without saying it does not know which types. |
| `no-design` (3 questions) | 9 of 9 | |
| total | 57 of 72 | |

Below the threshold, with three contradicting `fact` answers. Two things change at once against
draft 5's 68 on the same set, and this run cannot tell them apart: the check drops more — 45 per
cent of the sentences against 26 — leaving `fact` answers emptied to "I don't know" or a fragment,
and the grader is stricter than the grading by hand was. D3 passed by hand in every earlier run; the
grader reads its "No" as contradicting the notes.

### `2026-11-03-persona-control-check`, graded by the grader — 57 of 72

Draft 5's control run, graded by hand at 68 of 72 above, graded again by the grader to tell its
check apart from the grading. 72 calls, no error. The grader passes 27 of 42 `fact` answers, 21 of
21 `outside` and 9 of 9 `no-design`: 57 of 72, with D3 marked as contradicting in all three
repetitions. The 11 answers it fails beyond the hand grading are D3 ×3, D5 ×3, A2 ×3 ("I don't
know", then the desk's scope), T4 ×1 and D4 ×1, each failed for an added duty or consequence or for
not stating the fact.

Both checks score 57 on the control set under the grader, so the sourced check of draft 6 neither
gains nor loses there. The hand grading of every earlier run was more lenient than the grader by
about this margin, and its verdicts are not on the grader's scale.

### `2026-11-03-persona-control-a097ba45` — 59 of 72 by the grader, does not decide

The answering prompt revised against the graded control run (`a097ba45…`); check, model and grader
unchanged. Both runs completed without error; no check reply needed asking again. The check dropped
57 of 127 sentences.

| Kind | Answers passing | Failing answers, with the grader's reason |
| --- | --- | --- |
| `fact` (14 questions) | 29 of 42 | D3 ×3, still marked as contradicting: the answer still begins "No". T2 ×3: pads "set up for" specific connectors, and no plain "no". D5 ×3: a duty to deal with the closure, or "I don't know." left by the check. T4 ×2: "without human intervention". T1 ×1 and D1 ×1: "I don't know." left by the check. |
| `outside` (7 questions) | 21 of 21 | |
| `no-design` (3 questions) | 9 of 9 | |
| total | 59 of 72 | |

The revision removed the failures it aimed at in A2 and A1, and the frequency word in T4, but not
the "No" in D3, which the check keeps with a source from the notes. Three `fact` answers now fail
because the check dropped every sentence, one of them true to the notes: D1's "I decide which drone
flies and along which way". The answering pass and the check, on the same small model, each still
err in both directions.

### `2026-11-03-persona-control-flash-lite` and `-check` — 66 and 57 of 72 by the grader

The persona on `gemini-3.5-flash-lite` (a thinking model, by its own description), with the
answering prompt `a097ba45…`, once without the check and once with it; both graded by the grader.
All four runs completed without error, every response `STOP`; no check reply needed asking again.
With the check, 27 of 111 sentences were dropped.

| Kind | Without the check | With the check |
| --- | --- | --- |
| `fact` (14 questions) | 39 of 42 — T3 ×3: "I don't know.", where the notes say pads are never lent | 30 of 42 — T3 ×3 and T5 ×3: "I don't know." left by the check; D2 ×3: the check dropped the "no" and kept only "However, we do want help…"; A2 ×3: "I don't know." before the desk's wish |
| `outside` (7 questions) | 18 of 21 — D6 ×3: states that the connector types are several and not interchangeable, without saying it does not know which | 18 of 21 — D6 ×3, the same |
| `no-design` (3 questions) | 9 of 9 | 9 of 9 |
| total | 66 of 72 | 57 of 72 |

No answer in either run contradicts its slice. Without the check the persona is above the threshold
on the control set for the first time under the grader; with it, the check removes answers the
notes give. The persona runs without the check (D-53), with its answering prompt frozen.

### `2026-11-03-persona-holdout-4` — fail, 63 of 72 by the grader

Draft 6's deciding run: the fourth held-out set, run once with the persona frozen, graded by the
calibrated grader. Both runs completed without error, every response `STOP`.

| Kind | Answers passing | Failing answers, with the grader's reason |
| --- | --- | --- |
| `fact` (14 questions) | 33 of 42 | LT4 ×3, LD3 ×3, LA2 ×3: "I don't know.", where the notes answer — what the companies do not want (8.b4, twice) and what the company's own systems need to hear (7.b2). |
| `outside` (7 questions) | 21 of 21 | |
| `no-design` (3 questions) | 9 of 9 | |
| total | 63 of 72 | |

Two below the threshold of 65, with no contradicting answer; the grader's verdict is fail. Every
failure is the same one: the persona says it does not know what its notes state about "the
companies" or "each company", as it did about pads never being lent (T3) on the control set. It no
longer adds to its notes; it now holds back from part of them.

### `2026-11-03-persona-control-8e49283b` — 69 of 72 by the grader, does not decide

The persona of draft 7, with rule 3 revised (D-54), on the control set, graded by the grader. Both
runs completed without error, every response `STOP`.

| Kind | Answers passing | Failing answers, with the grader's reason |
| --- | --- | --- |
| `fact` (14 questions) | 42 of 42 | |
| `outside` (7 questions) | 18 of 21 | D6 ×3: states that the connector types are several and not interchangeable, and that pads are never lent, without saying it does not know which types. |
| `no-design` (3 questions) | 9 of 9 | |
| total | 69 of 72 | |

No answer contradicts its slice. T3 is answered in all three repetitions with "Pads are never lent
to another company.", and no answer speaks for another company. D6 fails as it did under draft 6.

### `2026-11-03-persona-holdout-5` — pass, 69 of 72 by the grader

Draft 7's deciding run: the fifth held-out set, run once with the persona frozen, graded by the
calibrated grader. Both runs completed without error, every response `STOP`.

| Kind | Answers passing | Failing answers, with the grader's reason |
| --- | --- | --- |
| `fact` (14 questions) | 39 of 42 | MT2 ×3: "I don't know.", where the notes list billing among what the companies do not want (8.b11). |
| `outside` (7 questions) | 21 of 21 | |
| `no-design` (3 questions) | 9 of 9 | |
| total | 69 of 72 | |

Four above the threshold of 65, with no `fact` answer contradicting its slice; the grader's verdict
is pass. The persona of draft 7 is calibrated.

## Grader

| Run | Model | `grader-prompt.md` (SHA-256) | Verdict |
| --- | --- | --- | --- |
| `runs/track-s/2026-11-03-grader-control` (cases `e3e3de4a…`) | `mistral-large-2512`, temperature 0, seed 1 | `d691edd3…` (draft 6) | **run failed** — no grade |
| `runs/track-s/2026-11-03-grader-control-2` (cases `e3e3de4a…`) | `gemini-3.8-flash`, temperature 0, seed 1 | `d691edd3…` (draft 6) | **pass** |

### `2026-11-03-grader-control` — run failed

The model check passed. The first case was refused with HTTP 403, "This model is not available in
your subscription tier" (`tier_not_allowed`), which is not retried, and the run failed as an
infrastructure error before any grade.

### `2026-11-03-grader-control-2` — pass

The grader on `gemini-3.8-flash`, which describes itself as a thinking model with an output limit of
65,536 tokens. 36 calls, no error or retry, every grade finished with `STOP`; 10,056 of the output
tokens were the model's reasoning. The Gemini API reports no rate-limit headers.

The grader agrees with all 36 verdicts and passes none of the six cases that contradict their slice.
Its `contradicts` flag agrees on 35: it also marks GD5, "a site can launch at most two drones at a
time", as contradicting, where the case marks it as an addition. That errs towards the strict side,
since a contradicting `fact` answer fails the persona on its own. The grader's prompt passes
unrevised and is frozen.

## Judges

| Run | Model | `judge-prompt.md` (SHA-256) | Verdict |
| --- | --- | --- | --- |
| `runs/track-s/2026-11-09-judge-control-gemini-4-argon` (mutants `aa11f7f4…`) | `gemini-4-argon`, temperature 0, seed 1 | `40baece8…` (version 4, draft 2) | **pass** — 18 of 18 exact |
| `runs/track-s/2026-11-09-judge-control-claude-opus-5-5` (mutants `aa11f7f4…`) | `claude-opus-5-5`, effort `high` | `40baece8…` (version 4, draft 2) | **pass** — 18 of 18 exact |

### `2026-11-09-judge-control-gemini-4-argon` and `-claude-opus-5-5` — pass

Both runs completed without error or retry, 18 judgements each, every response a natural stop
(`STOP`, `end_turn`). Every judgement of both judges is exact: every reference requirement has the
coverage its mutant was built with, every item its class, and every reworded item names the
requirement it was reworded from. Both judges report 39 covered on M1, M3 and M4; 31 covered and 8
missing on M2; 33 covered and 6 partial on M5; 4 out-of-scope and 3 technical additions on M4; and
nothing covered on the empty contract M6, in all three repetitions.

The mutants were written with Claude Code, on Claude Opus 5.5, the family of the judge of Gemini
subjects (D-56). Neither judge missed one difference the mutants hold, so the calibration does not
show where either judge's limit lies.
