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

Version: 3 (draft 3)
Decision register: D-45 to D-50. Versions 1 and 2 (the user-story procedure under
`contract/user-stories/`) are frozen at tags `us-procedure-v1` and `us-procedure-v2`; their runs are
Track S pilots (D-46).

## Instruments

| Instrument | Provider | Model | Sees |
| --- | --- | --- | --- |
| Persona — fleet technician, dispatcher, airspace desk | Mistral API | `ministral-8b-2512` (open weights: `mistralai/Ministral-3-8B-Instruct-2512`, Apache 2.0) | `persona-prompt.md` + its slice of `world-brief.md` (`brief-slices.yaml`) |
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
| `persona-prompt.md` | the persona instrument |
| `persona-control.yaml`, `persona-holdout.yaml` | the persona's calibration questions: the set the prompt is revised against, and the held-out set that decides |
| `interviewer-prompt.md`, `analyst-prompt.md` | the prompts of procedure v2's pilots; not used by version 3, and replaced by subject prompts before the first subject runs |
| `run-track-s.py`, `test_run_track_s.py` | the script and its tests |
| `procedure.md`, `how-to-calibrate-persona.md`, `calibration-log.md` | this reference, the how-to, the calibration record |

## Persona calibration — runs first

Two question sets of the same shape hold fixed questions per role, each with what the role's slice
supports (`fact`), a question the slice cannot answer (`outside`), or a question that invites
software design (`no-design`). The script asks each role its questions in one conversation, three
times: `persona-control` asks `persona-control.yaml`, `persona-holdout` asks `persona-holdout.yaml`.

Each answer is graded against its question's `expect`. A `fact` answer passes when it agrees with the
cited unit and adds nothing its slice does not give; an `outside` answer passes with "I don't know"
or a referral its slice supports; a `no-design` answer passes when it describes needs rather than
features or mechanisms. The verdict, and every failing answer, is recorded in `calibration-log.md`.

The persona prompt is revised against the control set only. With the prompt frozen, the held-out set
is run once, and decides: the persona passes when no `fact` answer contradicts its slice and at
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
- **Provider defaults.** No temperature or similar setting is sent.
- **Errors.** Network failures, timeouts, rate limits and server errors are retried with the same
  request and logged. An exhausted daily or monthly quota fails the run as an infrastructure error
  (program plan §9.1), never as a subject's failure. A response whose finish reason is not a natural
  stop fails the run. A failed run is kept and run again from the start in a new directory.
- **Free tiers.** Data sent on a free tier may be used by the provider for training. The brief and
  every prompt are public; subjects' outputs are published with the run anyway.
