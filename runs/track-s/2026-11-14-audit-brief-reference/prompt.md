# Audit prompt

Given on 2026-11-14 to a separate agent (Claude Code, Claude Opus 5.5), with no other context. The
agent reported that it read only the two files named. Below is the task as given, with file paths
shortened to the repository; the prompt went on to give the output shape of
`audit-requirements.yaml` and asked for a short reply naming any ambiguous unit.

> You are doing an independent requirements extraction from a product brief, as an audit. Your list
> will be compared with an existing reference list that you must NOT see.
>
> Read exactly two files and nothing else in the repository:
>
> - `trackS/world-brief.md` (the brief)
> - `trackS/brief-slices.yaml` (only to learn how the brief's paragraphs and bullets are numbered as
>   "units", e.g. "1.p1", "2.b3", "6.b4")
>
> Do NOT open, grep or list any other file: in particular not `trackS/brief-requirements.yaml`,
> `contract/*`, `docs/*`, `runs/*`, `trackS/judge-control.yaml` or any other trackS file. Do not
> search the repo.
>
> Task: write down every obligation of the service — what it must or must not do — that the users
> described in the brief could state from what the brief says. Rules:
>
> - Each obligation rests only on brief units you name; add no value, state, mechanism, technology
>   or number the brief does not give.
> - Write each in plain user language, one checkable obligation per item (split compound ones).
> - Include prohibitions when the brief states them as the users' expectation of the service. Brief
>   §8 is a list of user-visible anti-requirements: list them separately, not as requirements.
> - Separately list every unit that gives no checkable obligation of the service, and say why.
> - Be exhaustive: go unit by unit through §1–§7 so no unit is skipped.
