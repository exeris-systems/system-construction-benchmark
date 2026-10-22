# Phase 1 plan — contract, oracle, and calibration

## Goal

Build a small, technology-neutral and externally verifiable benchmark instrument. Phase 1 ends when its oracle detects every approved deliberate defect. It does **not** run agents, compare arms, or claim that the current Exeris application satisfies the final campaign contract.

## Non-goals

- Do not extend the Drone Fleet application for product completeness.
- Do not freeze the expanded flight lifecycle, durable recovery, or frontend as Campaign 1 gates yet.
- Do not expose the current implementation to a future greenfield agent run.
- Do not measure performance, cost, or platform superiority.

## Scope decision

The Phase 1 pilot contract is one vertical slice:

```text
create Drone → request charging → persisted state changes → event is observable
```

Requirements come from `contract/system-requirements.yaml`.

## Deliverables

| Deliverable | Location | Completion condition |
| --- | --- | --- |
| System requirements | `contract/system-requirements.yaml` | Domain language only; no Exeris, Spring, database, or generator names. |
| Pilot DOD | `contract/dod.yaml` | Every gate has provenance, `motivating_arm: none`, `reachable_without`, observable boundary, oracle check, and mutation IDs. |
| API expectation | `contract/expected-api.yaml` | Endpoint behavior, request/response semantics, and errors; not a copied implementation artifact. |
| Event expectation | `contract/expected-events.yaml` | Name, payload semantics, correlation, and after-commit requirement. |
| Domain model | `contract/domain-model.yaml` | Minimal concepts and allowed state transitions. |
| Anti-requirements | `contract/anti-requirements.md` | Explicitly excludes unmeasured production features. |
| Coverage declaration | `contract/coverage-declaration.md` | Per arm: surfaces exercised and explicitly out of scope. |
| Arm declaration | `contract/arms.yaml` | Scope, proximity, external store, and surface maturity are explicit. |
| Contract version | `contract/CONTRACT_VERSION` | Set to `0.1.0-pilot`; any semantic contract change increments it. |
| Oracle protocol | `oracle/` | Black-box checks and an evidence schema. |
| Mutation suite | `mutants/` | Each approved mutation has a reproducible broken target and expected `FAIL`. |
| Neutrality audit | `contract/neutrality-audit.md` | Raw answers of the auditor models, comment-window input, and resolved findings (D-03). |
| Run-artifact contract | `harness/` | A run directory can record all required evidence without a manual spreadsheet. |
| Instrument-cost ledger | `harness/instrument-cost.json` | Token vectors from session logs and a working-day estimate of human time, per category (D-40). |

## Pilot DOD to freeze

This is deliberately a small calibration set. IDs become stable only after review.

| Candidate ID | Observable requirement | Boundaries |
| --- | --- | --- |
| `DOD-DRONE-01` | A valid request creates a drone; retrieval returns the same required state. | HTTP, database |
| `DOD-DRONE-02` | An invalid creation request returns a 4xx response identifying the invalid input. | HTTP |
| `DOD-ACTION-01` | An eligible charging request creates an observable charge-service request; its storage representation is not prescribed. | HTTP, arm adapter |
| `DOD-EVENT-01` | A successful charge request produces exactly one event with a correlation ID and the committed drone state. | HTTP, database, event boundary |
| `DOD-MIGRATION-01` | A fresh database can apply the application schema and serve the above flow. | process, database, HTTP |

The current UI is retained as a manual discovery artifact. It becomes a gate only after an ARIA-only browser check is shown to be stable.

## Oracle design

### Hard boundaries

The oracle may observe only:

- HTTP responses;
- state through an arm-declared, read-only data adapter;
- process lifecycle and exit status;
- an event-consumer boundary or persisted outbox/event-store boundary;
- browser roles and accessible names, if the UI gate is admitted.

It may not inspect source annotations, generated classes, framework tables, logs as the sole proof, or in-process objects.

### Checks

| Check | Purpose | Required evidence |
| --- | --- | --- |
| `check_api` | Create, retrieve, error semantics, action response. | request/response transcript with redacted IDs. |
| `check_data` | Persisted state agrees with the API response. | arm-declared adapter query, validated by mutation. |
| `check_events` | Exactly-once observation, correlation, payload, and post-commit ordering. | shared external webhook, broker consumer, or consumer-side queue record correlated to the request and committed state. |
| `check_migrations` | Fresh schema bootstrap. | isolated database initialization log and schema version. |
| `check_frontend` | Optional, later only. | ARIA-role/name browser trace. |

Every check returns `PASS`, `FAIL`, `UNKNOWN`, or `UNREACHABLE_IN_PARADIGM`. `UNKNOWN` is a failed gate for campaign admission. A combined verdict must retain a machine-readable decomposition of every sub-check rather than report only “E2E failed”.

## Calibration mutations

The first approved pilot suite contains these five defects. Additions require an explicit contract and oracle revision.

| ID | Deliberate defect | Oracle must return |
| --- | --- | --- |
| `M-P1-01` | Accept an invalid creation payload. | `FAIL` from `check_api`. |
| `M-P1-02` | Return success from charge request without persisting its state transition. | `FAIL` from `check_data`. |
| `M-P1-03` | Persist the state transition but emit no event. | `FAIL` from `check_events`. |
| `M-P1-04` | The mutant publishes an event, then deliberately rolls back its state change. | `FAIL` from `check_events`: orphan event has no committed state and no successful HTTP result. |
| `M-P1-05` | No-op target returns success while creating neither a row nor an event. | `FAIL` simultaneously from `check_data` and `check_events`. |

Phase 1 is calibrated only when all five produce `FAIL` and both intact reference targets produce `PASS`. The full campaign mutation set will later add saga, pagination, OpenAPI, tenant-isolation, and browser mutants as their corresponding gates enter the frozen contract.

## Work sequence

1. **Freeze scope.** Decide which neutral business state `DOD-ACTION-01` targets. Write the decision before coding an oracle.
2. **Write the contract.** Create the six contract artifacts above, review for implementation leakage, and assign provenance to every DOD point.
3. **Choose observation adapters.** Each arm declares a read-only state-query adapter; its mapping is harness configuration, not contract schema. Events must cross a shared external boundary (webhook, common broker consumer, or consumer-side queue). An application-private outbox row alone is not proof of external publication.
4. **Implement the oracle.** Begin with API and data checks; add migration and event checks only after their evidence path is deterministic.
5. **Create mutants.** Implement one reproducible broken target per approved mutation. The oracle must fail each one for the intended reason.
6. **Dry-run the intact target repeatedly.** Establish that the same unchanged target does not vary; record `UNKNOWN` and flaky behavior rather than retrying it away.
7. **Run the neutrality audit.** Run the published procedure (D-03) on the DOD alone, without platform names or implementation context, with several auditor models; open the comment window. Publish the raw answers and the decisions.
8. **Freeze the Phase 1 instrument.** Version the contract and oracle, record hashes and environment versions, then create the Phase 2 harness plan.

## Exit criteria

- Every pilot gate is technology-neutral and has provenance, `motivating_arm`, `reachable_without`, a mutation ID, and an external observation path.
- Both intact reference targets — Exeris and Spring vanilla (D-15) — pass every admitted pilot gate.
- All five approved pilot mutations fail the intended oracle check: 5/5 detection.
- Repeated oracle runs against the same unchanged reference produce no unexplained result change.
- `UNKNOWN` is represented in artifacts and treated as non-passing.
- The coverage declaration and neutrality audit are complete.
- The contract, oracle, mutations, and environment record have versions/hashes and are ready to publish before any scored agent run.
- Instrument-building token vectors and human-time estimates are recorded in `harness/instrument-cost.json`.

## Phase 1 decision log

| Decision | Owner | Due before |
| --- | --- | --- |
| Event observation boundary shared by all arms | unassigned | `check_events` implementation |
| Read-only state-query adapter per arm | unassigned | `check_data` implementation |
| Neutrality-audit procedure published (D-03) | arkstack-dev | Contract freeze |
| Whether stable ARIA evidence admits a UI gate | unassigned | Contract freeze |

## Estimated order of magnitude

Treat this as instrument engineering, not application coding: several focused days is realistic. Do not use this estimate as a campaign cost or compare it with an agent arm; instrument cost is reported separately.
