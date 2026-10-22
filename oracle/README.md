# Oracle

External checks and their evidence format. The design — hard observation boundaries, checks, and the four verdict states — is in the [Phase 1 plan](../docs/phase-1-plan.md#oracle-design).

Every check observes only across a process boundary and returns `PASS`, `FAIL`, `UNKNOWN`, or `UNREACHABLE_IN_PARADIGM`; `UNKNOWN` is non-passing. Every evidence artifact includes a timestamp, contract version, and the command or scenario used.
