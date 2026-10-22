---
title: "Campaign 1 anti-requirements"
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# Campaign 1 anti-requirements

These properties are not required and must not become hidden `PASS` criteria. They are of two kinds (`trackS/brief-seeding.md`, synchronisation rule).

## User-visible

Each appears in `trackS/world-brief.md` §8 in the users' words; changing one here requires the matching change there.

- Management or analytical reports, exports, and dashboards.
- Login through an external identity provider.
- i18n.
- Compliance with any regulation, or a compliance audit. Regulations are cited as provenance only (`domain-profile.md` §9).
- Data retention and erasure: no retention schedule, deletion on request, or pseudonymisation of history.
- Backups.
- High availability or multi-node deployment.
- User accounts, sign-up, passwords, or user management. Staff identities are issued outside the system; each request carries a signed token (D-23).
- Notifying people by e-mail, text message, or phone. Domain events go only to the event webhook (D-18).
- Route planning or automatic choice of a drone. The system validates the dispatcher's choice and never makes it (D-33).
- Remote piloting or real-time flight control. Flight control is on the drone (`domain-profile.md` §2).
- Weather data or forecasts.
- Billing, invoicing, or pricing of deliveries and inspections.
- Onboarding of new operating companies or management of tenants through the system.

## Technical

Not stated in the brief; Track S is not penalised for adding them.

- Autoscaling.
- A second-level cache.
- A message broker, queue, or coordinator. Every boundary is HTTP (`domain-profile.md` §3).
- Geometric or geospatial computation. Position is a location or a corridor; coordinates, if present, are descriptive (`domain-profile.md` §4, §6).
- Throughput or latency at the declared scale. Scale is data context (`domain-profile.md` §7); the harness does not apply fleet-scale load during functional gates.
