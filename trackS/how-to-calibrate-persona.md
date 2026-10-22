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

4. With the persona prompt and model frozen, run the current draft's held-out set once, the same
   way; its verdict decides. For draft 4 that is `persona-holdout-2` on `mistral-small-2603`, whose
   limit of 20,000 tokens per minute calls for a rate of 10 requests per minute.

   ```sh
   python3 -I trackS/run-track-s.py persona-holdout-2 --persona-model mistral-small-2603 --persona-rpm 10 --out runs/track-s/YYYY-MM-DD-persona-holdout-2
   ```
