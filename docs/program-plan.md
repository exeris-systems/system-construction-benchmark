# System Construction Benchmark — program plan

Version: **1.0**
Date: 2026-10-22
Status: **Phase 1 — contract and oracle.** No scored run before the Phase 1–3 exit conditions are met and the preregistration is published.

Decisions that shape this plan, including the ones still open, are recorded in the [decision register](decision-register.md). This document states the current design; the register records why.

---

## 0. Governing principle

> The instrument is not an invisible observer. The contract, the oracle, and the harness are a second system, with their own defects and their own bias. The program measures them explicitly before it measures anything else.

Rules that follow:

1. **Fail closed.** A gate the instrument cannot judge reliably yields `UNKNOWN`, and `UNKNOWN` counts as `FAIL`.
2. **Calibrate before measuring.** An oracle that has never returned `FAIL` on a known-broken build is unvalidated, and its `PASS` is not a result.
3. **The contract author is a competitor.** Every contract item needs an explicit provenance and passes a neutrality audit.
4. **An excluded arm is a decision, not an omission.** Every arm considered and rejected is listed in §5A.6 with its reason. Silently leaving out a competitor is treated as an unreported result.

Rule 4 exists because the arms that threaten the thesis most are also the easiest to dismiss in one sentence.

---

## 1. Goal, scope, and explicit limits

### 1.1 Research question

What does it cost to bring a system to a fixed, machine-verifiable level of correctness and completeness — depending on the platform, the agent's level of knowledge about the platform, and the model class — and what does it cost afterwards to change one domain decision?

### 1.2 What this benchmark does NOT measure

```text
NOT requirements discovery, scope negotiation, or domain design in the construction track
    (contract derivation is measured separately, platform-independently — Track S, §6.4).
NOT code quality beyond what the oracle checks.
NOT platform performance (the code is written by the agent — §7.6).
NOT production readiness.
NOT "which stack is better".
NOT the whole surface of any platform (§3.9).
```

### 1.3 A side effect that must be named

Everything the oracle does not check is optimised downwards by the agent. When every arm passes the DOD at 100%, the only thing compared is the cost of reaching the same minimal bar. The partial counterweight is the change benchmark (§7.5): a hollowed-out implementation is expensive to maintain. It is the only control on unspecified quality in the program.

---

## 2. Measurement axes

```text
                 SYSTEM CONSTRUCTION BENCHMARK

                       ┌───────────────┐
                       │   CONTRACT    │
                       │   + ORACLE    │
                       └───────┬───────┘
                               │
        ┌──────────┬───────────┼───────────┬──────────┐
        ▼          ▼           ▼           ▼          ▼
     Build      Evolve      Operate    Reliability   Specify
   greenfield   domain      runtime    false-DONE    Track S
                change      + infra                  (model only)
        └──────────┴───────────┼───────────┴──────────┘
                               ▼
                       VERIFY / GATE / REPORT
```

| Axis | What it measures | Status |
|---|---|---|
| **Construction cost** | USD, time, turns, tool calls, tokens (broken down) | gated |
| **Evolution cost** | cost of one domain change + regressions | gated |
| **Runtime cost** | CPU, RSS, IO, startup, latency | **descriptive_only** |
| **Operational complexity** | processes, containers, brokers, coordinators | gated (structurally) |
| **Agent reliability** | false-DONE rate, first-pass gap, self-correction | gated |
| **Specification** | contract derivation from narrative user stories | model only, no arms (§6.4) |

A single construction run has one of four outcomes:

```text
outcome ∈ {
  PASS_ON_STACK,           # DOD met, on the intended technology
  PASS_OFF_STACK,          # DOD met, the agent used another stack (§7.4)
  FAIL,                    # including abort, timeout, budget exceeded
  UNREACHABLE_IN_PARADIGM  # gate outside the arm's paradigm (§5A.2)
}
```

---

## 3. Contract

### 3.1 Structure

```text
contract/
  CONTRACT_VERSION            # semver; a change ⇒ new campaignId
  domain-profile.md           # tenancy, autonomy, actors, airspace model, scale, time, provenance
  system-requirements.yaml    # what the system does (domain language)
  dod.yaml                    # what is gated and how
  domain-model.yaml           # entities, fields, actions, states — names included
  expected-api.yaml           # OpenAPI 3.x — what the system exposes
  external-api.yaml           # what the system calls: drone commands, charge service, event sink
  expected-events.yaml        # delivered by HTTP webhook to the event sink
  failure-scenarios.yaml
  change-scenarios.yaml.age   # ENCRYPTED until the construction phase ends (§7.5)
  anti-requirements.md
  coverage-declaration.md     # §3.9 — which surface of each platform is touched
  neutrality-audit.md
  abort-policy.yaml
  arms.yaml                   # §5A
  agent-brief/                # GENERATED agent-facing projection (§3.11); never edited by hand
```

Names of entities, fields, actions, endpoints, and events are contract content. They are fixed in `domain-model.yaml`, `expected-api.yaml`, and `expected-events.yaml`, and the agent receives them rather than inventing them.

### 3.2 DOD item format

```yaml
- id: DOD-SAGA-03
  requirement: >
    A workflow started before the process stops resumes after restart from the
    last durable point and finishes with the same final result.
  provenance: "US-17 — a dispatcher dispatches a mission; the process restarts mid-flight"
  motivating_arm: none          # none | exeris | spring | jhipster | ...
  observable_via: [http, db, process_signal]
  gate: true
  oracle_check: check_saga_recovery
  mutation_tests: [M-02, M-03]
  reachable_without: [graph_engine, event_store, external_orchestrator]
```

**Gating rule:** an item without `provenance` and without an assigned mutation test is not a gate.

**Neutrality rule:** an item with `motivating_arm != none` needs a domain justification or it is dropped.

**Reachability rule:** `reachable_without` lists the component classes WITHOUT which the requirement must still be satisfiable. An item that cannot be met without a component present in only one arm is a platform requirement disguised as a domain one, and it leaves the gates. Practical test: *can this be done with a recursive CTE in PostgreSQL?* If yes, the requirement is fair. If it needs a graph engine, it is biased.

### 3.3 No implementation leakage

Technology names do not appear in the contract. It describes behaviour only.

```text
❌  "use Temporal"
✅  "the workflow must survive a process restart and continue from the last durable point"
```

The only allowed exception: per-arm import/annotation allowlists used to compute WSS (§7.4). That is a scoring rule, not a requirement.

Standard protocols and formats at the process boundary — HTTP, OpenAPI, JSON, JWT — are not implementation leakage. They define the boundary the oracle observes, not how the system behind it is built.

### 3.4 Neutrality audit

Before freezing, the DOD alone (without Exeris context and without platform names) is audited with one question: *which class of platform is favoured here, and how can you tell?*

The audit is reproducible rather than independent:

- the procedure — prompt, models, exact input — is published in the preregistration before the audit result is seen;
- several auditor models, preferably from different vendors, run it; their raw answers are published in full;
- before the contract freezes, a public comment window with a fixed deadline is open to anyone, including people who have reviewed earlier benchmark reports.

The result, the raw answers, and the decisions taken are published as `neutrality-audit.md`. Every report states: *"The neutrality audit was run by models configured by the contract author according to a published procedure; it is not an independent audit."*

### 3.5 Anti-requirements

Listed in `contract/anti-requirements.md`, split into user-visible items (kept in sync with `contract/user-stories/world-brief.md` §8) and technical items. No other list is authoritative.

### 3.6 Gated scope

| Area | Gated | Notes |
|---|---|---|
| Domain model | yes | entities, relations, constraints, enumerations, lifecycle |
| CRUD | yes | |
| Query | yes | filtering, sorting, pagination (including page boundaries) |
| Actions | yes | all domain actions |
| Validation | yes | valid/invalid payload + error semantics |
| API | yes | conformance with `expected-api.yaml` |
| OpenAPI | yes | separate gate — §7.7 |
| Events | yes | declaration, emission, payload, correlation, ordering relative to commit |
| Persistence | yes | fresh install, schema, seed |
| Migration | yes | separate gate — §7.7 |
| Durable execution | yes | behaviourally only — §3.7 |
| Security | yes | if in the requirements: authn/authz, tenant isolation |
| Frontend | conditionally | accessible roles and names only — §3.8 |
| **Graph queries** | **conditionally** | only if they pass the reachability rule — §3.9 |

### 3.7 Durable execution — behaviourally only

```text
start saga
→ checkpoint
→ kill the process (SIGKILL, not a graceful shutdown)
→ restart
→ resume from the last durable point
→ complete with the same result
```

and separately failure → compensation, and long-running:

```text
start → wait → kill the process → restart → external event → resume → complete
```

Checking for the presence of classes, tables, or annotations is forbidden.

The scenario must distinguish a pre-dispatch state from a state parked on an external event; otherwise the two collapse into one verdict. A harness that delivers the external event **at most once** makes parked sagas unrecoverable by construction, on every engine — and then the result measures the harness policy, not the engine.

```yaml
recovery_scenarios:
  - id: REC-1
    pre_crash_state: pre_dispatch     # work in progress, before the external event is sent
    external_event_redelivery: n/a
  - id: REC-2
    pre_crash_state: parked_on_event
    external_event_redelivery: true   # the event IS redelivered after restart
  - id: REC-3
    pre_crash_state: parked_on_event
    external_event_redelivery: false  # control: unrecoverable by construction on EVERY arm
```

REC-3 must give the same result on all arms. If it does not, the defect is in the harness. A census of state before and after the kill is part of the gate artifact, not an option.

### 3.8 Frontend

Accessible roles and names only (ARIA / accessible name). Requiring `data-testid` would be implementation leakage.

```yaml
- id: DOD-UI-04
  requirement: >
    A drone list view allows filtering by status; after a drone's status is
    changed through the API, the list updates without a page reload within ≤2 s.
  observable_via: [browser_aria]
  selector_policy: accessible_role_and_name_only
  gate: true
```

**Exit rule:** if the frontend gates prove unstable (>5% result variance on the same implementation), the frontend moves to the descriptive section.

### 3.9 Contract scope against platform surface — coverage declaration

Every platform has a surface larger than the contract. Exeris has `spi.events`, `spi.graph`, `spi.scheduling`, `spi.storage.blob`, `spi.crypto`; Spring's ecosystem is an order of magnitude larger. Chasing that surface leads to a contract that is never frozen.

Resolution: **the contract is not extended; coverage is declared.**

`coverage-declaration.md` contains, per arm:

```text
surface declared by the platform     (e.g. list of SPIs / modules)
surface exercised by the contract    (which of them are exercised at all)
surface out of scope                 (listed by name)
```

Example (Exeris):

```text
EXERCISED:      flow, persistence, http, events, config, bootstrap, telemetry, security,
                crypto (token signature verification only)
NOT EXERCISED:  graph, scheduling, storage.blob, memory, transport, context
```

Report sentence: *"The contract exercises 9 of 17 kernel SPI surfaces. Results do not extend to surfaces not covered."* This turns "we did not test graphs" from a gap into a declared scope.

**Graphs.** A graph gate enters the contract **only** if it passes the reachability rule of §3.2, i.e. if the requirement can be met with a recursive CTE in PostgreSQL. Admissible example:

```yaml
- id: DOD-QUERY-09
  requirement: >
    For a mission origin and a hop limit N, the system returns the tenant's eligible
    drones reachable over at most N open corridors within their remaining range,
    with the hop count and total length of the shortest such path.
  provenance: "US-xx — a dispatcher looks for drones able to reach a mission origin"
  motivating_arm: none
  reachable_without: [graph_engine]
  gate: true
```

A requirement that cannot be met without a graph engine is a platform requirement and **does not enter the contract in this campaign**, however well the domain justifies it.

### 3.10 Maturity of the surface under measurement

A result resting on a surface marked unstable expires sooner than the platform itself, and the reader cannot see that unless it is declared.

`arms.yaml` declares, per arm, the maturity of the surfaces the gates rest on:

```yaml
- id: exeris
  surfaces_under_test:
    flow:        stable
    persistence: stable
    http:        mixed
    events:      preview      # ← EVENTS gates rest on a preview surface
    security:    preview
  note: >
    EVENTS and SECURITY gates rest on surfaces declared preview in the SPI
    stability matrix. The contract shape may still change; the result is valid
    for the version given in env.lock.
```

Report sentence, where applicable: *"Event gates in the Exeris arm rest on SPIs marked preview; the result is dated by version, not by platform."*

The declaration cuts both ways: an arm whose gates rest on `stable` surfaces with TCK coverage and a compatibility gate has a stronger result than an arm with the same number of PASSes and no such declaration.

### 3.11 What the agent sees

Knowledge levels L0–L3 vary knowledge of the **platform**. Knowledge of the **domain** is constant. Every construction run, at every level, receives the same agent-facing projection of the contract:

| Artifact | Visible to the agent |
| --- | --- |
| `domain-profile.md`, `system-requirements.yaml`, `domain-model.yaml` | yes |
| `expected-api.yaml`, `external-api.yaml`, `expected-events.yaml` | yes — the oracle observes at the process boundary, so the boundary shape is part of the task |
| `anti-requirements.md` | yes — without it arms diverge on unrequested scope |
| `dod.yaml` — `id`, `requirement` | yes |
| `dod.yaml` — `oracle_check`, `mutation_tests`, `motivating_arm`, `reachable_without` | no — instrument metadata |
| `failure-scenarios.yaml` | behaviour only; harness timing and REC-1/2/3 parameters are not |
| `oracle/`, `mutants/`, reference implementations | no |
| `arms.yaml`, `coverage-declaration.md`, `neutrality-audit.md`, `preregistration/` | no — they disclose the hypotheses |
| `change-scenarios.yaml.age` | no — sealed until the construction phase ends |

The projection is rendered from `contract/` into `contract/agent-brief/`. Its hash is part of `promptHash` and `env.lock`, and it is covered by the prompt equivalence audit (§10).

The oracle is hidden until the agent's first "done" declaration; from then on the agent receives the oracle result after each declaration (§7.2).

---

## 4. Oracle

### 4.1 Construction rules

1. **Process boundary only.** HTTP, database, process signals, DOM/ARIA. No in-process introspection — otherwise `check_saga()` turns into "there is a `SagaInstance` table".
2. **Not built alongside the first implementation:**

   ```text
   contract → oracle → mutation suite → reference implementations → only then agents
   ```

3. **Four states:**

```text
[PASS]                     met
[FAIL]                     not met
[UNKNOWN]                  the instrument cannot judge reliably
[UNREACHABLE_IN_PARADIGM]  gate outside the arm's paradigm (§5A.2)
```

`UNKNOWN` counts as `FAIL`. `UNREACHABLE_IN_PARADIGM` does **not** — it goes to the separate `paradigm_coverage` metric.

4. **A verdict may not merge disjoint behaviours.** A rule like `still_nonterminal > 0 → stranded` gives the same verdict for 71% and for 0% resumption. Every aggregate gate publishes the distribution behind it next to the verdict.

5. **Concurrency gates check invariants, not winners.** When several missions compete for one resource, the oracle checks that no resource is double-booked and that every losing mission has an explicit rejection reason — never which mission won.

### 4.2 Interface

```text
check_api()        check_schema()      check_events()
check_frontend()   check_saga()        check_recovery()
check_migrations() check_openapi()     check_data()
check_contract()   check_graph_query()
```

### 4.3 Result

```text
DOD RESULT — campaign C-01 / contract v1.0.0 / arm jhipster / run R-014

[PASS]        Domain model
[PASS]        REST contract
[PASS]        Validation
[PASS]        Events
[UNREACH]     Saga completion        — outside the generator's paradigm
[UNREACH]     Saga compensation      — outside the generator's paradigm
[UNREACH]     Crash recovery         — outside the generator's paradigm
[PASS]        Migration V2
[PASS]        OpenAPI

GATES:              6 PASS / 0 FAIL / 0 UNKNOWN / 3 UNREACHABLE / 9
PARADIGM COVERAGE:  6/9
STATUS:             PASS (within the arm's declared scope)
```

### 4.4 Reference implementations

Mutants are mutations of a passing implementation, so the oracle needs one. It is calibrated against reference implementations of the frozen contract on **two arms: Exeris and Spring vanilla.** The oracle must return `PASS` on every in-scope gate of both. A gate that passes on one reference and not on the other is a defect in the contract or the oracle until shown otherwise — an oracle calibrated against a single arm can encode that arm.

Reference implementations may be agent-built. They are instrument artifacts: their construction is never scored, their cost goes to §12.3, they are never shown to a scored run, and they implement the construction contract only, never the sealed change scenarios.

### 4.5 Mutation self-test — entry condition

The oracle must catch **100%** of the set:

```text
M-01  saga completes but does not compensate
M-02  checkpoint written after ACK instead of before
M-03  restart resumes the workflow from the beginning, not from the checkpoint
M-04  event emitted without a correlation id
M-05  event emitted before the transaction commits
M-06  event payload matches the schema but carries stale state
M-07  migration V1→V2 loses rows
M-08  validation returns 200 for an invalid payload
M-09  pagination loses a record at a page boundary
M-10  OpenAPI describes an endpoint that does not exist
M-11  an endpoint exists but is missing from OpenAPI
M-12  tenant isolation leaks under a filtered query
M-13  a domain action is not idempotent on retry
M-14  UI shows stale state after an event
M-15  transitive query loses a path of length N, or loops on a cycle in the corridor graph
M-16  empty database reported as PASS
M-17  outbound command retried without its idempotency key causes a second dispatch
M-18  frames after a drone restart (new device session) rejected as stale
M-19  restriction fan-out exposes another tenant's incidents or events
```

M-16 guards against an aggregate check that is vacuously true on no data — e.g. "all sagas terminal" over an empty table. The guard is part of the oracle, not a comment.

The result (`oracle-selftest.json`) is an artifact of every run and a published metric. Phase 1 calibrates a smaller pilot set (`M-P1-*`, see [Phase 1 plan](phase-1-plan.md)); the full set grows as its gates enter the frozen contract.

---

## 5. Domains

### Domain A — Autonomous Drone Fleet Manager

Domain actions, saga, events, UI, persistence, relations, real time, telemetry, failure cases, one transitive query (§3.9). Profile: event-driven, long-running.

### Domain B — Contract & Billing Back-Office

```text
few events, no long-running workflow
many relations, complex reporting queries, aggregations, export
change history and retroactive corrections
bulk data import
```

The profile is chosen to favour a mature ORM and reporting ecosystem — the strengths of the comparison arms. **Both domains are published regardless of the result.**

Domain B is **held out**: no documentation, tooling, prompt, or routing change is tuned on Domain B results (§9.4). It is the only test of whether such changes generalise beyond Domain A. Its contract is frozen and hashed in the Campaign 1 preregistration, before any Domain A result exists; it runs in Campaign 2.

---

## 5A. Arms

### 5A.1 Two classification axes

```text
                     how the code comes about
                     ────────────────────────────────────────────
                     by hand          generated       declarative
                     (framework)      from a model    (runtime does it)
   durable      ┌──────────────┬────────────────┬─────────────────┐
   execution    │              │                │                 │
   ──────────   │              │                │                 │
   none /       │  Spring      │  JHipster      │  Causeway       │
   roll-your-own│  vanilla     │  (JDL)         │  (campaign 2)   │
                ├──────────────┼────────────────┼─────────────────┤
   external     │  Spring +    │       —        │        —        │
   orchestrator │  Restate     │                │                 │
                ├──────────────┼────────────────┼─────────────────┤
   in-process / │  Spring +    │       —        │  EXERIS         │
   library      │  DBOS        │                │                 │
                │  (Axon emb.) │                │                 │
                └──────────────┴────────────────┴─────────────────┘
```

The "in-process durable execution" corner is not empty: it holds a current position outside Exeris (DBOS) and one already measured in the existing corpus (Axon embedded).

**Two kinds of proximity — not to be mixed in one arm selection.** "Close to Exeris" means two different things and points to two different arms:

```text
engine-design proximity     similar engine philosophy: light, log-based, modern
  → Restate                  answers "is Exeris's approach better than its closest
                             contemporary counterpart"

deployment-shape proximity  same deployment shape: one process, backend in the database
  → DBOS                     answers "does the operational advantage survive when the
                             competitor also runs as one process"
```

An arm chosen for one kind of proximity **does not answer** the other's question. Restate is still two processes, so it does not close H5; DBOS has a different engine philosophy, so it does not close the question of approach quality. Hence both, both as subset arms.

### 5A.2 `arm_scope` — an arm need not pass the whole contract

```yaml
arms:
  - id: spring-vanilla
    scope: full
  - id: jhipster
    scope: full
    expected_unreachable: [DOD-SAGA-*, DOD-DURABLE-*]
  - id: exeris
    scope: full
  - id: spring-restate
    scope: subset
    proximity: engine_design
    gates: [DOD-SAGA-*, DOD-DURABLE-*, DOD-EVENTS-*, DOD-MIGRATION-*]
  - id: spring-dbos
    scope: subset
    proximity: deployment_shape
    gates: [DOD-SAGA-*, DOD-DURABLE-*, DOD-EVENTS-*, DOD-MIGRATION-*]
  - id: spring-axon-embedded
    scope: subset
    proximity: none
    role: continuity          # link to the existing corpus, not a competitor
    optional: true
    gates: [DOD-SAGA-*, DOD-DURABLE-*]
```

**Reporting rule:** a gate unreachable within an arm's paradigm is a result, not a run failure and not a reason for exclusion.

### 5A.3 Full arms (campaign 1)

| Arm | Role | Rationale |
|---|---|---|
| **Spring Boot vanilla** | prior baseline | what the model does by default; the reference point for WSS |
| **JHipster** (9.0.0, March 2026) | code-gen control | the agent writes JDL, not code — the sharpest test of SDC and change cost; closes the "generator vs hand-written" objection |
| **Exeris** | arm under study | |

On JHipster, because there is a temptation to dismiss it as "a faster Spring": **that is exactly the hypothesis the benchmark is meant to test, not an assumption it may rest on.** If JHipster is only a faster Spring, the arm is cheap and will confirm it. If JDL turns out cheaper in tokens than Exeris on the CRUD/API/UI/migration gates, that must be known before publication, not after. The maintenance-cost objection to JHipster is directly testable: it is Change 3–5 of §7.5, where regeneration starts to collide with custom code. The result there is the answer, not a prior.

### 5A.4 Subset arms — durable execution and operational complexity

| Arm | Processes besides the application | Proximity | Role |
|---|---|---|---|
| **Spring + Restate** | 2 | engine design | closest contemporary engine counterpart; continuity with the existing saga corpus |
| **Spring + DBOS Transact Java** | 0 (library, backend = PostgreSQL) | deployment shape | **control for the single-process thesis (H5)** |
| **Spring + Axon embedded (JDBC)** | 0 (no Axon Server) | none | **continuity arm**, optional — see below |

**Restate rather than Temporal.** The selection criterion for a subset arm is **engine-design proximity**: the question is "does Exeris's approach do better than its closest contemporary counterpart", not "what does an arbitrary orchestrator cost". Restate is closer in engine philosophy and already appears in the existing saga corpus, which gives **cross-campaign comparability**. Temporal remains a sensible second arm in this cell if budget allows, and then answers a different question: *what does the default market choice cost*, not *the closest counterpart*.

**Axon embedded — a continuity arm, not a competitor.** The assessment of the framework (heavy, slow) is separate from its evidential value. In the existing corpus this arm has two artifact-backed properties:

```text
– deployment unit = PostgreSQL + gateway, without an external engine          [CITABLE]
– throughput ceiling no lower than the Axon Server variant                    [CITABLE]
  (server-backed: fails at 60/s; embedded: fails at 70/s)
```

The conclusion recorded there — *the cost sits in the round-trip to the store, not in the process boundary* — comes from that corpus and limits the scope of the process-count claim (§7.8).

This arm's role is narrow and stays narrow: **a link between the old and the new corpus**, on a reduced gate set, so that results of both campaigns can be joined if they diverge. It is not a competing arm and does not enter construction-cost comparisons. If the budget is tight it is the first to go — and then it is entered in §5A.6 with a reason, not dropped silently.

**On DBOS:** having no first-hand experience with DBOS is an argument **for** including it. An arm the contract author does not know is the best available control against unconsciously shaping the contract around familiar capabilities. It, not Axon, carries H5.

### 5A.5 Maturity of the surface under measurement

See §3.10. `arms.yaml` declares the maturity of the surfaces each arm's gates rest on. For external arms it declares the version and release status (GA / beta / preview) of the modules used.

### 5A.6 Arms considered and rejected — with reasons

| Arm | Decision | Reason |
|---|---|---|
| **Temporal** | deferred behind Restate | same cell (2 processes); Restate is closer in engine design and comparable with the existing corpus. Enters as the cell's second arm if budget allows, answering the default-market-choice question |
| **Jmix** (3.0) | rejected | its advantage sits in Studio (an IDE plugin) unavailable to the agent — it would measure the IDE, not the platform |
| **Apache Causeway** | deferred to campaign 2 | closes a methodological objection (a second low-prior arm), not a product one |
| **Quarkus** as a fourth full arm | rejected for campaign 1 | at n=3 it cannot carry Spring vs Quarkus claims; it closes none of the three objections |
| **Own durable-execution implementation** | rejected | no stable artifact to compare; it would be an arm written by the contract author |

This table is published with the contract. An exclusion without an entry here is treated as an unreported result.

---

## 6. Agent knowledge levels

| Level | Input | What it measures |
|---|---|---|
| **L0** | agent brief only (§3.11) | the model's prior mass (not the platform) |
| **L1** | + official docs | value of documentation |
| **L2** | + source repository | value of access to the implementation |
| **L3** | + native tooling (MCP/LSP) | value of semantic affordances |

### 6.1 L0 — mandatory framing

```text
L0 is not a platform test. L0 is a dated measurement of the platform's presence
in the training data of a specific model version. An L0 result:
  – changes without any change to the platform,
  – is not comparable across arms,
  – is the zero point of the adoption curve.
```

**L0 does not appear in the arm comparison table.** A result in which a fast model builds canonical Spring/JPA instead of the target platform is reported exactly as it came out.

### 6.2 L1 — documentation as an asset

Per arm, the size and date of the documentation corpus provided are reported. Otherwise the comparison is of documentation volume, not of platforms.

### 6.3 L3 — single-arm ablation

```text
reported:      Exeris L2 → L3  (delta)
NOT reported:  L3 Exeris  vs  L3 Spring
```

A cross-arm comparison would need symmetric tooling for the comparison arm and a report of the effort spent on both.

```text
L3a — does tooling exist                          (trivial: yes/no)
L3b — how many turns/tokens a concrete operation saves
```

**MCP tool results count as input tokens.** This is where MCP can lose — verbose output costs.

### 6.4 Track S — specification

Contract derivation is measured as a separate track, never inside construction: mixing the two makes a `FAIL` ambiguous between a misread requirement and a broken build.

- **Input:** the world brief and the mapped user stories (the `provenance` texts), without the DOD (decision register D-37). Stories carry `provenance_origin: independent | brief_seeded | author` (D-36), and Track S reports results on the three sets separately. The model that wrote the stories does not take part in Track S.
- **Scope:** a Track S contract is not penalised for adding technical anti-requirements, which the brief never states.
- **Output:** a contract written by the agent.
- **Scoring:** item-level comparison with the reference contract — reference DOD items covered, missed, and items added beyond the anti-requirements.
- The contract contains no technology names, so Track S is platform-independent: it runs per model, without arms.

A chained track (S → construction on the agent's own contract → reference oracle) is permitted as a descriptive end-to-end result only. It never replaces the construction track and is not used for arm comparisons.

Track S is the specification stage of the planner/executor/verifier split excluded in §16; it is admitted alone because it needs no arm matrix.

---

## 7. Metrics

### 7.1 Construction cost — never a single number

```text
input_tokens / output_tokens / cache_read / cache_write   (separately)
cost_usd  + pricelist_date
wall_clock_min
turns
tool_calls
```

Token-to-token comparisons only within one model. Across models — USD and time.

Scored construction runs go through vendor subscriptions, so `cost_usd` is a valuation of the token vector at the dated list price, not an amount paid. The metric is the same either way; what limits the program is subscription throughput, not money (§9.6).

### 7.2 Agent reliability — the program's leading metric

```text
false_DONE_rate      "done" declarations with the DOD unmet, per run
first_pass_gap       gates missing at the first "done" declaration
self_correction      whether the agent closed the gap after seeing oracle output (y/n, turns)
turns_to_true_done   turns from the first "done" to an actual PASS
done_declarations_to_true_done
                     "done" declarations, each answered by an oracle report, until an actual PASS
```

These are defined against the protocol of §3.11: the oracle is hidden until the first "done". The oracle report is the only feedback an agent receives in a scored run: it is identical for every arm and reproducible. A human message to the agent is neither, and the contract author knows one arm best (§0, rule 3).

### 7.3 Runs reaching 100% and paradigm coverage

```text
runs_reaching_100  = runs with PASS on every gate in the arm's scope / runs
paradigm_coverage  = gates reachable in the arm's paradigm / contract gates
```

Together these replace a useless "DOD completion 100% / 100% / 100%".

```text
UNREACHABLE_IN_PARADIGM = a gate unreachable without leaving the arm's toolset.

In a general-purpose framework paradigm_coverage is 100% by definition, because
anything can be written by hand. The metric is NOT a measure of platform
completeness — it measures how narrow the paradigm is. Read alone it ranks
Spring vanilla highest. It may only be read together with construction cost:
100% coverage at three times the cost is a different result from 100% at baseline cost.
```

Reporting rule: the `paradigm coverage` row never stands in a table without an adjacent cost row, and never appears in report text as a standalone claim.

### 7.4 Adherence — split, with a prior column

```text
WSS  Wrong-Stack Substitution   the agent used another framework
     → machine-checkable (per-arm import/annotation allowlist) → gated
NIU  Non-Idiomatic Usage        right framework, beside its programming model
     → requires judgement → descriptive_only
```

Also measured during the run: `first_deviation_turn`, `self_recovery`.

```text
arm              WSS    prior          interpretation
Spring vanilla   ...    very high      no information
JHipster         ...    medium         cost of a niche DSL over a known stack
Causeway (c.2)   ...    low            does the "low prior" effect generalise
Exeris           ...    zero           information about the value of docs/tooling
```

### 7.5 Cost of a semantic change

**Sealed.** `change-scenarios.yaml` is written with the contract but stays encrypted until the construction phase ends.

**Cold context.** The change is made by the same model in a fresh session, without the construction history.

```text
Change 1  Additive        add a field (e.g. Drone.maxSpeedKmH)
Change 2  Relational      new relation (Drone ↔ OperatorProfile)
Change 3  Semantic        change of the conceptual model, not just a field
Change 4  Breaking        change of type/semantics of an existing field
Change 5  Cross-cutting   audit field on every entity + API + events + UI
```

After each change: `compile → migrate → regenerate → test → DOD`.

```text
files_touched, loc_touched, turns, tokens (broken down), cost_usd, wall_clock
failed_tests, missed_propagation, manual_interventions
regression_introduced   ← gates PASS before the change, FAIL after it
```

Derived metric: **Semantic Change Cost** = `cost_usd / successful_domain_change`.

### 7.6 Runtime — descriptive_only

Runtime is measured on agent-written code. It measures the agent's code quality on a given platform, not the platform. **Never a gate, never cited as a platform performance figure.**

```text
R0  telemetry OFF
R1  telemetry ON, write/persistence minimised
R2  production telemetry ON
```

For each: latency, CPU, RSS, allocation, disk write, disk size, startup, throughput.

**Footprint measurement hygiene:** every memory reading needs an artifact, a measurement window, and a forced-GC control. A reading "from the terminal" is not a result — in the saga corpus one such reading gave 1055 MB where the artifact-backed measurement gave 319 MB. Readings from different interfaces are not summed (RSS from `/proc` vs `anon` from cgroup), and an observability asymmetry is declared when one component is introspected and another only sampled from outside.

### 7.7 Separate gates: OpenAPI / Events / Migration

```text
OPENAPI    every endpoint described
           every described endpoint exists
           schemas complete / actions / errors represented

EVENTS     events declared, emitted
           payload correct, correlation correct
           emitted after commit, not before — on receipt the sink queries the API at once,
             and the state the event represents must already be visible
           duplicates with the same eventId accepted; the oracle deduplicates

MIGRATION  fresh install
           V1 → V2 with data (data preserved)
           V1 → V2 on an empty database
           idempotence: a re-run does not corrupt state
           rollback semantics (if required)
```

### 7.8 Infrastructure — two variants and the scope of the claim

```text
D-agent   deployment chosen by the agent
D-floor   minimal deployment for the arm
          — measured where a measuring arm exists, estimated only where it does not
```

Frozen profile: single node, no HA, no autoscaling.

Reported as **a vector, not a scalar**: `process_count`, `container_count`, `jvm_count`, `broker: y/n`, `coordinator: y/n`, `lock_service: y/n`, `external_runtime_count`.

There is no Architecture Complexity Index: a weighted scalar built by a competitor is not a measurement.

**Scope of the process-count claim.** Process count is an **operational** claim — resting footprint, number of moving parts, maintenance surface — and **not** a performance claim. The existing saga corpus shows that, comparing one framework deployed with and without a server, the throughput ceiling did not get worse and the cost sat in the round-trip to the store. Publishing process count as a performance argument would contradict that corpus.

What remains defensible and measured: the resting cost of a component the other arm does not have at all. That claim requires a single-process arm in the table (DBOS, Axon embedded) — otherwise the comparison is against the only alternative that loses by definition.

### 7.9 Semantic Duplication Count

Counting rule: one domain decision → the number of distinct artifacts in which it must be written for the system to work (`Java / DTO / OpenAPI / TS model / Zod / store / component / migration / event`).

The metric favours code-generating platforms by definition — it is a thesis, not a finding. It has value only if it correlates with the actual cost of change (Change 5). If it does not, the negative result is published. The comparison only makes sense against the generating arm (JHipster), because "Exeris vs hand-written Spring" is true by definition.

---

## 8. Models and pinning

Three classes for scored runs, all on one harness (Claude Code):

| Class | Model | Role |
|---|---|---|
| fast | Claude Haiku | model matrix; H3 at L3 |
| balanced | Claude Sonnet | Phase 4 model — baseline, 4b, L-ablation, L0, changes |
| deep | Claude Opus | model matrix; H3 reference at L1 |

Exact model identifiers are pinned in the preregistration and recorded per run.

**Off-vendor series.** Gemini Flash runs through Antigravity, a different harness. It is the only data point outside Anthropic and is reported as a separate series in its own table. It is never compared with the Claude runs in one table or claim: a harness difference cannot be told apart from a model difference.

Single sessions without an agent loop — the neutrality audit and other audits — may use other models (e.g. Gemini Argon), as assigned in the role table of `contract/user-stories/story-writer-prompt.md`.

```yaml
model:
  id: "exact API identifier"
  observed_date: YYYY-MM-DD
  harness: "name + version"
  harness_system_prompt_hash: "..."
```

**The agent harness is identical across all arms and models within a series** — its version dominates token counts more than platform differences do. Comparisons are made only within one harness.

---

## 9. Run protocol

### 9.1 Abort policy — frozen before the campaign

```yaml
abort_policy:
  max_turns: 120
  max_wallclock_min: 240
  max_cost_usd: 25
  on_abort: record_as_failure       # no retry, no exclusion
  human_intervention: record_as_failure   # any human message to the agent; annotated `intervened`,
                                          # kept in every metric including false_DONE_rate; never retried

retry_policy:
  infrastructure_error: retry_unlimited   # harness side only — container, network, subscription limit;
                                          # touches the environment, never the conversation with the agent
  agent_failure: no_retry                 # hallucination, wrong path, stuck — this is what is measured
  limit_wait: excluded_from_wall_clock    # time spent waiting for a limit reset is never wall_clock_min

reporting: all_runs_published_individually
```

### 9.2 Number of runs and the claim threshold

At least 3 runs per configuration.

```text
A difference between arms is claimed only when the [min, max] ranges of both
arms' runs do not overlap. Otherwise: INCONCLUSIVE.
```

All runs are reported individually, plus the median and p25/p75.

**Precedence of decision rules.** §9.2 and the falsification thresholds of §12.1 are different rules and at n=3 can give contradictory verdicts — the median within the threshold, the ranges overlapping. The order is fixed:

```text
1. §9.2 is the gate admitting ANY comparative claim.
2. §12.1 thresholds apply only after it passes.
3. Overlapping ranges ⇒ the hypothesis remains INCONCLUSIVE.
   Not "not falsified", not "confirmed" — inconclusive.
```

The distinction matters because only "not falsified" sounds like a result. The report uses only the first word until §9.2 passes.

### 9.3 Environment determinism (`env.lock`)

```text
model version (id + date)              harness version + system prompt hash
prompt hash                            agent-brief hash (§3.11)
repo / docs commit                     MCP / tooling version
package registry state (snapshot / lockfile)
network access: y/n + allowlist        system time and time zone
JDK / OS / hardware                    oracle version + self-test result
external arm module versions           surface maturity levels (§3.10)
simulator and event-sink version + hash  database version + profile
Track S: world-brief + brief-seeding hashes
```

### 9.4 Invalidation

```text
contract change                              ⇒ new campaignId
change to docs, tooling, or routing driven
by campaign results                          ⇒ new campaignId
runs from different campaignIds are not comparable
```

Campaign data may be used to improve Exeris documentation, tooling, and routing, but such a change alters the measured input. Domain B is never used for that tuning (§5).

### 9.5 Validation fences

Every defect in the harness, target, or oracle found during a campaign gets a **fence** — a marker with a date and commit that invalidates all earlier results for the affected gates.

```yaml
fences:
  - id: F-01
    marker: "commit abc1234"
    invalidates: "EVENTS gates on arm X before YYYY-MM-DD"
    reason: "..."
```

Results before a fence are not deleted — they are marked. Placing them next to post-fence results in one table is a reporting error, not a matter of taste.

### 9.6 Campaign 1 run matrix

The matrix is fixed here and in the preregistration, before any scored run; it is never trimmed during the campaign. Subscription throughput is the binding resource, and a shorter campaign also shortens the window in which a pinned model version can be withdrawn (§9.4).

| Stage | Configuration | Runs | Serves |
|---|---|---|---|
| Phase 4 | Sonnet × 3 full arms × L1 × 3 | 9 | H1; publication #1 (false-DONE) uses these runs |
| Phase 4b | Restate, DBOS × durable gates × 3, Phase 4 model | 6 | H5a, H5b |
| Phase 5 | Exeris × L2, L3 × 3, Phase 4 model | 6 | L-ablation (§6.3) |
| Phase 5 | L0 × 3 full arms × 1, Phase 4 model | 3 | descriptive only (§6.1) |
| Phase 6 | Haiku, Opus × 3 full arms × L1 × 3 | 18 | model comparison |
| Phase 6 | Haiku × Exeris × L3 × 3 | 3 | H3 |
| Off-vendor series | Gemini Flash (Antigravity) × 3 full arms × L1 × 3 | 9 | separate table; no comparison with Claude runs |
| Phase 7 | Changes 3, 4, 5 × 3 full arms × 3, Phase 4 model | 27 change sessions | H2, H4 |
| Track S | 3 models through the API, no agent loop | a few calls | Track S |

Total: 45 construction runs on Claude Code, 9 in the off-vendor series, and 27 change sessions. Track S runs through the API, which pins the model version; the API budget is also the reserve for retries after infrastructure errors.

Configurations not run in Campaign 1, each with its reason:

| Configuration | Reason |
|---|---|
| L0–L3 on Spring vanilla and JHipster | §6.3 defines the L-ablation on one arm; cross-arm L3 needs symmetric tooling (§16) |
| Model matrix at L0, L2, L3 | budget; L1 is the level of the arm comparison |
| L0 with 3 runs | L0 is descriptive and outside the comparison table; one run per arm suffices |
| Changes 1 and 2 | budget; no hypothesis depends on them (H2 uses Changes 3–5, H4 uses Change 5) |
| Axon embedded | optional continuity arm; first to go under budget (§5A.4) |
| Temporal | §5A.6 |

The harness asserts, on every turn, that the model reported by the vendor matches `env.lock`; a mismatch is an infrastructure error.

---

## 10. Prompts

```text
prompts/  L0/  L1/  L2/  L3/  S/
```

Every prompt is versioned and hashed.

**Equivalence audit.** The prompts and the agent brief are audited with one question: *does any arm get a hint the other does not?* The audit follows the same reproducible procedure as the neutrality audit (§3.4): published before its result, several auditor models, raw answers published, a public comment window.

**Equal starting budget.** Every arm gets a "getting started" section of equal token budget (±10%).

---

## 11. Data recording

```text
benchmark-run/
    run.json
    trajectory.jsonl
    metrics.json
    dod-result.json
    deployment.json
    oracle-selftest.json
    abort.json
    env.lock
    coverage.json           # §3.9 — surfaces touched by this run
    artifacts/
```

Outcomes are recorded **per gate**, not only per run. Each turn in `trajectory.jsonl` carries a stage label (`spec`, `build`, `verify`, `change`) and the DOD area being worked on — the minimum needed to derive per-stage, per-model data from campaign runs.

```json
{
  "campaignId": "C-01",
  "contractVersion": "1.0.0",
  "runId": "R-014",
  "track": "construction",
  "arm": "spring-dbos",
  "armScope": "subset",
  "model": "...",
  "modelObservedDate": "YYYY-MM-DD",
  "knowledgeLevel": "L1",
  "domain": "drone-fleet",
  "task": "greenfield",
  "promptHash": "...",
  "agentBriefHash": "...",
  "oracleVersion": "...",
  "fencesApplied": ["F-01"],
  "intervened": false,
  "outcome": "PASS_ON_STACK"
}
```

---

## 12. Preregistration and publication order

### 12.1 Hypotheses with falsification conditions

```text
H1  At an equal DOD level, construction cost in Exeris is lower than in the BEST
    of the other full arms.
    Falsified if: median cost_usd(Exeris) > 0.7 × min(cost_usd of the full arms).

H2  The cost of a semantic change grows more slowly in Exeris than in the generating arm.
    Falsified if: Semantic Change Cost(JHipster) ≤ Exeris on Change 3, 4, or 5.

H3  Agent-native tooling lets a faster model match heavier reasoning.
    Falsified if: fast+L3 does not reach the DOD level of deep+L1.

H4  Semantic Duplication Count predicts the cost of change.
    Falsified if: no monotonic relation SDC ↔ Semantic Change Cost on Change 5.

H5a On process count Exeris TIES with library-based durable execution.
    Predicted result: a tie (1 : 1). The hypothesis is preregistered so that the tie
    is recorded in advance rather than found by a reviewer.
    Falsified if: process_count(D-floor, Spring+DBOS) > process_count(D-floor, Exeris)
    — i.e. it falls if DBOS turns out WORSE than assumed.

H5b Under equal load the resting footprint of the whole deployment unit is lower
    in Exeris than in Spring+DBOS.
    Falsified if: footprint(Spring+DBOS) ≤ footprint(Exeris), artifact-backed,
    with a window and forced-GC control per §7.6.
    (Axon embedded is a continuity arm, not a test of H5 — §5A.4.)

H6  The L1/L2/L3 effect comes from documentation and tooling, not from a low prior alone.
    Falsified if: the L0→L3 curve for Causeway has the same shape at incomparable
    docs/tooling effort.   [campaign 2]
```

**Why H5 is split.** A condition "`process_count(D-floor)` of DBOS ≤ Exeris" is met by construction (`1 ≤ 1`): the hypothesis would be falsified before the first run. On process count a tie against an honest comparator is predictable by construction. H5a records that tie in advance, which removes a "1 vs 2+" headline before a reviewer does, and moves the operational claim to where it is still falsifiable: footprint (H5b).

**Durable store.** Every arm needs a database, and all arms run against the same PostgreSQL version and profile. The store is therefore a shared dependency: both H5 arms tie on runtime dependencies as well as on process count, and the operational claim reduces to the footprint of the application unit. The preregistration states this up front.

The existing corpus already partly undermines this whole axis: a single-process arm with a ceiling no lower than the server variant exists and is measured. That is a reason to preregister these hypotheses, not to remove them.

### 12.2 Publishing the preregistration

Hypotheses, contract, oracle, mutation suite, `arms.yaml`, the rejected-arms table (§5A.6), the coverage declaration (§3.9), and the abort policy are published **before** the campaign, with a hash.

**Freezing a set.** Every frozen set — the user-story procedure, the preregistration, the Domain B contract — gets:

- a **protected tag** (`us-procedure-*`, `prereg-*`, `domain-b-*`): a repository ruleset forbids deleting or moving tags matching these patterns. A tag is a name for the frozen commit, not evidence of time;
- an **independent timestamp** of the commit: archival of the public repository by Software Heritage ("Save code now"), or an OpenTimestamps proof of the commit hash. Commit dates are set by the author and prove nothing; the hosting provider's push history is neither permanent nor protected from force-pushes.

Documents and run metadata refer to a frozen set by its tag; the tag resolves to the commit hash.

### 12.3 Cost of the instrument

Contract, oracle, mutation suite, reference implementations, harness, and audits are reported as a separate line in `harness/instrument-cost.json`, by category (contract design including naming, oracle, mutants, reference implementations, harness, audits). Tokens are measured from the session logs of the agent harness. Human time is a rough estimate in working days per category, flagged as an estimate; a figure in seconds would claim a precision that self-reported time does not have. Accounting starts in Phase 1.

### 12.4 Publication order

```text
Publication #1   false-DONE rate — about AGENTS, not platforms
Publication #2   arm comparison, on an instrument with published calibration
Publication #3   cost of a semantic change
```

---

## 13. Instrument calibration

```text
oracle_detection_rate    % of mutants caught (100% required as an entry condition)
reference_agreement      oracle verdicts agree on both reference implementations (§4.4)
unknown_rate             % of gates ending UNKNOWN
flakiness                result variance on the same, unchanged implementation
evidence_capability      whether an arm CAN provide evidence that the DOD is met
simulator_control        the simulator's control scenarios give the same result on every arm
verdict_decomposition    whether every aggregate gate publishes its distribution, not only the verdict
```

The drone simulator, charging service, and event sink are instrument, not infrastructure: one version for every arm, recorded in `env.lock`, with control scenarios whose result is arm-independent by construction (as REC-3, §3.7). A control scenario that differs between arms is a harness defect.

`evidence_capability`: if an arm cannot show that its saga compensated, that is not a saga FAIL — it is an observability FAIL, and a separate, publishable result.

---

## 14. Phases

| Phase | Content | Exit condition |
|---|---|---|
| **1** | Contract (names included) + agent brief + oracle + mutation suite + reference implementations on Exeris and Spring vanilla + neutrality audit + coverage declaration | oracle catches 100% of mutants and agrees on both references; audit published |
| **2** | Harness: prepare → launch → execute → test → collect → DOD → archive, with per-gate and per-turn stage records | full run artifact generated automatically |
| **3** | Preregistration of hypotheses + `arms.yaml` + rejected-arms table, published with a hash | published before the first scored run |
| **4** | Baseline: Sonnet × **3 full arms** × L1 × 3 runs = **9 runs** | first numbers |
| **4b** | Durable/ops subset: Restate (engine design), DBOS (deployment shape), optionally Axon embedded (continuity) | the process and footprint table has ≥1 single-process arm besides Exeris |
| **4s** | Track S: models × user stories, no arms | item-level scoring against the reference contract |
| **5** | Knowledge ablation on Exeris (L2, L3) + L0 on every full arm, descriptive — §9.6 | |
| **6** | Model matrix at L1 + fast model at L3 on Exeris (H3) — §9.6 | |
| **7** | Change benchmark: Changes 3, 4, 5, cold context — §9.6 | |
| **8** | Runtime + infrastructure (descriptive_only) | |
| **9** | Domain B (held out) + Causeway (campaign 2) | |
| **10** | Final campaign + publishable dataset | |
| **—** | *Exeris Extensibility Test* | outside the program, §16 |
| **—** | Planner/executor/verifier beyond Track S | outside the program, §16 |

---

## 15. Final report format

```text
                        EXERIS   JHIPSTER   SPRING   RESTATE    DBOS   AXON-EMB*
---------------------------------------------------------------------------------
paradigm coverage         ...       ...       ...      ...      ...      ...
runs reaching 100%        ...       ...       ...       —        —        —
---------------------------------------------------------------------------------
cost USD (median)         ...       ...       ...       —        —        —
cost USD [min, max]       ...       ...       ...       —        —        —
turns (median)            ...       ...       ...       —        —        —
---------------------------------------------------------------------------------
Semantic Change Cost      ...       ...       ...       —        —        —
regression introduced     ...       ...       ...       —        —        —
SDC (Change 5)            ...       ...       ...       —        —        —
---------------------------------------------------------------------------------
processes (D-floor)       ...       ...       ...      ...      ...      ...
processes (D-agent)       ...       ...       ...      ...      ...      ...
resting footprint        descriptive_only, artifact-backed with forced-GC control
---------------------------------------------------------------------------------
WSS (+ prior)             ...       ...       ...      ...      ...      ...
---------------------------------------------------------------------------------
SPI surfaces under measurement: see coverage-declaration.md
surface maturity:               see arms.yaml (§3.10)
* JHipster: gates outside the paradigm are UNREACHABLE_IN_PARADIGM, not FAIL
* AXON-EMB: continuity arm with the old corpus, not a competing arm (§5A.4)
* paradigm coverage: 100% in a general-purpose framework is an artifact of the
  definition, not a strength — read only together with the cost row (§7.3)
```

Track S results are reported separately, per model, with no arm columns.

Every report includes: the limits section (§1.2, §1.3), instrument calibration state (§13), the coverage declaration (§3.9), the rejected-arms table (§5A.6), and the list of fences (§9.5).

No "efficiency frontier" chart is drawn before the data exist.

---

## 16. Deliberately out of scope

| Excluded | Reason | Where it goes |
|---|---|---|
| Contributor benchmark (CAP / SKU / template) | no comparison arm — a product test, not a comparison | separate *Exeris Extensibility Test* |
| Planner / executor / verifier roles beyond Track S | multiplies the matrix by 3 roles × N models | separate publication |
| Cross-arm L3 comparison | needs symmetric tooling | later decision, §6.3 |
| Platform performance | the code is written by the agent | existing benchmark corpus |
| SPI surfaces outside the coverage declaration | the contract must be freezable | §3.9 |
| Assisted runs (formalised human hints, intervention count as a metric) | would have to be a separate preregistered series; never mixed with scored runs | a later campaign, if at all |

---

## Open decisions

D-05 is deferred and resolved by a Phase 1 trial ([decision register](decision-register.md)). No other decision is open.
