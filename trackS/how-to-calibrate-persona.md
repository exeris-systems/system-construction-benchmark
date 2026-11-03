---
title: "How to calibrate the Track S persona"
type: howto
visibility: public
owning-repo: system-construction-benchmark
status: active
last-verified: 2026-10-22
---

# How to calibrate the Track S persona

Covers the persona instrument only; the judge and the subjects have procedures of their own. Run
from the repository root. The key comes from the environment and is never written to the output.
Each run makes 72 calls, about 130,000 tokens, against the provider's per-minute limits.

1. Check the inputs without calling anything:

   ```sh
   python3 -I trackS/run-track-s.py persona-control --persona-model ministral-8b-2512 --dry-run
   ```

2. Run the calibration. Set the key on its own line, or in front of the command; `export` followed by
   the command on one line exports the command's words instead of running it.

   ```sh
   export MISTRAL_API_KEY=...
   python3 -I trackS/run-track-s.py persona-control --persona-model ministral-8b-2512 --out runs/track-s/YYYY-MM-DD-persona-control
   ```

3. Commit the output directory unedited, and record the verdict against the criteria of
   [`procedure.md`](procedure.md) in [`calibration-log.md`](calibration-log.md).

   From draft 6, every run takes the persona's provider, model, temperature, seed and output limit,
   which leaves room for a thinking model's reasoning tokens; with the check pass it makes 144 calls,
   without it 72:

   ```sh
   python3 -I trackS/run-track-s.py persona-control --persona-provider gemini --persona-model gemini-3.5-flash-lite --persona-temperature 0 --persona-seed 1 --persona-max-tokens 8192 --persona-rpm 10 --persona-check --out runs/track-s/YYYY-MM-DD-persona-control-check
   ```

   From draft 6, a persona run is graded by the grader, not by hand, into a run of its own:

   ```sh
   python3 -I trackS/run-track-s.py grade --graded runs/track-s/YYYY-MM-DD-persona-control-check --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grade-persona-control-check
   ```

   The grader is calibrated before it grades anything, 36 calls:

   ```sh
   python3 -I trackS/run-track-s.py grader-control --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grader-control
   ```

4. With the persona's prompts and model and the grader's prompt frozen, run the current draft's
   held-out set once, the same way, and grade it; the grade decides. For draft 6 that is
   `persona-holdout-4`.

   ```sh
   python3 -I trackS/run-track-s.py persona-holdout-4 --persona-provider gemini --persona-model gemini-3.5-flash-lite --persona-temperature 0 --persona-seed 1 --persona-max-tokens 8192 --persona-rpm 10 --out runs/track-s/YYYY-MM-DD-persona-holdout-4
   python3 -I trackS/run-track-s.py grade --graded runs/track-s/YYYY-MM-DD-persona-holdout-4 --grader-provider gemini --grader-model gemini-3.8-flash --grader-temperature 0 --grader-seed 1 --grader-max-tokens 8192 --grader-rpm 10 --out runs/track-s/YYYY-MM-DD-grade-persona-holdout-4
   ```
