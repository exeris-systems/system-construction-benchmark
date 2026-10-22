# Brief seeding declaration

Applies to: `world-brief.md` v1.0
Visibility: published with the Track S procedure; **never given to a persona or a subject** (it names requirement IDs). It applies unchanged to every persona slice, because slices are selections of brief units (`brief-slices.yaml`).

Every sentence of the brief is one of three kinds:

- **fact** — describes the world; a derived item that rests on it counts as independent;
- **constraint** — a business or legal limit the users impose; a derived item that restates it is `brief_seeded`;
- **seeded need** — states something users want; a derived item that rests on it is `brief_seeded`.

Only constraints and seeded needs are listed. Every other sentence is a fact. In Track S (D-46, D-47), a requirement in a subject's derived contract that traces to a listed sentence is read as `brief_seeded`, and its recall is reported apart from items that trace only to facts; the declaration is not a scoring input of the judge.

| Brief | Sentence | Kind | Points to |
| --- | --- | --- | --- |
| §1 | Each company's fleet, jobs, sites, and problems are its own business. | constraint | SR-TEN-01, SR-TEN-04 |
| §2 | Fleet technicians … add new drones to the fleet, retire old ones, set up charging pads …, take drones out of service for repairs and put them back, and send drones to charge. | constraint | SR-TEN-02, SR-REG-01, SR-INV-05, SR-CHARGE-01 |
| §2 | … they sign off a flight before it leaves. A dispatcher can call off a flight. | constraint | SR-MIS-01, SR-TEN-02 |
| §2 | The desk … has no business looking into any one company's operations. | constraint | SR-TEN-01, SR-TEN-03 |
| §2 | When a closure is entered, the desk wants to know how much disruption it caused across customers. | seeded need | SR-TEN-03 |
| §3 | Pads are never lent to another company. | constraint | SR-CHARGE-02 |
| §3 | Regulators can ask a company to show how its drones have been looked after. | constraint | SR-REC-01 |
| §4 | The companies' policy is that software never chooses a drone or a way for them. | constraint | SR-MIS-01, D-33 |
| §4 | Dispatchers do want help finding out which of their drones could get to where a job starts. | seeded need | SR-ROUTE-02 |
| §7 | … systems … need to hear about what happens to its drones and jobs. | seeded need | SR-X-01, SR-X-02 |
| §7 | The companies accept a few minutes of interruption. | constraint | anti-requirements (HA) |
| §8 | (whole section) | constraint | `anti-requirements.md` |

**Synchronisation rule.** Track S receives the brief, so it must not be penalised for scope it never saw. `anti-requirements.md` items are of two kinds:

- **user-visible** (analytical reports, external identity, i18n, compliance, retention and erasure, backups, HA, multi-node, accounts and passwords, notifications to people, route planning and drone choice, remote piloting, weather, billing, tenant onboarding) — each appears in brief §8 in the users' words;
- **technical** (autoscaling, second-level cache, no broker required, no geometric computation, no throughput criterion at declared scale) — these never appear in the brief, and a Track S contract that adds them is not penalised for it.

A change to a user-visible anti-requirement requires the matching change to brief §8, and the brief hash changes.
