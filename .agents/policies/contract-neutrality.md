---
title: "Policy — neutrality of the contract"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Policy — neutrality of the contract

The contract author is a competitor (program plan §0, rule 3). These constraints keep the contract
from encoding one platform's shape.

1. **No technology names in the contract.** `contract/` describes behaviour only. Standard
   protocols and formats at the process boundary — HTTP, OpenAPI, JSON, JWT — are not technology
   names (program plan §3.3). The only other exception is the per-arm allowlists used to score
   wrong-stack substitution.
2. **Every gated requirement is reachable without a single-arm component.** `reachable_without`
   lists the component classes a requirement must not need; a requirement that only one arm can
   meet is a platform requirement and leaves the gates (§3.2).
3. **No hidden scope.** A property not in the requirements is not a `PASS` criterion. Anything a
   reader could take as required but is not belongs in `contract/anti-requirements.md`; a
   user-visible anti-requirement is mirrored in brief §8 (D-47).
4. **Synchronised artefacts change together.** A change to `world-brief.md` changes
   `brief-slices.yaml` and `brief-seeding.md` in the same pull request, and is a new frozen
   version of the user-story procedure. A change to the requirements' parameters respects
   `parameter_constraints`.
5. **An excluded arm or configuration is listed with its reason** (§0, rule 4; §5A.6; §9.6). An
   exclusion without an entry is an unreported result.
6. **The oracle observes only at the process boundary.** A check that inspects classes, tables,
   annotations or in-process state is not a check of this benchmark (§4.1).
