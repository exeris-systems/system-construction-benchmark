---
title: "Phase 1 plan — contract, oracle, and calibration"
type: methodology
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Phase 1 plan — contract, oracle, and calibration

## Goal

Build the instrument that every later phase measures with: a frozen-ready campaign contract, an
external oracle, the simulator and event sink it observes through, and a mutation suite it catches in
full, calibrated against two independent reference implementations. Phase 1 runs no scored agent and
compares no arms (program plan §14).

## Exit criteria

- The contract artifacts of program plan §3.1 exist, with every entity, field, action, endpoint and
  event named (D-14), and every gated requirement carrying `rationale`, `motivating_arm`,
  `reachable_without`, an oracle check and mutation IDs (§3.2, D-46).
- The agent brief is rendered from `contract/`, never written by hand, and hashed (§3.11, D-09).
- The simulator and the event sink are versioned, and their control scenarios give the same result
  on both reference implementations (§13, D-17, D-18).
- The oracle returns `PASS` on every in-scope gate of both reference implementations — Exeris and
  Spring vanilla — and detects 100% of the approved mutants (§4.4, §4.5, D-15).
- Repeated oracle runs against an unchanged reference produce no unexplained change; time-dependent
  gates and UI gates have a measured flakiness, and any above 5% is moved to the descriptive section
  (§3.8, D-05, D-20).
- The coverage declaration and `arms.yaml` are complete, and the neutrality audit has run under its
  published procedure with its comment window closed (§3.4, §3.9, D-03).
- Instrument cost is recorded per category in `harness/instrument-cost.json` (§12.3, D-40).

## Done

| Artefact | State |
| --- | --- |
| `contract/domain-profile.md` | tenancy, autonomy, actors and channels, telemetry order, airspace graph, slots, scale, time, regulatory provenance |
| `contract/system-requirements.yaml` | 39 requirements with parameters, parameter constraints and vocabulary |
| `contract/anti-requirements.md` | user-visible and technical items, synchronised with brief §8 |

Track S — requirements elicitation measured per model — runs in parallel and does not feed the
contract (D-45, D-46).

## Work, in dependency order

1. **Name the domain and its boundary.** `domain-model.yaml` (entities, fields, actions, states —
   the vocabulary of the requirements), `expected-api.yaml` (what the system exposes),
   `external-api.yaml` (drone commands, charge-service requests, the event sink, with idempotency
   keys), and `expected-events.yaml` (event names and payloads, delivered by webhook) (§3.1, D-14,
   D-17, D-18).
2. **Write the DOD.** `dod.yaml` from the requirements, one behaviour per gate (§4.1 rule 4), each
   with an authored `rationale` (D-46), UI gates included (D-44), and `failure-scenarios.yaml`
   including REC-1/2/3 (§3.7).
3. **Render the agent brief.** A render step from `contract/` into `contract/agent-brief/`, hashed,
   carrying only what D-09 allows.
4. **Build the simulator and the event sink.** Drones, charging service, and readiness, waypoint and
   arrival sources as one versioned component, with control scenarios whose result is
   arm-independent by construction (D-17). The sink deduplicates by `eventId` and queries the API on
   receipt, which makes publication before commit observable (D-18).
5. **Build the oracle, gate group by gate group**, each check observing only at the process boundary
   and publishing the distribution behind an aggregate verdict (§4.1): registration, validation and
   query; tenancy and access; telemetry and connectivity; charging; missions, routing and airspace;
   durable execution and recovery; events and idempotency.
6. **Write the mutation suite** for the gates that exist: M-01 to M-19 where their gate is in the
   contract, each a reproducible broken build with the check that must fail it (§4.5).
7. **Build the two reference implementations** — Exeris and Spring vanilla — from the contract,
   agent-built if convenient; they are instrument, never shown to a scored run, and implement the
   construction contract only (D-15).
8. **Calibrate.** Both references pass; every mutant is caught for its intended reason; repeated runs
   are stable; the flakiness trials of D-05 and D-20 are recorded.
9. **Declare coverage and arms**, run the neutrality audit under its published procedure, and open
   the comment window (D-03).
10. **Version the contract** (`CONTRACT_VERSION` 1.0.0) and hand over to Phase 2. The contract is
    frozen with the preregistration in Phase 3 (§12.2).

## Out of scope

Agent runs of any kind, arm comparison, Domain B (its contract is frozen in Campaign 1's
preregistration, D-07), and runtime measurement.
