---
title: "Review rules for system-construction-benchmark"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Review rules for `system-construction-benchmark`

The `repo-routine` extension of `exeris-systems/.github`'s `docs-guardrails-review.md`, applied
**after** its steps and under its severity tags, output format and verdict schema. It adds checks and
raises severities; it lowers nothing and skips nothing. The shared routine judges prose, records,
commits and pull request bodies; this file judges the benchmark instrument those documents describe.

## What this repository is answerable for

A measuring instrument: a contract, an oracle, a harness, a user-story procedure and the records of
their runs. Its results are only as good as two properties — what was measured is exactly what was
published, and the contract does not encode one platform's shape. The policies
[`instrument-integrity`](../.agents/policies/instrument-integrity.md) and
[`contract-neutrality`](../.agents/policies/contract-neutrality.md) are the home of their wording;
the rules below are how a reviewer applies them to a diff.

## Step B — rules of this repository

B1. **A frozen set is not edited in place.** `preregistration/frozen-sets.md` lists every frozen set
    and the paths it contains. A diff that modifies or deletes a file belonging to a frozen set —
    today everything under `trackS/` — without the same pull request declaring a new
    version of that set (the version line of its procedure file and a decision-register entry) →
    `[HARD BLOCK]`. A new version that leaves `frozen-sets.md` without a row for it, to be filled
    once tagged → `[CONTRACT]`.

B2. **Run records are append-only.** A diff that modifies, renames or deletes any existing file under
    `runs/` → `[HARD BLOCK]`. Adding a new run directory is the only permitted change there. A new
    run presented as canonical when an earlier completed run of the same procedure version exists
    → `[HARD BLOCK]`; it is a replication and must say so.

B3. **No credential and no session link.** A string that looks like an API key, token or private
    key in any file, or a `Claude-Session:` trailer or `claude.ai/code/session_` link in a commit
    message or the pull request body → `[HARD BLOCK]`.

B4. **The contract names no technology.** A framework, library, database, broker or vendor name in
    a requirement, the domain profile, the agent brief or a DOD item → `[HARD BLOCK]`. Standard
    protocols and formats at the process boundary (HTTP, OpenAPI, JSON, JWT) and the per-arm
    scoring allowlists are not technology names. A gated requirement without `reachable_without`
    where reachability is in doubt, or one that only a single arm's component can meet →
    `[CONTRACT]`.

B5. **Synchronised artefacts change together.** A change to `trackS/world-brief.md`
    without the matching change to `brief-slices.yaml` and `brief-seeding.md` → `[HARD BLOCK]`. A
    change to a user-visible item of `contract/anti-requirements.md` without the matching change to
    brief §8, or the reverse → `[CONTRACT]`. A parameter value in `system-requirements.yaml` that
    violates its `parameter_constraints` → `[CONTRACT]`.

B6. **Requirement and decision identifiers are stable.** Renumbering or reusing a requirement ID
    (`SR-*`), DOD ID or decision ID (`D-NN`) → `[CONTRACT]`. A removed requirement leaves the
    reason in the decision register.

B7. **An agent is shown only what D-09 allows.** A change that puts oracle checks, mutants,
    reference implementations, `arms.yaml`, the coverage declaration, the neutrality audit, the
    preregistration or sealed change scenarios within reach of a construction agent's input, or
    `brief-seeding.md` within reach of a story-producing role → `[HARD BLOCK]`.

B8. **No human in a run, no silent retry.** A harness or procedure change that lets a person send
    input to an agent mid-run, or that retries anything but an infrastructure error with the same
    input → `[HARD BLOCK]`. A run that changes a prompt, model or parameter and is recorded as a
    retry of an earlier one → `[HARD BLOCK]`.

B9. **An exclusion carries its reason.** An arm, configuration, gate or run left out of a table or a
    matrix without an entry and a reason in the plan's exclusion tables (§5A.6, §9.6) →
    `[CONTRACT]`.

B10. **A correction replaces.** A document or decision that annotates its own history ("amended",
     "an earlier draft said", "corrected") instead of stating the current position → `[DOC DEBT]`.
     The history lives in git and in the decision register's own entries.

## Not checked here

The merge method of a pull request that carries a frozen set (it must be a merge commit, policy
`instrument-integrity`, Frozen sets, rule 2) is decided after the review and is not visible in a diff; the pull
request body states it, and the person merging applies it.
