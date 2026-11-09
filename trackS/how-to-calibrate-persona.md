---
title: "How to calibrate the Track S persona and judges"
type: howto
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-11-09
---

# How to calibrate the Track S persona and judges

Covers the instruments: the persona, the grader of its calibration, and the two judges. The
subjects have procedures of their own. Run from the repository root. Keys come from the environment
and are never written to the output: `GEMINI_API_KEY` for the persona, the grader and the judge of
Claude subjects, `ANTHROPIC_API_KEY` for the judge of Gemini subjects. Set a key on its own line, or
in front of the command; `export` followed by the command on one line exports the command's words
instead of running it.

1. Check the inputs of any mode without calling anything; `--dry-run` prints the SHA-256 of every
   input and the number of calls:

   ```sh
   python3 -I trackS/run-track-s.py persona-control --persona-provider gemini --persona-model gemini-3.5-flash-lite --dry-run
   ```

2. Calibrate the grader before it grades anything, on the 36 cases of `grader-control.yaml`, 36
   calls:

   ```sh
   python3 -I trackS/run-track-s.py grader-control --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grader-control
   ```

3. Run the persona on the control set, 72 calls (144 with `--persona-check`), then grade it into a
   run of its own, 72 calls:

   ```sh
   python3 -I trackS/run-track-s.py persona-control --persona-provider gemini --persona-model gemini-3.5-flash-lite --persona-temperature 0 --persona-seed 1 --persona-max-tokens 8192 --persona-rpm 10 --out runs/track-s/YYYY-MM-DD-persona-control
   python3 -I trackS/run-track-s.py grade --graded runs/track-s/YYYY-MM-DD-persona-control --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grade-persona-control
   ```

4. With the persona's prompts and model and the grader's prompt frozen, run the current draft's
   held-out set once, the same way, and grade it; the grade decides, as `summary.passes` in
   `grades.json`. The persona of version 4 is the one version 3 calibrated, on `persona-holdout-5`:

   ```sh
   python3 -I trackS/run-track-s.py persona-holdout-5 --persona-provider gemini --persona-model gemini-3.5-flash-lite --persona-temperature 0 --persona-seed 1 --persona-max-tokens 8192 --persona-rpm 10 --out runs/track-s/YYYY-MM-DD-persona-holdout-5
   python3 -I trackS/run-track-s.py grade --graded runs/track-s/YYYY-MM-DD-persona-holdout-5 --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grade-persona-holdout-5
   ```

5. Calibrate each judge on the mutant contracts of `judge-control.yaml`, 18 calls each: the judge of
   Claude subjects on the Gemini API, the judge of Gemini subjects on the Anthropic API. The verdict
   is `summary.passes` in `judge-control.json`, and every judgement that is not exact lists its
   differences under `disagreements`:

   ```sh
   python3 -I trackS/run-track-s.py judge-control --judge-provider gemini --judge-model gemini-4-argon --judge-temperature 0 --judge-seed 1 --judge-max-tokens 32768 --judge-rpm 5 --out runs/track-s/YYYY-MM-DD-judge-control-gemini-4-argon
   python3 -I trackS/run-track-s.py judge-control --judge-provider anthropic --judge-model claude-opus-5-5 --judge-effort high --judge-max-tokens 32768 --judge-rpm 5 --out runs/track-s/YYYY-MM-DD-judge-control-claude-opus-5-5
   ```

6. Commit every output directory unedited, and record its verdict against the
   criteria of [`procedure.md`](procedure.md) in [`calibration-log.md`](calibration-log.md).
