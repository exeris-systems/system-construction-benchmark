---
title: "system-construction-benchmark: a preregistered benchmark of building systems under a fixed contract"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# system-construction-benchmark: a preregistered benchmark of building systems under a fixed contract

The portable entry point for any AI agent working in this repository. It is an index and a safety
boundary: the program is in [`docs/program-plan.md`](docs/program-plan.md), the decisions behind it
in [`docs/decision-register.md`](docs/decision-register.md), and the operating rules for agents in
[`.agents/`](.agents).

## Mission and scope

This repository is a measuring instrument, not an application. It holds the contract a system must
satisfy, the external oracle that judges it, the harness that runs agents against it, the
user-story procedure that grounds the contract, and the records of every run. It measures what it
costs an agent to build and change a system to a fixed, machine-verifiable bar on different
platforms; it does not measure platform performance or decide which stack is better
(program plan §1.2). The contract author is also a competitor, and the instrument is built to make
that visible rather than to hide it.

## Operating contract

Hard constraints. The policies [`instrument-integrity`](.agents/policies/instrument-integrity.md)
and [`contract-neutrality`](.agents/policies/contract-neutrality.md) state them in full; this list
names them so no agent starts without them.

- **Frozen sets are never edited.** Anything under a protected tag (`us-procedure-*`, `prereg-*`,
  `domain-b-*`) changes only as a new version with a new tag and timestamp. Pull requests that carry
  one merge with a merge commit.
- **Run records are committed as written.** Nothing under `runs/` is edited, reformatted or
  deleted. The first completed run of a procedure is canonical.
- **No human in a run.** Scored and procedural runs execute without a person steering; an
  intervention fails a scored run.
- **No technology names in `contract/`**, beyond standard protocols at the process boundary.
- **What an agent is shown is fixed** (D-09): a construction agent sees the agent brief only.
- **No credential in any committed file**, and no session link in a commit message or pull request.

When sources disagree: the decision register, then the program plan, then `.agents/policies/`, then
this file, then `README.md`. A higher source wins; the lower one is a drift to fix.

English for every persisted artefact — documents, code, comments, commit messages, pull requests.
Conversation with the founder happens in Polish.

## Where things are

| Path | What it holds |
| --- | --- |
| `contract/` | domain profile, requirements, anti-requirements, arms |
| `trackS/` | Track S: world brief, persona slices, prompts, control set, `run-track-s.py` (D-45 to D-48) |
| `docs/` | program plan, Phase 1 plan, decision register |
| `preregistration/` | frozen sets with their timestamps; hypotheses before a campaign |
| `oracle/`, `mutants/`, `harness/`, `prompts/` | the instrument as it is built |
| `runs/` | raw run records, committed unedited |
| `tools/` | repository checks the review reads (`repo-checks`): append-only runs, frozen sets, credentials, agent material |

## `.agents/` — the canonical agent material

[`.agents/manifest.yaml`](.agents/manifest.yaml) composes this repository's policies with the
organisation bundle `exeris-agents`, pinned and vendored under `.agents/vendor/` (never edited).
The repository's own review rules — the `repo-routine` extension of the organisation review — are
in [`docs/repo-review-rules.md`](docs/repo-review-rules.md).

## Verification and reporting

A change to Track S reruns `python3 -I trackS/run-track-s.py persona-control --persona-model M
--dry-run`. A change to the agent material reruns `agents_file_check.py`,
`agents_render.py --check` and `agents_bundle.py verify` from `exeris-systems/exeris-agents`.

Report what ran and its result, and name what did not run as not run — silence is not a pass.

## Provider adapters

[`CLAUDE.md`](CLAUDE.md) is a thin pointer to this file for clients that look for it, and states no
rule of its own. Adapters are generated from `.agents/` by the shared renderer and never edited.
