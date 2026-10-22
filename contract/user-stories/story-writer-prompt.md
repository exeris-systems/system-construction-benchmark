# Story writer — prompt and run procedure

Version: 0.2 (draft)
Part of the published user-story procedure (decision register D-36). The prompt below is given verbatim, together with `world-brief.md` and nothing else. `brief-seeding.md` is never given to the writer.

---

## Role assignment — fixed before any run

| Role | Sees | Vendor | Model | Notes |
| --- | --- | --- | --- | --- |
| Contract author's working models | everything | Anthropic | Claude (incl. coding agent) | reference row |
| Story writer | prompt + brief | OpenAI | GPT-6, ChatGPT interface | excluded from Track S by exact model id |
| Second story writer | — | — | — | not used: it would take the only vendor left for the audit |
| Mapping instance | stories + SR + brief + `brief-seeding.md` | Anthropic | Claude Opus, fresh session | shares the author's vendor; it sees SR anyway |
| Neutrality auditor 1 (D-03) | DOD only | Google | Gemini 4 Argon | not the writer's vendor |
| Neutrality auditor 2 (D-03) | DOD only | Anthropic | Claude Opus, fresh session | **shares the author's vendor — disclosed in every report** |

The table is completed and published, with its hash, before the writer runs. Model labels are recorded exactly as the interface shows them on the day of the run.

### Isolation of chat-interface runs

Every role runs in a chat interface, not through an API, so isolation is procedural:

- no memory, no reference to past chats, no custom instructions or personal context — temporary or incognito chat in every interface;
- no web search, no connected apps, no file tools beyond the attached input;
- record the model label exactly as the interface shows it, the date, and the interface; export the full transcript.

Reports state: "runs through vendor chat interfaces; vendor system prompts unknown; exact model snapshots not pinned". A replication through the vendors' APIs is the stronger form and is invited.

---

## Run procedure

- **Model:** as assigned above. Record the exact model identifier, date, interface, and settings. This model identifier is excluded from Track S.
- **Input:** this prompt + `world-brief.md`. No other files, no tools, no web access.
- **Session:** one fresh session. The full transcript, including the interviews, is published.
- **No follow-up from the author.** Any question the writer asks is recorded and not answered. If the writer stops to ask, it is told to proceed on its own best assumptions and to record them.

---

## Prompt

You are a requirements analyst at the start of a software project. Your task is to find out what the future users of a service need, and to write it down as user stories.

The attached document describes the world these users work in: the companies, the people, their equipment, their work, and the conditions they face. It does not describe the service. Nobody has designed it yet.

### Step 1 — Interviews

Conduct one interview with each kind of user named in the document: fleet technician, dispatcher, and the platform's airspace desk. You play both the interviewer and the interviewee. The interviewee knows their job well, speaks plainly, and has no technical background in software.

Cover at least these topics in every interview, in your own words:

- an ordinary working day, from start to end;
- the worst day of the last few months, and what made it bad;
- what they check by hand today because they do not trust it;
- what they are afraid a new service would do wrong;
- what they need to know right after something has gone wrong;
- who they hand work to, and who hands work to them.

Follow up wherever an answer is vague. Write the interviews out in full.

### Step 2 — User stories

From the interviews, write user stories. Each story:

- is told from one user's point of view, in that user's language;
- says what happened or what situation the user is in, what they need, and what they fear will happen without it;
- describes outcomes the user cares about, not procedures, screens, or steps;
- contains no numbers that the user would not naturally say, no technical terms, no names of technologies, and no proposals for how the service should work inside;
- is three to eight sentences long.

Write stories for ordinary days and for bad days. Where users would disagree with each other, write both stories; do not resolve the conflict. Where a story rests on an assumption that the document does not settle, state the assumption in one sentence.

Aim for forty to sixty stories. Prefer more distinct situations over more variations of one situation.

### Output format

```yaml
- id: US-01
  user: dispatcher            # fleet technician | dispatcher | airspace desk
  title: short title in the user's words
  story: >
    ...
  fear: >
    what goes wrong for this user if the need is not met
  assumption: null            # or one sentence
  interview_ref: dispatcher, worst day
```

After the stories, list every question you would have asked the people who wrote the attached document, if you could. Do not wait for answers.
