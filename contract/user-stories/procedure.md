# User-story procedure

Version: 2
Decision register: D-36, D-37, D-43. Version 1 (single self-played writer) is frozen at tag `us-procedure-v1`.

## Design

Stories come from interviews between separate model sessions with asymmetric information, so the interviewer has to find things out rather than recall what it already knows.

| Role | Sees | Produces |
| --- | --- | --- |
| Persona — fleet technician, dispatcher, airspace desk (one session each) | `persona-prompt.md` + its own slice of `world-brief.md` | answers |
| Interviewer (one session per interview) | `interviewer-prompt.md` + brief §1 + the role names | questions |
| Analyst | `analyst-prompt.md` + the three transcripts | stories and open questions |
| Mapping instance | `mapping-prompt.md` + the analyst's output + requirements + profile + brief + seeding declaration | mapping |

Slices are a mechanical selection of brief units, listed in `brief-slices.yaml`; no text is written for them. The only words added outside the brief are the role descriptions in `run-procedure.py` (e.g. "a fleet technician at one of the drone operating companies"). `brief-seeding.md` therefore applies to every slice unchanged. `brief-seeding.md` is never given to any role that produces stories.

The interviewer's §1 contains a listed constraint ("Each company's fleet, jobs, sites, and problems are its own business"), so the interviewer knows it as business context. The mapping instance treats a story that rests on it as `brief_seeded` whether the interviewer or the interviewee raised it.

## Role assignment — fixed before the run

| Role | Vendor | Model | Channel | Notes |
| --- | --- | --- | --- | --- |
| Contract author's working models | Anthropic | Claude | Claude Code | reference row |
| Interviewer, personas | Google | Gemini 3.5 Flash Lite | Gemini API, `run-procedure.py` | excluded from Track S by exact model id |
| Analyst | Google | Gemini 3.8 Flash | Gemini API, `run-procedure.py` | excluded from Track S by exact model id |
| Mapping instance | Anthropic | Claude Opus | fresh session | shares the author's vendor; it sees the requirements anyway |
| Neutrality auditor 1 (D-03) | OpenAI | GPT-6 | chat, temporary chat | ran the two v1 writer runs; an auditor sees only the DOD, in a session without memory |
| Neutrality auditor 2 (D-03) | Anthropic | Claude Opus | fresh session | **shares the author's vendor — disclosed in every report** |

The parameters are fixed here before the run and passed to the script; the model version each response reports is recorded per call.

| Parameter | Value |
| --- | --- |
| `--model` (interviewer, personas) | `gemini-3.5-flash-lite` |
| `--analyst-model` | `gemini-3.8-flash` |

The API offers no dated variant of either model; the `-latest` aliases (e.g. `gemini-flash-latest`, currently routed to `gemini-3.8-flash`) are not used, because their target can change. The model version each response reports is recorded per call.
| temperature, thinking level | provider defaults: nothing is sent, so no value is chosen by the author |
| `--rpm` / `--analyst-rpm` | 14 / 4 calls per minute, below the per-minute limits |
| `--max-turns` | 25 |
| `--max-output-tokens-turn` | 8192 |
| `--max-output-tokens-analyst` | 65536 |

**Why two models.** The run uses the Gemini API free tier, whose limits on the contract author's account on 2026-10-22 were:

| Model | Requests per minute | Tokens per minute | Requests per day |
| --- | --- | --- | --- |
| Gemini 3.8 Flash | 5 | 250K | 20 |
| Gemini 3.5 Flash Lite | 15 | 250K | 500 |
| Gemini 3.1 Flash Lite | 15 | 250K | 500 |
| Gemma 4 31B | 30 | 16K | 14.4K |

Interviews need up to 3 × 25 × 2 = 150 calls, more than Gemini 3.8 Flash allows in a day; a run spread over several days could not be resumed (below) and could change model version midway. Gemma 4 31B's 16K tokens per minute cannot hold the analyst's input. The split is forced by these limits, not chosen for an outcome: interviews on Gemini 3.5 Flash Lite (150 calls, 30% of its daily limit), the single analyst call on Gemini 3.8 Flash, where story quality is decided. Before the first content call the script reads both models' token limits and refuses to start if a setting exceeds them.

Start the canonical run on a fresh daily limit; `--dry-run` makes no calls and is the only test. The brief and all prompts are public, so data use on the free tier for training discloses nothing.

## Run

```sh
export GEMINI_API_KEY=...            # never written to the output
# from the repository root
python3 -I contract/user-stories/run-procedure.py --dry-run --model MODEL    # check slices and hashes
python3 -I contract/user-stories/run-procedure.py --model MODEL --out runs/user-stories/<date>
```

The output directory is committed unedited:

- `requests/NNN.json` and `responses/NNN.json` — every request and response verbatim, so every transcript can be rebuilt from the raw record;
- `calls.jsonl` — per call: response id, reported model version, finish reason, token usage, retries;
- `run.json` — status (`completed` or `failed`), inputs with SHA-256 hashes, parameters, timing;
- `interview-*.md` and `analyst-output.md` — the transcripts and the analyst's output.

- **No human in the loop.** Nobody reads, edits, or steers between calls; the script runs end to end.
- **Errors.** Network failures, timeouts, rate limits, and server errors are retried with the same request and logged. A response whose finish reason is anything but `STOP` — a token limit, a safety block, recitation — fails the run, because a truncated or altered answer must not become canonical. A failed run is kept in the output with `status: failed`, and the procedure is run again from the start in a new directory; a failed run is never edited or resumed.
- **One canonical run.** The first run that completes is canonical. Further runs are replication, published but not used as input.

Reports state: "stories produced by Gemini Flash through the Gemini API; model version as reported per call; full repeatability is not guaranteed, but the run can be repeated with one command from the public inputs".
