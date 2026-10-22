# System Construction Benchmark

Research-program repository for comparing the cost of building and evolving a system under a fixed, externally verifiable contract.

Status: **Phase 1 — contract and oracle**. Do not start scored agent campaigns, publish arm comparisons, or treat results as benchmark findings before the Phase 1–3 exit conditions are met.

## Working principle

The contract, oracle, and harness are part of the instrument under study. Every `PASS` requires evidence observable at a process boundary; `UNKNOWN` is a non-passing result. The oracle will be calibrated against mutants before the first agent run.

## Repository layout

| Directory | Purpose |
| --- | --- |
| `contract/` | Versioned domain contract, DOD, and scope declarations. |
| `oracle/` | External checks and their evidence format. |
| `mutants/` | Deliberately broken implementations for oracle calibration. |
| `harness/` | Run preparation, launch, collection, and archival. |
| `prompts/` | Versioned L0–L3 prompts. |
| `preregistration/` | Hypotheses, arms, abort policy, and decisions published before a campaign. |
| `runs/` | Local run artifacts; never a substitute for the contract or oracle. |
| `docs/` | [Program plan](docs/program-plan.md), phase plans, and the decision register. |

## Immediate milestone

Phase 1: complete the campaign contract, build the external oracle, and calibrate it against deliberate mutants and two reference implementations — see the [Phase 1 plan](docs/phase-1-plan.md). Tokens and an estimate of human time spent on the instrument are recorded in `harness/instrument-cost.json`.

## Condition for progressing

The agent campaign may begin only after 100% detection of the approved mutant set, a neutrality audit, and publication of the preregistration.
