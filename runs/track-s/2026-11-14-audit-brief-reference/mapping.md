# Audit items against the reference

Each audit item (`audit-requirements.yaml`, AR) mapped by hand onto the reference
(`trackS/brief-requirements.yaml`, BR) on 2026-11-14, by Claude Code (Claude Opus 5.5), the model
that drafted the reference.

## Audit items within a reference requirement

| BR | AR |
| --- | --- |
| BR-01 | AR-01, AR-03, AR-04, AR-05, AR-07 |
| BR-02 | AR-08 |
| BR-03 | AR-22 (in part) |
| BR-04 | AR-28 |
| BR-05 | AR-09, AR-31, AR-32, AR-33, AR-34, AR-35 |
| BR-06 | AR-40 |
| BR-07 | AR-10, AR-11 |
| BR-08 | AR-13, AR-14, AR-15 |
| BR-09 | AR-12, AR-36 |
| BR-10 | AR-42 |
| BR-11 | AR-16, AR-37 |
| BR-12 | AR-43 |
| BR-13 | AR-44 |
| BR-14 | AR-46, AR-47 |
| BR-15 | AR-17, AR-18, AR-19, AR-49 |
| BR-16 | AR-52, AR-53 |
| BR-17 | AR-54 |
| BR-18 | AR-21, AR-22 |
| BR-19 | AR-23 |
| BR-20 | AR-45, AR-48 |
| BR-21 | AR-63, AR-69 |
| BR-22 | AR-50, AR-51, AR-57 |
| BR-23 | AR-55, AR-56 |
| BR-25 | AR-58, AR-59, AR-60, AR-61 |
| BR-26 | AR-75 |
| BR-27 | AR-73, AR-74 |
| BR-28 | AR-76, AR-79 (in part) |
| BR-29 | AR-77 |
| BR-30 | AR-25, AR-26, AR-62 |
| BR-31 | AR-27, AR-64, AR-65, AR-66, AR-67, AR-68 |
| BR-32 | AR-70, AR-71 |
| BR-34 | AR-29, AR-30 |
| BR-35 | AR-83, AR-84, AR-85 |
| BR-36 | AR-80, AR-81 |
| BR-37 | AR-87, AR-88, AR-89 |
| BR-38 | AR-72 |

## Audit items with no reference requirement

| AR | Unit | Obligation |
| --- | --- | --- |
| AR-02 | 1.p1 | further companies can be brought onto the service |
| AR-06 | 1.p2 | a company cannot see another company's problems |
| AR-20 | 2.b2 | every flight has one dispatcher known as responsible for it |
| AR-24 | 2.b2, 4.b6 | a dispatcher can follow how each of their flights is going |
| AR-38 | 3.b1 | a company can run a few hundred drones |
| AR-39 | 3.b1 | a fleet can mix models from several manufacturers |
| AR-41 | 3.b2 | a company can have a few dozen charging pads |
| AR-58 | 4.b6 | a report that the load is not ready is accepted (the reference has "ready") |
| AR-78 | 6.b5 | one person can be responsible for hundreds of drones |
| AR-82 | 7.b1, 8.b5 | the service runs on a single server |
| AR-86 | 7.b1 | an interruption lasts no more than a few minutes |

## Reference requirements the audit does not state

| BR | What the audit has instead |
| --- | --- |
| BR-24 (does not count on a full battery's range) | 6.b4 listed as giving no obligation: the brief states the condition, not what the service does about it |
| BR-33 (does not itself call off, reroute or change a flight because of a closure) | only AR-52, AR-53: never chooses the drone or the way |
| BR-03 (each action only by the role given it) | only AR-22: only a dispatcher signs off |
| BR-12, "and by whom" | AR-43 has when, not by whom |
| BR-28, "flags the flight to its dispatchers" | AR-76: a missing report is not treated as arrived; AR-79: the responsible person learns what needs attention |

The audit lists 5.b3 as giving no obligation, as the reference does.
