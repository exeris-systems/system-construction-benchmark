# Mapping instance — prompt and run procedure

Version: 2 (draft)
Part of the published user-story procedure (decision register D-36, D-37). Runs after the analyst (`procedure.md`), before any story is assigned as `provenance`.

---

## Run procedure

- **Model:** as assigned in the role table of `procedure.md`. Fresh session, no memory, no custom instructions, no web, no tools beyond the attached input.
- **Input, exactly:** this prompt; the analyst's output (`analyst-output.md`: stories and its question list), unedited; `system-requirements.yaml`; `domain-profile.md`; `world-brief.md`; `brief-seeding.md`.
- **Not given:** DOD, oracle, mutants, arms, preregistration, the interview transcripts. The mapping judges stories as they will reach Track S, not how they were produced.
- **Output:** published in full, unedited.
- **Author review:** the contract author reviews the mapping afterwards. Every change the author makes is recorded as an override with a one-sentence reason and published next to the original mapping. The author never edits the mapping file itself.

---

## Prompt

You are reviewing the traceability between a set of user stories and a set of system requirements. The user stories were written independently by an analyst who never saw the requirements, from interviews with simulated users whose knowledge came from a description of their world only. Your job is to report honestly how well they support the requirements, not to make them fit.

The attached files are:

- `stories` — the user stories, each with an `id`;
- `system-requirements.yaml` — the requirements, each with an `id`;
- `domain-profile.md` — background to the requirements;
- `world-brief.md` — the description of the world; the simulated users each saw only a part of it, and the analyst saw none of it;
- `brief-seeding.md` — the brief sentences that state constraints or needs rather than facts, with the requirements each one points to.

### Main risk

You can see the requirements. With them in front of you, it is easy to find some link between almost any story and almost any requirement. A mapping built from such links is worthless. Map a story to a requirement only when an analyst who had **not** seen the requirement would arrive at it from the story. When in doubt, do not map.

### Task 1 — Map each story

For every story, record:

- **maps_to:** the requirements it supports, each with a strength:
  - `direct` — the need behind the requirement is stated in the story;
  - `partial` — the story supports part of the requirement, or the requirement follows only together with another story; name the part.
- **carrier:** for each `direct` mapping, the one sentence of the story that carries it.
- **brief_seeded:** `true` when the need comes from a sentence listed in `brief-seeding.md`; give the brief section.
- **paraphrases_brief:** the brief section, when the story repeats a specific sentence of the brief (any kind of sentence, listed or not); otherwise `null`.
- **scope:** one of
  - `in_contract` — the story maps to at least one requirement;
  - `excluded` — the story asks for something that the brief's §8 or the requirements exclude; name which;
  - `contradicts` — the story asks for something that a requirement or a constraint in the brief rules out (for example, software choosing on the user's behalf); name the requirement or brief section;
  - `unaddressed` — the story states a need that no requirement covers and nothing excludes.

### Task 2 — Coverage of each requirement

For every requirement, record:

- **status:** `covered_independent` (at least one `direct` mapping from a story that is not `brief_seeded`), `covered_seeded_only` (direct mappings only from `brief_seeded` stories), `partial_only`, or `uncovered`;
- **primary_story:** for covered requirements, the strongest story, preferring stories that are not `brief_seeded`;
- **other_stories:** the rest;
- for `partial_only` and `uncovered`: a **hypothesis**, one of
  - `brief_too_thin` — the brief gives no facts from which a user would feel this need;
  - `technical_not_user` — the requirement describes internal behaviour that users would not express as a need;
  - `writer_missed` — the brief contains the relevant facts, but no story uses them;
  - `other` — explain in one sentence.

Do not write new stories. Do not edit stories or requirements. Do not suggest wording. An uncovered requirement is a finding to report, not a gap to fill.

### Task 3 — Summary

- counts per requirement status and per story scope;
- the share of `in_contract` stories that are `brief_seeded`, and the share that paraphrase the brief;
- every `contradicts` and `unaddressed` story, listed, each with one sentence;
- the analyst's questions that, if answered, would most likely have changed coverage.

### Output format

```yaml
stories:
  - id: US-07
    maps_to:
      - { requirement: SR-SAGA-01, strength: direct }
      - { requirement: SR-SAGA-02, strength: partial, part: "release of earlier reservations" }
    carrier:
      SR-SAGA-01: "..."
    brief_seeded: false
    brief_section: null
    paraphrases_brief: null
    scope: in_contract

requirements:
  - id: SR-SAGA-01
    status: covered_independent
    primary_story: US-07
    other_stories: [US-12]
  - id: SR-X-04
    status: uncovered
    hypothesis: technical_not_user

summary:
  ...
```
