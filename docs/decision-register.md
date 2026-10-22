# Pre-Phase-1 decision register

| ID | Decision | Why it blocks / affects the work | Owner | Status |
| --- | --- | --- | --- | --- |
| D-01 | Which database do arms use? | Determines whether H5b compares footprints with a shared runtime dependency. | arkstack-dev | closed 2026-10-22 — see below |
| D-02 | Does Spring + DBOS Transact Java use the same PostgreSQL profile? | Required for a fair H5b and `D-floor` comparison. | arkstack-dev | closed 2026-10-22 — by D-01 |
| D-03 | How is the neutrality audit performed? | Required before freezing the contract. No independent human reviewer is available. | arkstack-dev | closed 2026-10-22 — see below |
| D-04 | Does `DOD-QUERY-09` enter Campaign 1? | Raises the cost for every arm despite satisfying the reachability rule. | arkstack-dev | closed 2026-10-22 — see below |
| D-05 | Does the frontend pass the flakiness trial? | Above 5% result variance, UI gates are descriptive only. | arkstack-dev | deferred — resolved by trial, see below |
| D-06 | How is `D-floor` defined for each arm? | Without it there is no comparable infrastructure vector; the contract author defining competitors' topology is a conflict of interest. | arkstack-dev | closed 2026-10-22 — see below |
| D-07 | Does Domain B belong in Campaign 1 or 2? | Changes preregistration scope and instrument budget. | arkstack-dev | closed 2026-10-22 — see below |
| D-08 | Which model runs Phase 4b? | Determines cost comparability for durable/ops gates. | arkstack-dev | closed 2026-10-22 — see below |
| D-09 | Which contract artifacts does an agent see during a construction run? | Fixes the agent input across arms and knowledge levels; anything visible becomes part of the prompt under the equivalence audit. | arkstack-dev | closed 2026-10-22 — see below |
| D-10 | When does the agent see oracle output? | `false_DONE_rate` is undefined if the agent can run the oracle before declaring done. | arkstack-dev | closed 2026-10-22 — see below |
| D-11 | Is contract derivation measured, and where? | Mixing derivation with construction makes a FAIL ambiguous between a misread requirement and a broken build. | arkstack-dev | closed 2026-10-22 — see below |
| D-12 | What granularity do trajectories record? | Per-stage routing data cannot be recovered from run-level outcomes after the fact; the harness schema is set in Phase 2. | arkstack-dev | closed 2026-10-22 — see below |
| D-13 | May campaign results feed back into Exeris docs, tooling, or routing? | Tuning the measured inputs on the measurement contaminates later L1–L3 results. | arkstack-dev | closed 2026-10-22 — see below |
| D-14 | Are domain names part of the contract? | Naming entities, fields, and actions is a large share of construction effort and is unrelated to the platform. | arkstack-dev | closed 2026-10-22 — see below |
| D-15 | What implementation is the oracle calibrated against? | Mutants are mutations of a passing implementation; an oracle calibrated on one arm only may encode that arm. | arkstack-dev | closed 2026-10-22 — see below |
| D-16 | What autonomy model and precedence does the domain have? | Without a precedence rule two correct implementations diverge and the oracle has no single answer. | arkstack-dev | closed 2026-10-22 — see below |
| D-17 | Who are the external actors and how does the system reach them? | Determines `external-api.yaml` and makes the simulator part of the instrument. | arkstack-dev | closed 2026-10-22 — see below |
| D-18 | How does the oracle observe domain events? | Without a contract channel, agents reach for a broker and H5 is contaminated. | arkstack-dev | closed 2026-10-22 — see below |
| D-19 | How is telemetry ordered across drone restarts? | A sequence number alone rejects fresh frames after a reboot. | arkstack-dev | closed 2026-10-22 — see below |
| D-20 | How are time-dependent behaviours judged? | Silence detection depends on the server clock; it is the largest source of flakiness. | arkstack-dev | closed 2026-10-22 — see below |
| D-21 | What do scale, heterogeneity, and concurrency mean for gates? | Declared scale must not become a hidden performance criterion. | arkstack-dev | closed 2026-10-22 — see below |
| D-22 | What role do regulations play? | Regulation is the strongest neutral provenance, but compliance and GDPR erasure would pull in untested surfaces. | arkstack-dev | closed 2026-10-22 — see below |
| D-23 | Single- or multi-tenant, and how does identity cross the boundary? | Decides the security gates, M-12, and whether crypto is an exercised surface. | arkstack-dev | closed 2026-10-22 — see below |
| D-24 | What values do the requirement parameters take? | Without values the oracle has no single correct answer. | arkstack-dev | closed 2026-10-22 — see below |
| D-25 | May a drone charge while it has open service work? | SR-INV-05. | arkstack-dev | closed 2026-10-22 — see below |
| D-26 | What happens to a mission after `mission_pause_timeout_s`? | SR-TEL-05. | arkstack-dev | closed 2026-10-22 — see below |
| D-27 | What is the source of truth for a full charge? | SR-CHARGE-04. | arkstack-dev | closed 2026-10-22 — see below |
| D-28 | Does expiry of a restriction restore withdrawn approvals? | SR-ROUTE-03b. | arkstack-dev | closed 2026-10-22 — see below |
| D-29 | Does an inspection mission have a landing slot? | SR-SAGA-01/02 reserve take-off and landing slots for every mission. | arkstack-dev | closed 2026-10-22 — by D-34 |
| D-30 | What correlation do tenants' events carry in a cross-tenant fan-out? | SR-X-02. | arkstack-dev | closed 2026-10-22 — see below |
| D-31 | Can a dispatcher take over a drone whose connectivity is `lost`? | SR-INV-01 vs SR-OVR-01. | arkstack-dev | closed 2026-10-22 — see below |
| D-32 | How does telemetry report position? | Matching coordinates would bring geometry back into routing. | arkstack-dev | closed 2026-10-22 — see below |
| D-33 | Who chooses a mission's route and drone? | If the system plans routes or assigns drones, the oracle must judge solution quality. | arkstack-dev | closed 2026-10-22 — see below |
| D-34 | What is a slot? | SR-SAGA-01/02 rest on slots that were not defined. | arkstack-dev | closed 2026-10-22 — see below |
| D-35 | When is an in-flight mission affected by a restriction? | Progress along a route is not observable when position is only a corridor. | arkstack-dev | closed 2026-10-22 — see below |
| D-36 | How are user stories written? | Stories written after the requirements easily paraphrase them, and Track S then measures copying. | arkstack-dev | closed 2026-10-22 — see below |
| D-37 | What does a Track S run receive? | Without the brief, Track S is penalised for scope it never saw. | arkstack-dev | closed 2026-10-22 — see below |
| D-38 | What run matrix does Campaign 1 have, and through which channel? | Subscription throughput, not money, limits the program; trimming the matrix during the campaign would look like selecting results. | arkstack-dev | closed 2026-10-22 — see below |
| D-39 | Which models run scored sessions, and on which harness? | The harness dominates token counts; mixing harnesses in one comparison confounds harness with model. | arkstack-dev | closed 2026-10-22 — see below |
| D-40 | How is the instrument's cost measured? | Self-reported active seconds cannot be checked and claim false precision. | arkstack-dev | closed 2026-10-22 — see below |
| D-41 | What happens when a human intervenes in a scored run? | Human guidance is neither identical across arms nor reproducible, and the contract author knows one arm best. | arkstack-dev | closed 2026-10-22 — see below |

Closed decisions must state their evidence, date, author, and impact on the contract or preregistration. Rejected decisions are retained.

## Closed decisions

### D-01 — One database profile for every arm

Every arm needs a database to persist state; the database engine is a deployment choice, not a contract item. All arms run against the same PostgreSQL version and profile, recorded in `env.lock`. The store is a shared dependency: it is counted in each arm's `D-floor` vector identically and is not a point of comparison. H5b therefore compares the footprint of the application unit only. This also settles D-02.

Impact: `contract/arms.yaml`; program plan §12.1 (H5b); `D-floor` definitions.

### D-03 — Reproducible, not independent, audits

No independent human reviewer is available, and a model configured by the contract author is not outside the project. The neutrality audit (and the prompt equivalence audit, program plan §10) is therefore reproducible instead of independent: the procedure — prompt, models, exact input — is published in the preregistration before the result is seen; several auditor models, preferably from different vendors, run it, and their raw answers are published in full; a public comment window with a fixed deadline opens before the contract freezes. Every report states that the audit was run by models configured by the contract author according to a published procedure and is not independent.

Impact: program plan §3.4, §10; preregistration.

### D-04 — `DOD-QUERY-09` enters Campaign 1

After D-33, SR-ROUTE-02 is the dispatcher's tool for choosing a mission's drone, not an optional extra. It is also the only gate behind the coverage entry "graph: not exercised; transitive query exercised". Its cost is the same for every arm.

Impact: Campaign 1 DOD; coverage declaration.

### D-05 — Frontend flakiness is decided by a trial

Not a decision but a Phase 1 procedure: N runs of the UI gates on both reference implementations (D-15), against the 5% variance threshold. The result decides. The frontend scope itself waits for the H1 scope decision.

Impact: Phase 1 plan.

### D-06 — `D-floor` by rule, resolved against Exeris

`D-floor` for each arm is the minimal single-node topology given in the vendor's official documentation, with a citation. Every ambiguity is resolved in the competitor's favour — the smaller process count is taken. A rule that is asymmetric against the contract author is the only defence that works without an independent reviewer.

Impact: program plan §7.8; `contract/arms.yaml`.

### D-07 — Domain B runs in Campaign 2, frozen in Campaign 1

Domain B runs in Campaign 2, but its contract is frozen and hashed in the Campaign 1 preregistration, before any Domain A result exists, so it cannot be chosen after seeing the first numbers. The Campaign 1 report is labelled "Domain A only; Domain B frozen on <date>, runs in Campaign 2". Domain B remains held out (D-13).

Impact: preregistration; program plan §5, §14.

### D-08 — Phase 4b uses the Phase 4 model

The durable/ops subset runs on the same pinned model as Phase 4. Otherwise its costs are not comparable with the full arms and the §15 table loses its meaning.

Impact: program plan §14.

### D-09 — Agent-facing contract in the construction track

Knowledge levels L0–L3 vary knowledge of the **platform**; knowledge of the **domain** is held constant. Every construction run, at every level, receives the same agent-facing projection of the contract:

| Artifact | Visible to the agent |
| --- | --- |
| `domain-profile.md`, `system-requirements.yaml`, `domain-model.yaml` | yes |
| `expected-api.yaml`, `external-api.yaml`, `expected-events.yaml` | yes — the oracle observes at the process boundary, so the boundary shape is part of the task |
| `anti-requirements.md` | yes — without it arms diverge on unrequested scope and cost stops being comparable |
| `dod.yaml` — `id`, `requirement` | yes |
| `dod.yaml` — `oracle_check`, `mutation_tests`, `motivating_arm`, `reachable_without` | no — instrument metadata |
| `failure-scenarios.yaml` | behaviour only (e.g. "survives SIGKILL"); harness timing and REC-1/2/3 parameters are not |
| `oracle/`, `mutants/` | no |
| `arms.yaml`, `coverage-declaration.md`, `neutrality-audit.md`, `preregistration/` | no — they disclose the hypotheses |
| `change-scenarios.yaml.age` | no — sealed until the construction phase ends |

The projection is generated from `contract/` into `contract/agent-brief/`, never maintained by hand. Its hash is part of `promptHash` and `env.lock`, and it is covered by the prompt equivalence audit.

Impact: Phase 2 harness (render step), Phase 3 prompts, `env.lock`.

### D-10 — Oracle visibility

The oracle is hidden until the agent's first "done" declaration. From then on the agent receives the oracle result after each declaration, which is what `self_correction` and `turns_to_true_done` measure.

Impact: Phase 2 harness loop; §7.2 metrics are defined against this protocol.

### D-11 — Specification track (Track S)

Contract derivation is measured as a separate track, not inside construction:

- **Input:** the world brief and the `in_contract` user stories (the `provenance` texts), without the DOD (D-37).
- **Output:** a contract written by the agent.
- **Scoring:** item-level comparison with the reference contract — reference DOD items covered, missed, and items added beyond the anti-requirements.
- The contract contains no technology names, so Track S is platform-independent: it runs per model, without arms.

A chained track (S → construction on the agent's own contract → reference oracle) is permitted as a descriptive, end-to-end result only. It never replaces the construction track and is not used for arm comparisons.

Track S is the specification stage of the Planner/Executor/Verifier split excluded by §16; it is admitted alone because it needs no arm matrix. The other roles remain out of scope.

Impact: §1.2 gains a pointer to Track S; preregistration lists it as a separate, model-only measurement.

### D-12 — Trajectory granularity

Outcomes are recorded per gate, not only per run. Each turn in `trajectory.jsonl` carries a stage label (`spec`, `build`, `verify`, `change`) and the DOD area being worked on. This is the minimum needed to derive per-stage, per-model routing data from campaign runs.

Impact: Phase 2 harness schema; `metrics.json` and `dod-result.json` gain per-gate records.

### D-13 — Feedback into Exeris and held-out data

Campaign data may be used to improve Exeris documentation, tooling, and routing, but a change to any of them is a change to the measured input: it requires a new `campaignId` (the docs and tooling commits are already in `env.lock`). Domain B is held out: no docs, tooling, prompt, or routing change is tuned on Domain B results. It is the only test of whether those changes generalise beyond Domain A. This holds whether Domain B lands in Campaign 1 or 2 (D-07).

Impact: §9.4 invalidation rule; preregistration states the held-out domain.

### D-14 — Domain names are contract content

Names of entities, fields, actions, endpoints, events, and UI accessible names are fixed by the contract in `domain-model.yaml`, `expected-api.yaml`, and `expected-events.yaml`, and an agent receives them (D-09) instead of inventing them. Naming effort is contract design: it is recorded under that category in `harness/instrument-cost.json`, and it never enters a run's construction cost.

Impact: Phase 1 contract artifacts; instrument-cost categories.

### D-15 — Two reference implementations for oracle calibration

The oracle is calibrated against reference implementations of the frozen campaign contract on two arms: Exeris and Spring vanilla. Phase 1 exits only when the oracle gives `PASS` on every in-scope gate of both and detects 100% of the mutants derived from them. A gate that passes on one reference and not the other is a defect in the contract or the oracle until shown otherwise.

Reference implementations may be agent-built; they are instrument artifacts, so their construction is never scored. Their cost, human and token, is reported under §12.3. They are never exposed to a scored run (D-09), and they implement the construction contract only — never the sealed change scenarios.

Impact: Phase 1 exit criteria; mutant set provenance; §12.3 instrument cost.

### D-16 — Supervisory autonomy with fixed precedence

The system supervises; flight control is on the drone and outside the system. Missions need dispatcher approval; approval can be invalidated in flight. Precedence: airspace restriction > critical battery > operator/dispatcher decision > mission plan. A dispatcher can take over a drone; taken over is a flag orthogonal to the operational state. While it is set, restriction and critical-battery policies still act, the mission plan does not advance by itself, and warning-level policies emit their events and record requests that take effect after release.

Impact: `contract/domain-profile.md` §2; requirements for approval, takeover, and policy conflicts.

### D-17 — External actors and the simulator

The system is a single-node central backend. Drones, the charging service, and readiness/waypoint sources are external actors played by a simulator. The simulator and the event sink are instrument: one version for every arm, hashed in `env.lock`, calibrated by control scenarios whose result is arm-independent by construction. What the system calls is a contract artifact, `external-api.yaml`, visible to the agent. Outbound commands and charge-service requests are at-least-once and carry an idempotency key (mutant M-17).

Impact: program plan §3.1, §3.11, §9.3, §13; `contract/domain-profile.md` §3.

### D-18 — Events by webhook to a sink

Domain events are delivered by HTTP webhook to an event sink in the harness, at-least-once, each with a unique `eventId`. On receipt the sink queries the API immediately; the state the event represents must already be visible, which makes publication before commit (M-05) observable. Duplicates with the same `eventId` are accepted and deduplicated by the oracle. A polled event feed was rejected because it does not expose publication before commit as directly. No broker is required by the contract.

Impact: `expected-events.yaml`; program plan §7.7.

### D-19 — Telemetry order is (device session, sequence)

Every frame carries a device session number that increases on every drone restart; order is the pair `(session, sequence)`, and a higher session supersedes every lower one. The device timestamp is recorded and never used for ordering. A monotonic session number is required: an opaque session identifier cannot distinguish a new session from a late frame of an old one. A frame older than the last processed frame of the same session is kept in history and does not change current state (mutant M-18).

Impact: SR-TEL-01; `contract/domain-profile.md` §4.

### D-20 — Time by tolerance windows

Time-dependent behaviour is specified as a window `[T, T + Δ]` with a generous `Δ`. The harness does not control the system's clock and the API exposes no time-control hook, which would be implementation leakage. Time-dependent gates have measured flakiness and move to the descriptive section above 5% variance on an unchanged implementation.

Impact: SR-TEL-03 and every timeout requirement; program plan §13.

### D-21 — Scale as data, concurrency as invariants

Declared scale (a few hundred drones, tens of pads per tenant) is data context for pagination and contention, never load: the harness does not drive fleet-scale telemetry during functional gates. Concurrency gates check invariants — no double-booked resource, an explicit reason for every losing mission — never which mission won. Heterogeneity is in data (capabilities, connector type), not in protocols. Two mission types: delivery and inspection.

Impact: `contract/anti-requirements.md`; program plan §4.1; `contract/domain-profile.md` §5, §7.

### D-22 — Regulation as provenance only

EU drone regulation is cited as provenance, never as compliance: 2019/947 Art. 15 (geographical zones) and Annex UAS.SPEC.050 (maintenance records), 2021/664 Art. 9 (geo-awareness: restrictions with validity and version) and Art. 10 (flight authorisation per flight, updated or withdrawn in flight). GDPR is provenance for isolation and access control only; retention and erasure are anti-requirements, because they would pull in scheduling and crypto-shredding and favour event-sourced designs.

Impact: `contract/domain-profile.md` §9; `contract/anti-requirements.md`.

### D-23 — Multi-tenant, token verified by public key

The system is a multi-tenant service for drone-fleet operators. Drones, missions, pads, incidents, and service work are tenant-private; corridors, zones, and restrictions are shared and managed by a platform administrator, who sees tenant data only as the aggregate impact of a restriction. No pads are shared between tenants. Roles: operator, dispatcher, platform administrator.

Identity crosses the boundary as a JWT signed by the harness with a private key; the system holds only the public key and verifies. Boundary standards (HTTP, OpenAPI, JSON, JWT) are not implementation leakage (program plan §3.3). Signature verification makes crypto an exercised surface, declared as such in the coverage declaration. A restriction that aborts missions of several tenants must not leak one tenant's incidents or events to another (mutant M-19).

Impact: program plan §3.3, §3.9, §4.5; `contract/domain-profile.md` §1.

### D-24 — Parameter values and constraints

The proposed values in `system-requirements.yaml` → `parameters` are adopted, with `degraded_recovery_ratio` added as link hysteresis and `parameter_constraints` protecting the relations between values (e.g. a drone eligible for a mission must not immediately cross the warning threshold). Latency is not a degradation criterion: it compares the device clock with the system clock and measures their synchronisation, not the system. Gaps in the sequence suffice and are deterministic.

Impact: `system-requirements.yaml`. A full mission-pause timeout path takes about 165 s per oracle scenario; `mission_pause_timeout_s` is the first candidate to shorten if oracle time matters.

### D-25 — Charging during service work

Allowed. Service work is a fact orthogonal to the operational state, so a drone can have open service work and be charging; a ban has no domain basis.

Impact: SR-INV-05; vocabulary.

### D-26 — Mission after the pause timeout

Aborted; reservations are released with compensation events; the drone stays `lost` with its connectivity incident open.

Impact: SR-TEL-05.

### D-27 — Full charge comes from telemetry

Telemetry is the only source of truth for battery level. A charging-service callback would add a second source that can disagree with it.

Impact: SR-CHARGE-04; `external-api.yaml` has no charge-complete callback.

### D-28 — Expiry does not restore approvals

When a restriction expires, approvals it withdrew stay withdrawn. Approval is a human decision (2021/664 Art. 10); automatic restoration would add a timer with no measurement value.

Impact: SR-ROUTE-03b.

### D-30 — Per-tenant correlation in a fan-out

In each tenant's events, the cause of a fan-out reaction is the restriction (id and version) and the correlation identifier is generated per tenant. The administrator's request correlation never appears in tenant events, so a tenant cannot infer that another tenant was affected.

Impact: SR-X-02; mutant M-19.

### D-31 — A lost drone can be taken over

Taking over is a decision recorded by the system, not a command to the drone and not a change of assignment, so SR-INV-01 does not block it. The connectivity incident stays open.

Impact: SR-OVR-01.

### D-32 — Position is a location or a corridor

A frame reports position as a location (on the ground, docked or not) or a corridor (in flight). Coordinates, if present, are descriptive and used by no rule. Position, open service work, and takeover are facts orthogonal to the operational state; `docked` and `maintenance` are not operational states, so a docked, charged drone is `idle` and eligible.

Impact: vocabulary; `domain-profile.md` §4.

### D-33 — The dispatcher chooses route and drone

The dispatcher gives the drone and the route, as a sequence of corridors from the drone's location through the origin to the end location. The system validates connectivity of the route, eligibility, and range, and never computes a route or assigns a drone. SR-ROUTE-02 is a selection aid for the dispatcher, not an assignment mechanism.

Impact: SR-MIS-01, SR-ROUTE-01; `domain-profile.md` §5.

### D-34 — Slots are location capacity

Each location has a number of take-off and landing slots. A mission holds one take-off slot at the first location of its route and one landing slot at its end location — the origin, for inspection — from reservation until it completes, is rejected, or is aborted. This closes D-29.

Impact: SR-SAGA-01/02; `domain-profile.md` §6.

### D-35 — The full route decides whether a mission is affected

A mission is affected by a restriction when any corridor of its full route is covered, whatever part has already been flown.

Impact: SR-ROUTE-03b, SR-TEN-03.

### D-36 — Independently written user stories

User stories come from a world independent of the requirements:

1. **World brief**, written and published by the contract author: who the operators and dispatchers are, which drones they fly, which missions they run, the conditions they work in, which regulations apply. It describes the world only — no system behaviour, no thresholds, no states, no mechanisms, and no account of past failures: failures written by the author would map one-to-one onto requirements, so bad days are invented by the story writer in its interviews. It is the single point where the author shapes the content, so it is short and public.
2. **Story writer**: a model from a different vendor that receives only the brief and produces stories through interviews with personas (fleet technician, dispatcher, airspace desk), not through an instruction to "write user stories". It never sees the requirements.
3. **Mapping**: a separate instance that sees the requirements maps stories to them; the author reviews the mapping.
4. **A requirement without a story is a signal, not a gap to fill**: either the brief is too thin or the requirement is a platform requirement in domain clothing — the same logic as `motivating_arm`. Missing stories are written by the author.

Every story carries `provenance_origin`: `independent` (derived from a fact in the brief), `brief_seeded` (derived from a constraint or seeded need listed in `contract/user-stories/brief-seeding.md`), or `author`. The mapping instance also marks any story that paraphrases a specific brief sentence. The seeding declaration names requirement IDs and is never given to the writer. Track S reports the three sets separately, and the story-writing model does not take part in Track S.

Roles, vendors, and the isolation of chat-interface runs are fixed in `contract/user-stories/story-writer-prompt.md` and published with a hash before the writer runs.

Stories, written either way, use the language of operators and dispatchers — what happened, what they need, what they fear — and state no thresholds, state names, or order of steps.

Impact: `provenance` of every requirement; Track S input (program plan §6.4).

### D-37 — Track S input: brief and mapped stories

A Track S run receives `world-brief.md` and the stories whose mapping scope is `in_contract` — at least one `direct` or `partial` mapping — so the boundary is set by the mapping data, not by the author's judgement. Stories marked `excluded`, `contradicts`, or `unaddressed` are withheld, because they would penalise scope the contract does not have; their counts are reported. Anti-requirements are split into user-visible ones, which appear in brief §8 and are kept in sync with it, and technical ones, which never appear in the brief and which a Track S contract is not penalised for adding. The hashes of `world-brief.md` and `brief-seeding.md` are part of a Track S run's `env.lock`: the `brief_seeded` category depends on the seeding declaration, so a change to it changes Track S results.

Impact: program plan §6.4, §9.3; `contract/anti-requirements.md`.

### D-38 — Fixed run matrix on subscriptions

Scored construction runs go through vendor subscriptions; `cost_usd` is a list-price valuation of the token vector. A subscription limit hit mid-run is an infrastructure error, retried under §9.1, and the time spent waiting for a reset is excluded from `wall_clock_min`. Track S runs through the API, which pins the model version; the API budget also covers retries. The harness asserts on every turn that the reported model matches `env.lock`.

The Campaign 1 matrix is fixed in program plan §9.6 before any scored run: 45 construction runs and 27 change sessions, against 108+ for the full matrix. It includes a fast-model L3 run on Exeris, without which H3 cannot be tested, and Changes 3–5, without which H2 and H4 cannot. Every configuration not run is listed with its reason (§0, rule 4).

Impact: program plan §7.1, §9.1, §9.6, §14; preregistration.

### D-39 — Claude classes on one harness, Gemini Flash as a separate series

Scored runs use three Claude classes on Claude Code: Haiku (fast), Sonnet (balanced, the Phase 4 model), Opus (deep); exact identifiers are pinned in the preregistration. Gemini Flash runs through Antigravity as a separate series — the only data point outside Anthropic — reported in its own table and never compared with Claude runs, because a harness difference cannot be told apart from a model difference. Gemini Argon is used only for single sessions without an agent loop, such as the neutrality audit.

Impact: program plan §8, §9.6.

### D-40 — Instrument cost: measured tokens, estimated days

Tokens spent on the instrument are measured where a session log exists. A session without a log — a chat interface — is listed by name with tokens `null` and, where available, a checkable proxy (transcript characters and turns from the conversation export); it is never added to a token total, so the total is not read as the full cost. Human time is a rough estimate in working days per category, flagged as an estimate; seconds of "active" time are self-reported, unverifiable, and ill-defined when the work is done with AI. If a less arbitrary figure is wanted, session time can be reconstructed by rule from message timestamps (summing gaps shorter than a fixed threshold). Scored runs record no human time: they are autonomous, their duration is `wall_clock_min`, and human involvement is an event (D-41).

Impact: `harness/instrument-cost.json`; program plan §12.3.

### D-41 — An intervention loses the run

In a scored run the only feedback to the agent is the oracle report after a "done" declaration (D-10): identical for every arm and reproducible. Any human message to the agent makes the run a `FAIL` annotated `intervened`; it stays in every metric, including `false_DONE_rate`, and is never retried. Hallucination, a wrong path, or getting stuck is an agent failure — the phenomenon publication #1 measures — so excluding such runs would remove the subject from the data. Only harness-side infrastructure errors are retried: a failed container, a subscription limit, a broken network — the environment, never the conversation. How much help an agent needs is measured by the oracle cycles (`done_declarations_to_true_done`); a series with formalised human hints would be a separate preregistered series and is not part of Campaign 1.

Impact: program plan §7.2, §9.1, §11, §16.
