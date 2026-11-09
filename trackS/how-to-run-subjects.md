---
title: "How to run a Track S subject"
type: howto
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-11-09
---

# How to run a Track S subject

Covers one subject run in the script series and its judging. The instruments must be calibrated
first ([`how-to-calibrate-persona.md`](how-to-calibrate-persona.md)); the subjects, variants and
judges are those of [`procedure.md`](procedure.md). Run from the repository root, with
`ANTHROPIC_API_KEY` and `GEMINI_API_KEY` set; neither is written to the output.

1. Check the inputs without calling anything:

   ```sh
   python3 -I trackS/run-track-s.py subject-naive --subject-provider anthropic --subject-model claude-opus-5-5 --persona-provider gemini --persona-model gemini-3.5-flash-lite --dry-run
   ```

2. Run the subject, with the persona as it was calibrated. `subject-naive` makes one subject call per
   message and one persona call per question, at most 90; `subject-instructed` makes up to 30
   questions per role, then one analyst call:

   ```sh
   python3 -I trackS/run-track-s.py subject-naive --subject-provider anthropic --subject-model claude-opus-5-5 --persona-provider gemini --persona-model gemini-3.5-flash-lite --persona-temperature 0 --persona-seed 1 --persona-max-tokens 8192 --persona-rpm 10 --out runs/track-s/YYYY-MM-DD-subject-naive-claude-opus-5-5-1
   ```

   The record's `subject.json` holds every exchange, the requirements message, the items read from
   it, whether it was unreadable, and the variant's measures.

3. Judge the run twice: by the judge of the other vendor, which scores, and by the judge of the
   subject's own family, which is recorded unscored. For a Claude subject:

   ```sh
   python3 -I trackS/run-track-s.py judge --judged runs/track-s/YYYY-MM-DD-subject-naive-claude-opus-5-5-1 --judge-provider gemini --judge-model gemini-4-argon --judge-temperature 0 --judge-seed 1 --judge-max-tokens 32768 --judge-rpm 5 --out runs/track-s/YYYY-MM-DD-judge-gemini-4-argon-subject-naive-claude-opus-5-5-1
   python3 -I trackS/run-track-s.py judge --judged runs/track-s/YYYY-MM-DD-subject-naive-claude-opus-5-5-1 --judge-provider anthropic --judge-model claude-opus-5-5 --judge-effort high --judge-max-tokens 32768 --judge-rpm 5 --out runs/track-s/YYYY-MM-DD-judge-claude-opus-5-5-subject-naive-claude-opus-5-5-1
   ```

   For a Gemini subject the two judges swap roles. Each `judgement.json` says whether it is
   `scored`, and gives the judgement and its `score`.

4. Classify the run's questions as follow-ups, with the same two judges in the same roles; mode
   `follow-up` makes one call per role that was asked more than one question:

   ```sh
   python3 -I trackS/run-track-s.py follow-up --judged runs/track-s/YYYY-MM-DD-subject-naive-claude-opus-5-5-1 --judge-provider gemini --judge-model gemini-4-argon --judge-temperature 0 --judge-seed 1 --judge-max-tokens 32768 --judge-rpm 5 --out runs/track-s/YYYY-MM-DD-follow-up-gemini-4-argon-subject-naive-claude-opus-5-5-1
   ```

   `follow-ups.json` gives each question's label, `follow_up_ratio`, and whether it is `scored`.

5. Commit every output directory unedited.
