---
title: "Track S procedure"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: draft
last-verified: 2026-10-22
---

# Track S procedure

The reference for Track S: its instruments, the files of the set, the persona calibration, the tests
of the script, the run record, and the rules every run follows. The commands that run a calibration
are in [`how-to-calibrate-persona.md`](how-to-calibrate-persona.md); each calibration's verdict is in
[`calibration-log.md`](calibration-log.md).

Version: 3 (draft 6)
Decision register: D-45 to D-53. Versions 1 and 2 (the user-story procedure under
`contract/user-stories/`) are frozen at tags `us-procedure-v1` and `us-procedure-v2`; their runs are
Track S pilots (D-46).

## Instruments

| Instrument | Provider | Model | Sees |
| --- | --- | --- | --- |
| Persona — fleet technician, dispatcher, airspace desk | Mistral API | `ministral-8b-2512` (open weights: `mistralai/Ministral-3-8B-Instruct-2512`, Apache 2.0), temperature 0, random seed 1, for both passes | answering: `persona-prompt.md` + its slice of `world-brief.md` (`brief-slices.yaml`); checking: `persona-check-prompt.md` + the same slice, the question and the answer's sentences |
| Grader — of the persona's calibration answers | Gemini API | `gemini-3.8-flash`, temperature 0, random seed 1 | `grader-prompt.md` + the answering role's slice, the question, its kind and `expect`, and the answer |
| Judge, script series | Gemini API | Gemini 3.8 Flash, exact identifier fixed before its calibration | the derived contract + the reference requirements |
| Judge, native series | Mistral API | `mistral-large-2512` (open weights: `mistralai/Mistral-Large-3-675B-Instruct-2512`, Apache 2.0) | the derived contract + the reference requirements |

Instruments are fixed across subjects and calibrated before the first subject. The subjects, the
judge's calibration and the S-naive and S-instructed tasks are added to this procedure before they
run.

## Files of the set

| File | Role in version 3 |
| --- | --- |
| `world-brief.md`, `brief-slices.yaml` | the world and each persona's slice of it |
| `brief-seeding.md` | the brief sentences that are constraints or seeded needs; used to read derived contracts |
| `persona-prompt.md`, `persona-check-prompt.md` | the persona instrument: the answering pass and the check pass |
| `grader-prompt.md`, `grader-control.yaml` | the grader of the persona's calibration and the cases it is calibrated on |
| `persona-control.yaml`, `persona-holdout.yaml` to `persona-holdout-4.yaml` | the persona's calibration questions: the set the prompts are revised against, the held-out sets that decided drafts 3 to 5, and the held-out set that decides draft 6 |
| `interviewer-prompt.md`, `analyst-prompt.md` | the prompts of procedure v2's pilots; not used by version 3, and replaced by subject prompts before the first subject runs |
| `run-track-s.py`, `test_run_track_s.py` | the script and its tests |
| `procedure.md`, `how-to-calibrate-persona.md`, `calibration-log.md` | this reference, the how-to, the calibration record |

## The persona's two passes

The persona answers each question in two passes of the same model. The answering pass writes the
answer from the persona prompt and its slice. The check pass receives the same slice, the question,
and the answer split into numbered sentences, and returns KEEP or DROP for each sentence, with the source of
each sentence it keeps: words copied from the slice, at least four long, or `DONT_KNOW` or
`FEELING`. It never rewrites a sentence. The script keeps a sentence only when the check keeps it
and its source holds: a quote is found in the slice, `DONT_KNOW` marks a sentence that says the
speaker does not know, and `FEELING` is taken on the check's word. The persona's answer is its kept
sentences, in order, and "I don't know." when none is kept. The persona's conversation, and the subject, receive only that answer; the run record keeps
the draft, its sentences and the verdicts as well. A check reply that is not one verdict and source
per sentence fails the run.

## Persona calibration — runs first

Question sets of the same shape hold fixed questions per role, each with what the role's slice
supports (`fact`), a question the slice cannot answer (`outside`), or a question that invites
software design (`no-design`). The script asks each role its questions in one conversation, three
times: `persona-control` asks `persona-control.yaml`, and `persona-holdout` to `persona-holdout-4`
ask the held-out sets.

Each answer is graded against its question's `expect`, each repetition by itself; agreement across
repetitions is not a criterion of its own (D-50). The grader grades, never the author of the
persona's prompts: mode `grade` grades every answer of a completed persona run, from its slice, the
question, its kind and `expect`, into a run of its own. The grader is calibrated first, by mode
`grader-control`, on the 36 cases of `grader-control.yaml`, whose verdicts follow the rules below; it
passes when it agrees with at least 33 of them and passes no case that contradicts its slice. Its
prompt may be revised against those cases, and is frozen before it grades a deciding run.

A `fact` answer passes when it agrees with the
cited unit and adds nothing its slice does not give; an `outside` answer passes with "I don't know"
or a referral its slice supports; a `no-design` answer passes when it describes needs rather than
features or mechanisms. Any answer fails that speaks for another organisation. The grader also
marks an answer that contradicts the slice. The verdict, and every failing answer with the grader's
reason, is recorded in `calibration-log.md`.

The persona's prompts are revised against the control set only. With them frozen, the current
draft's held-out set is run once, and decides: the persona passes when no `fact` answer contradicts its slice and at
least 65 of the 72 answers pass. A persona that fails the held-out set is not revised against it; a
new prompt or model is a new draft, with a new held-out set. The rate-limit headers recorded on every
call show the provider's limits, from which the subject runs are scheduled.

The calibration establishes only that the persona keeps to its slice. It says nothing about how any
subject interviews or derives a contract.

## Tests

`python3 -I trackS/test_run_track_s.py`, run by the `track-s-tests` workflow, checks the script
against a stubbed transport; it needs no network and no key.

## Run record

The output directory is committed unedited:

- `requests/NNNN.json`, `responses/NNNN.json` — every request and response verbatim;
- `calls.jsonl` — per call: role, provider, model, response id, reported model, finish reason, token
  usage, every response header that reports a rate limit, and for an HTTP error its status and body;
- `run.json` — status (`completed` or `failed`), parameters, the model's own description, and the
  SHA-256 of every input;
- the mode's result, e.g. `persona-control.json`.

## Rules

- **No human in the loop.** Nobody reads, edits or steers between calls.
- **Sampling.** A subject runs on the provider's defaults: no temperature or similar setting is
  sent. The persona runs at temperature 0 with random seed 1, sent with every call and recorded in
  `run.json`, so its answers do not depend on a default the provider may change.
- **Errors.** Network failures, timeouts, rate limits and server errors are retried with the same
  request and logged. An exhausted daily or monthly quota fails the run as an infrastructure error
  (program plan §9.1), never as a subject's failure. A response whose finish reason is not a natural
  stop fails the run. A failed run is kept and run again from the start in a new directory.
- **Free tiers.** Data sent on a free tier may be used by the provider for training. The brief and
  every prompt are public; subjects' outputs are published with the run anyway.
