---
title: "Track S procedure"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: draft
last-verified: 2026-11-09
---

# Track S procedure

The reference for Track S: its instruments, the files of the set, the persona calibration, the tests
of the script, the run record, and the rules every run follows. The commands that run a calibration
are in [`how-to-calibrate-persona.md`](how-to-calibrate-persona.md); each calibration's verdict is in
[`calibration-log.md`](calibration-log.md).

Version: 6 (draft 2)
Decision register: D-45 to D-60. Version 5, whose instruments, subjects and calibration this version
keeps, is frozen at tag `us-procedure-v5`; version 4, at `us-procedure-v4`; version 3, at `us-procedure-v3`. Versions 1 and 2 (the user-story procedure under
`contract/user-stories/`) are frozen at tags `us-procedure-v1` and `us-procedure-v2`; their runs are
Track S pilots (D-46).

## Instruments

| Instrument | Provider | Model | Sees |
| --- | --- | --- | --- |
| Persona — fleet technician, dispatcher, airspace desk | Gemini API | `gemini-3.5-flash-lite`, temperature 0, random seed 1; answering pass only | answering: `persona-prompt.md` + its slice of `world-brief.md` (`brief-slices.yaml`); checking: `persona-check-prompt.md` + the same slice, the question and the answer's sentences |
| Grader — of the persona's calibration answers | Gemini API | `gemini-3.8-flash`, temperature 0, random seed 1 | `grader-prompt.md` + the answering role's slice, the question, its kind and `expect`, and the answer |
| Judge of a Claude subject, both series | Gemini API | `gemini-4-argon`, temperature 0, random seed 1 | `judge-prompt.md` + the requirements and parameters of `contract/system-requirements.yaml` + the anti-requirements of `contract/anti-requirements.md`, and the derived contract |
| Judge of a Gemini subject, both series | Anthropic API | `claude-opus-5-5`, effort `high`; the API takes no temperature or seed | the same |

Instruments are fixed across subjects and calibrated before the first subject. Each subject is judged by the other vendor; in the script series each contract is also judged, unscored, by the judge of the subject's own family, and the report gives how often the two agree (D-55). The subjects are
those of D-55, and their S-naive and S-instructed tasks are set out under Subjects.

## Files of the set

| File | Role in version 6 |
| --- | --- |
| `world-brief.md`, `brief-slices.yaml` | the world and each persona's slice of it |
| `brief-seeding.md` | the brief sentences that are constraints or seeded needs; used to read derived contracts |
| `persona-prompt.md`, `persona-check-prompt.md` | the persona instrument: the answering pass and the check pass |
| `grader-prompt.md`, `grader-control.yaml` | the grader of the persona's calibration and the cases it is calibrated on |
| `judge-prompt.md`, `judge-control.yaml` | the judge, and the mutant contracts it is calibrated on; the same prompt judges the brief for the ceiling |
| `follow-up-prompt.md`, `follow-up-control.yaml` | the judges as follow-up classifiers, and the labelled pairs they are calibrated on |
| `persona-control.yaml`, `persona-holdout.yaml` to `persona-holdout-5.yaml` | the persona's calibration questions: the set the prompts are revised against, the held-out sets that decided drafts 3 to 6, and the held-out set that decides draft 7 |
| `subject-naive-prompt.md` | the subject in S-naive: the client's request, brief §1, the roles and the channel to them |
| `subject-interviewer-prompt.md`, `subject-analyst-prompt.md` | the subject in S-instructed: as interviewer of one role, then as analyst of the three transcripts |
| `run-track-s.py`, `test_run_track_s.py` | the script and its tests |
| `procedure.md`, `how-to-calibrate-persona.md`, `how-to-run-subjects.md`, `calibration-log.md` | this reference, the two how-tos, the calibration record |

## The persona's check pass

The persona answers each question in one pass. A check pass was built for drafts 5 and 6 and is
kept in the script behind `--persona-check`; on `gemini-3.5-flash-lite` it lowers the graded
control run, and the persona runs without it (D-53). With it, each answer takes two passes of the
same model. The answering pass writes the
answer from the persona prompt and its slice. The check pass receives the same slice, the question,
and the answer split into numbered sentences, and returns KEEP or DROP for each sentence, with the source of
each sentence it keeps: words copied from the slice, at least four long, or `DONT_KNOW` or
`FEELING`. It never rewrites a sentence. The script keeps a sentence only when the check keeps it
and its source holds: a quote is found in the slice, `DONT_KNOW` marks a sentence that says the
speaker does not know, and `FEELING` is taken on the check's word. The persona's answer is its kept
sentences, in order, and "I don't know." when none is kept. The persona's conversation, and the subject, receive only that answer; the run record keeps
the draft, its sentences and the verdicts as well. A check reply that is not one verdict and source
per sentence is asked for once more, with the same request; a second such reply fails the run.

## Persona calibration — runs first

Question sets of the same shape hold fixed questions per role, each with what the role's slice
supports (`fact`), a question the slice cannot answer (`outside`), or a question that invites
software design (`no-design`). The script asks each role its questions in one conversation, three
times: `persona-control` asks `persona-control.yaml`, and `persona-holdout` to `persona-holdout-5`
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

## Judge calibration — before any subject

A derived contract is a list of items, each with an `id` and one `requirement`, in YAML; the subject
prompts ask for that shape (D-56). The judge receives `judge-prompt.md` with the reference
requirements and their parameters from `contract/system-requirements.yaml`, the user-visible and the
technical anti-requirements of `contract/anti-requirements.md`, and the contract. It returns, for
each reference requirement, `covered`, `partial` or `missing`, with the items that state its
obligations, and for each item its class: `reference`, with the requirements it states, or
`user_visible`, `technical` or `other`. A reply that does not list every requirement and every item
exactly once fails the run; it is never asked for again, since a second draw on the same contract
could replace a judgement the calibration counts.

From one judgement: `derived_recall` is the covered requirements over all of them, partial ones
reported apart and never counted in it; `derived_precision` is the `reference` items over every item
that is not `technical`; `out_of_scope_additions` is the number of `user_visible` items.

Mode `judge-control` builds six contracts from `judge-control.yaml`: every reference requirement
reworded (M1); eight of them removed (M2); six invented items added, two of which state nothing
checkable (M3); four user-visible and three technical anti-requirements added (M4); six items with
one obligation left out (M5); and the empty contract (M6). Items are renumbered in their final
order. Each contract is judged three times, 18 judgements in all. A judge passes when every one of
them gives every requirement the coverage its contract was built with, every item its class, and
every reworded item the requirement it was reworded from; a single difference fails it. Each judge
is calibrated on its own, and its prompt is frozen before it judges a subject; a revision is a new
draft. Draft 3 records both judges passing, 18 of 18 judgements exact, on the prompt and mutants of
draft 2, which it leaves unchanged (`calibration-log.md`).

## Subjects — after the instruments

A subject is the model under test, run on its provider's defaults (Rules). It receives brief §1 and
the role names (D-47), never a slice, and writes the requirements as a derived contract in the shape
of D-56 (D-57).

**S-naive**, in both series, is one conversation with `subject-naive-prompt.md` as its system
prompt, opened by the turn "Begin." A message that is exactly one line, `ASK <role>: <question>`, with `<role>` one of
`technician`, `dispatcher` or `desk`, is a question: it goes to that role's persona, which keeps one
conversation for the whole run, and the persona's answer is the subject's next turn. A question that
names no such role is answered with the list of roles, and counts. The answer to the 90th question
also tells the subject it can ask no more and asks for the requirements. The first message that is
not a question, or any message after that answer, is the subject's requirements, and ends the run. `elicitation_initiated` is whether a
question came before it, and `turns_before_first_artifact` is the number of questions before it. In
the native series the harness's `ask_user(role, question)` tool takes the place of the `ASK` line:
the prompt's sentence that describes the line reads instead "You can reach one person in each role
with the `ask_user` tool, giving `role`, one of `technician`, `dispatcher` or `desk`, and
`question`; their answer comes back to you."

**S-instructed**, in the script series, is three interviews and an analysis. Each interview is a
conversation between the subject, with `subject-interviewer-prompt.md`, and one role's persona, in
the order technician, dispatcher, desk, opened by the turn "The interviewee is ready. Ask your first
question." Every message of the subject is a question; an interview ends when a message has
`END OF INTERVIEW` on a line of its own, or after 30 questions. A new session of the same subject,
with `subject-analyst-prompt.md` holding the three transcripts and nothing else, is given the turn
"Write the requirements." and writes them. `questions_per_interview` is read from the transcripts.

**Follow-ups.** A question is a follow-up when it asks about something the same role said in the
answer just before it; in S-naive that is the role's previous answer, whatever was asked of the
other roles in between. `follow_up_ratio` is the follow-ups over every question after a role's
first, in both variants. Mode `follow-up` sends a completed subject run's pairs, one call per role,
to a judge with `follow-up-prompt.md`, and records each question's label; as for the contract, the
judge of the other vendor scores and the judge of the subject's own family is recorded unscored
(D-59).

**The contract** is read from the requirements message as a YAML list: the items of the message's
`yaml` block when it has one, and of the whole message otherwise. Each entry with an `id` and a
`requirement` is an item. A message from which no item can be read is the empty contract, recorded
as unreadable, never repaired or asked for again. The judges judge exactly the items read, numbered
`DR-01`, `DR-02`, … in their order, as in the calibration; the numbers the subject gave are kept
beside them. Mode `judge` judges one completed subject run with one judge into a run of its own. Its
judgement is scored when the judge's provider is not the subject's, and otherwise recorded as the
unscored judgement of the subject's own family (D-55).

Every turn the script itself writes to a subject is quoted above, with the reply to a question that
names no role, "There is no such role. The roles are technician, dispatcher and desk.", and the
sentence added to the 90th answer, "You cannot ask any more questions. Write the requirements now."
A subject model's turns go back to it as it returned them, its thinking blocks included (D-58).

## Follow-up calibration — before any subject

Mode `follow-up-control` gives each judge the four conversations of `follow-up-control.yaml`, 40
pairs of an answer and the question after it, each labelled a follow-up or not, three times. A judge
passes as classifier when it agrees with at least 37 of the 40 labels in every repetition. A reply
that does not label every question exactly once fails the run. The prompt is frozen before it
classifies a subject's questions. Draft 4 records both judges passing as classifiers, each with 40
of 40 in every repetition, on the prompt and pairs of draft 3, which it leaves unchanged
(`calibration-log.md`).

## Ceiling — before the subjects are compared

Some reference requirements cannot be derived from the brief (D-45). Mode `ceiling` estimates which:
it gives a judge `judge-prompt.md`, unchanged, with the whole of `world-brief.md` as the contract, each
unit of the brief (a paragraph or a bullet, as `brief-slices.yaml` numbers them) one item, numbered
`DR-01`, `DR-02`, … in the brief's order. Every unit reaches at least one persona, so the brief is
everything a subject can learn. A requirement the brief covers is one a subject can derive in full; a
partial one, in part; a missing one, not at all. Each judge of D-55 judges the brief three times; a
reply that does not list every requirement and every unit exactly once fails the run (D-60).

The ceiling is reported beside every `derived_recall`: the covered requirements of each judgement of
the brief, and how many requirements kept one coverage in all three. It is never used to rescale a
score. It reads no subject run, and no subject run reads it.

Draft 2 records both judges' judgements of the brief: neither finds a reference requirement the brief
covers, and they give 1 to 12 a partial coverage. The judge prompt counts only what the service must
or must not do, and the brief describes the users' world, so the method gives a lower bound on what a
subject can derive, not the ceiling (`calibration-log.md`, D-60). The instruments of draft 1 are
unchanged.

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
  sent. The persona, the grader and the Gemini judge run at temperature 0 with random seed 1, and
  the Anthropic judge at effort `high`, sent with every call and recorded in `run.json`, so their
  answers do not depend on a default the provider may change.
- **Errors.** Network failures, timeouts, rate limits and server errors are retried with the same
  request and logged. An exhausted daily or monthly quota fails the run as an infrastructure error
  (program plan §9.1), never as a subject's failure. A response whose finish reason is not a natural
  stop fails the run. A failed run is kept and run again from the start in a new directory.
- **Free tiers.** Data sent on a free tier may be used by the provider for training. The brief and
  every prompt are public; subjects' outputs are published with the run anyway.
