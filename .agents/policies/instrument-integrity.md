---
title: "Policy — integrity of the benchmark instrument"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Policy — integrity of the benchmark instrument

Not negotiable. The contract, the oracle, the harness and the user-story procedure are a second
system whose defects become the benchmark's results (program plan §0). These constraints keep what
was measured identical to what was published.

## Frozen sets

1. **A frozen set is never edited.** Files that belong to a set frozen under a protected tag
   (`us-procedure-*`, `prereg-*`, `domain-b-*`; program plan §12.2, decision register D-42) change
   only as a new version of the set, with a new tag and a new independent timestamp. An edit in
   place silently changes what an earlier run used.
2. **A pull request that carries a frozen set is merged with a merge commit.** Squash and rebase
   rewrite commits, and the tag would point outside the history of `main`.
3. **Every frozen set has an entry in `preregistration/frozen-sets.md`**: tag, commit, contents,
   and the independent timestamp with its identifier.

## Raw records

1. **A run record is committed exactly as the tool wrote it.** Nothing under `runs/` is edited,
   reformatted, trimmed or deleted after it is written. A run that failed stays, marked failed by
   its own record.
2. **The first completed run of a procedure is canonical.** A later run is replication: it is
   published, never substituted. A procedure changes only by a new frozen version, before its run.
3. **No credential reaches a record.** API keys come from the environment and never enter
   `runs/`, `harness/` or any committed file.

## Runs

1. **No human in a scored or procedural run.** The only feedback an agent receives in a scored run
   is the oracle report after a "done" declaration (D-10); any human message makes the run a
   `FAIL` annotated `intervened` (D-41). A procedure run executes end to end without a person
   relaying, editing or steering between calls.
2. **Infrastructure errors are retried with the same input; nothing else is.** A changed prompt,
   model or parameter is a new configuration, not a retry.

## What an agent is shown

1. **A construction agent sees the agent brief and nothing else of the instrument** (D-09):
   never the oracle, mutants, reference implementations, `arms.yaml`, the coverage declaration,
   the neutrality audit, the preregistration, or the sealed change scenarios.
2. **The seeding declaration never reaches a persona or a Track S subject** (D-47), and a model
   that serves as a Track S instrument is never a Track S subject (D-48).
