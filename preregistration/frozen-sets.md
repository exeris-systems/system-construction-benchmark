---
title: Frozen sets
type: reference
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-11-09
---

# Frozen sets

Each frozen set has a ruleset-protected tag and an independent timestamp (program plan §12.2, decision register D-42).

| Tag | Commit | Contents | Independent timestamp |
| --- | --- | --- | --- |
| `us-procedure-v1` | `0890c97ac4404a762948f77c1e5defd5faf2d61c` | User-story procedure: `contract/user-stories/` — world brief v1.0, brief seeding declaration, story-writer and mapping prompts, role assignment | Software Heritage visit 2026-10-22T08:56:19Z, snapshot `swh:1:snp:6550393745e54a5c82fb86965e52af114aaba7e6` (contains `refs/tags/us-procedure-v1` → release `abb2fb70c771a733786abfae39c6846ce4964a8f` → `0890c97`) |
| `us-procedure-v2` | `ed49771f6f07eea0e5cf44d51adf7a67ed3ba3b2` | User-story procedure v2: `contract/user-stories/` — world brief v1.0 (unchanged), brief slices, persona, interviewer, analyst and mapping prompts, `run-procedure.py`, role assignment and parameters (`gemini-3.5-flash-lite`, `gemini-3.8-flash`) | Software Heritage visit 2026-10-22T10:23:02Z, snapshot `swh:1:snp:b0db1a61c493a419dd6a0acb323558867cb83cec` (contains `refs/tags/us-procedure-v2` → release `f6e252b95b56bf8f4459c5dfbc9eae0b5ba45b20` → `ed49771`) |
| `us-procedure-v3` | `8015bcdf855cccf112e9de4ccff3af4f340b2070` | Track S procedure v3: `trackS/` — world brief v1.0 (unchanged), brief slices, seeding declaration, persona prompt and check prompt, control set and the five held-out sets, grader prompt and grader control set, the pilots' interviewer and analyst prompts, `run-track-s.py` and its tests, the procedure, how-to and calibration log | Software Heritage visit 2026-11-03T17:43:32Z, snapshot `swh:1:snp:6cfe6b703d8db79d2bce9dfea803dc79de0738c6` (contains `refs/tags/us-procedure-v3` → release `342a044f25fd0de272c148557e228249cd4c0d37` → `8015bcd`) |
| `us-procedure-v4` | `f164d87094a4e0026de9e91cec75e01806e24186` | Track S procedure v4: `trackS/` — the persona and grader of v3, unchanged, and the judges: `gemini-4-argon` for Claude subjects and `claude-opus-5-5` for Gemini subjects, the judge prompt and its mutant contracts, `run-track-s.py` and its tests (D-55, D-56) | Software Heritage visit 2026-11-09T10:21:50Z, snapshot `swh:1:snp:bdd5f22592900a6da9a39f82708e0fef81f62ee0` (contains `refs/tags/us-procedure-v4` → release `012689b519c44a0fb669e774babb73e147566085` → `f164d87`) |
| `us-procedure-v5` | `e514a6670ecf022b40915fa39223244a3bdd778d` | Track S procedure v5: `trackS/` — the instruments of v4, unchanged, and the subjects' prompts: S-naive, and the S-instructed interviewer and analyst; the subject modes; the follow-up classifier's prompt and its labelled pairs (D-57 to D-59) | Software Heritage visit 2026-11-09T12:59:00Z, snapshot `swh:1:snp:97bea50c75c9d99af216e2e554d9d2bce341f684` (contains `refs/tags/us-procedure-v5` → release `e6e1a19ccc3e8bd4ff45b56cea34741110546b12` → `e514a66`) |
| `us-procedure-v6` — pending | pending | Track S procedure v6: `trackS/` — the instruments and subjects of v5, unchanged, and the ceiling: mode `ceiling`, in which both judges judge the whole brief as a contract (D-60) | pending — added when the set is tagged |
