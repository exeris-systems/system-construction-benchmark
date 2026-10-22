# Domain profile — Autonomous Drone Fleet Manager

This profile fixes the shape of the domain before requirements are written. Every requirement in `system-requirements.yaml` must be consistent with it. User stories are written from `user-stories/world-brief.md`, never from this profile (decision register D-36). It describes behaviour and boundaries only; it names no implementation technology except standard protocols at the process boundary (program plan §3.3).

## 1. Customer and tenancy

The system is a multi-tenant platform operated as a service for several drone-fleet operators.

| Data | Ownership | Access |
| --- | --- | --- |
| Drones, missions, charging pads, incidents, service work | private to one tenant | that tenant's users only |
| Transit corridors, airspace zones, airspace restrictions | shared, managed by the platform administrator | read by every tenant |

Charging pads are never shared between tenants.

Roles:

| Role | Scope | May |
| --- | --- | --- |
| Operator | one tenant | register and maintain drones and pads, request charging, open and close service work |
| Dispatcher | one tenant | create, approve, and abort missions; take over a drone |
| Platform administrator | platform | manage corridors, zones, and restrictions; sees no tenant-private data except the aggregate impact of a restriction (number of affected missions per tenant, without identifiers) |

A platform-administrator action can affect many tenants at once — a new restriction aborts missions of several tenants. Each tenant observes only its own consequences: its incidents, events, and views never contain another tenant's data.

## 2. Autonomy

The system supervises; it does not fly. Flight control runs on the drone and is outside the system. The system validates and dispatches missions chosen by dispatchers, monitors the fleet, and enforces safety policies on its own; humans approve missions and may override.

A mission requires dispatcher approval before dispatch. Approval can be invalidated while the mission is in progress.

**Precedence.** When automatic policies and human decisions conflict, the higher rule wins:

```text
1. airspace restriction          (always applies)
2. critical battery              (always applies)
3. operator / dispatcher decision
4. mission plan
```

A dispatcher can take over a drone and release it. **Taken over** is a flag orthogonal to the drone's operational state — a drone in a mission can be taken over. While taken over, rules 1 and 2 still act automatically, the mission plan does not advance by itself, and warning-level policies emit their events and record their requests, which take effect after release.

## 3. Deployment and external actors

The system is a central backend on a single node (anti-requirements: no HA, no multi-node). Drones, the charging service, and readiness, waypoint, and arrival sources are external actors. In a benchmark run they are played by a simulator that is part of the instrument, identical for every arm.

| Direction | Channel | Contract artifact |
| --- | --- | --- |
| into the system — user actions, telemetry frames, external readiness, waypoint, and arrival events | HTTP | `expected-api.yaml` |
| out of the system — drone commands, charge-service requests | HTTP calls to the simulator | `external-api.yaml` |
| out of the system — domain events | HTTP webhook to an event sink | `expected-events.yaml` |

No broker, queue, or coordinator is required by the contract. An arm may introduce one, and it then appears in its `D-agent` vector.

Delivery in every direction is **at-least-once**:

- inbound events and frames may arrive duplicated or out of order;
- every outbound command and charge-service request carries an idempotency key; a retried command with the same key must not cause a second dispatch;
- every domain event carries a unique `eventId`; the sink may receive it more than once, and duplicates with the same `eventId` are not a defect.

## 4. Connectivity and telemetry

Link unreliability is modelled in the data, not in the network: the simulator replays frames late, duplicated, out of order, or not at all.

- Every frame carries a device timestamp, a **device session number** (increases by at least one every time the drone restarts), and a sequence number. Frame order is the pair `(session, sequence)`; a higher session supersedes every lower one regardless of sequence values. The device timestamp is recorded and never used for ordering.
- A frame reports the drone's position as a location (on the ground, docked or not) or a corridor (in flight). Coordinates, if present, are descriptive and never used by any rule.
- A frame that does not advance the `(session, sequence)` order — an older frame of the current session or any frame of a lower session — is stored in history and does not change current position, battery, or operational state.
- The absence of telemetry is detected by the system against its own clock (see §8).

## 5. Fleet heterogeneity and mission types

Drones differ in data, not in protocol: model, payload capacity, range, sensor packages, and charging connector type. All drones use one telemetry schema and one command interface.

Two mission types:

| Type | Exercises |
| --- | --- |
| Delivery | payload capacity, point-to-point route, destination slot |
| Inspection | required sensor packages, waypoint sequence |

| Type | External events after dispatch |
| --- | --- |
| Delivery | readiness, arrival at destination |
| Inspection | readiness, waypoint reached (one per waypoint, in order), arrival at origin |

The dispatcher chooses the drone and gives the route as a sequence of corridors from the drone's location through the origin to the end location. The leg from the drone's location to the origin is part of the route in every respect — range, slots, and restrictions. The system validates both and never computes a route or assigns a drone: route planning and fleet assignment are optimisation problems whose quality the oracle cannot judge.

## 6. Airspace model

Airspace is a graph: transit corridors connect locations (mission origins, destinations, pads), and each corridor has a length. Corridors are undirected. The graph may contain cycles. An idle drone is always at a location. Zones group corridors and locations. A route is a sequence of corridors. Each location has a number of take-off slots and landing slots. A mission holds one take-off slot at the first location of its route and one landing slot at its end location from reservation until it completes, is rejected, or is aborted. A restriction applies to zones or corridors, has a validity period, and has a version.

The model needs no geometry: intersection of a route with a restriction is membership of a corridor in a restricted zone, and reachability is a bounded, length-weighted traversal of the corridor graph (program plan §3.2, reachability rule).

## 7. Scale

Declared as data context, not load:

- up to a few hundred drones and tens of pads per tenant — lists must be long enough to paginate;
- several missions competing for the same drone, pad, or slot — concurrency must be real.

The harness never drives telemetry at fleet scale during functional gates. Throughput and latency are not `PASS` criteria (anti-requirements; program plan §7.6).

## 8. Time

The system detects silence and timeouts against its own clock. The contract states each time-dependent behaviour as a window `[T, T + Δ]` with a generous `Δ`; the harness does not control the system's clock, and the API exposes no time-control hook. Time-dependent gates have measured flakiness; above 5% result variance on an unchanged implementation, a gate moves to the descriptive section (program plan §3.8, §13).

## 9. Regulatory provenance

Requirements may cite EU drone regulation as provenance. The system is **not** compliant with any regulation and makes no claim to be.

| Source | Provides provenance for |
| --- | --- |
| Implementing Regulation (EU) 2019/947, Art. 15 — UAS geographical zones | zones that prohibit operations or impose conditions on them |
| Implementing Regulation (EU) 2021/664, Art. 9 — geo-awareness service | restrictions with a validity period and a version, delivered promptly |
| Implementing Regulation (EU) 2021/664, Art. 10 — UAS flight authorisation service | approval per mission before dispatch; approval updated or withdrawn in flight when a new restriction applies |
| Implementing Regulation (EU) 2019/947, Annex, UAS.SPEC.050 — operator responsibilities | records of maintenance activities (service work) |
| GDPR | tenant isolation and access control only |

Data retention and erasure are out of scope (anti-requirements).
