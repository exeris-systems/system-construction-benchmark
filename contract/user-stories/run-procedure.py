#!/usr/bin/env python3
"""Run the user-story procedure: three persona interviews, then the analyst.

Each role is a separate model session that sees only its own input
(decision register D-36, D-43): personas see their slice of the world brief,
the interviewer sees the business section and role names, the analyst sees
only the transcripts. Every request and response is written to the output
directory verbatim, so the transcripts can be rebuilt from the raw record;
the directory is published unedited.

Requires only the Python standard library. The API key is read from
GEMINI_API_KEY and is never written to the output.
"""

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import socket
import sys
import time
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
END_MARKER = "END OF INTERVIEW"
RETRYABLE_HTTP = (429, 500, 502, 503, 504)
MAX_ATTEMPTS = 8

ROLES = {
    "technician": {
        "persona": "a fleet technician at one of the drone operating companies",
        "interviewee": "a fleet technician",
    },
    "dispatcher": {
        "persona": "a dispatcher at one of the drone operating companies",
        "interviewee": "a dispatcher",
    },
    "desk": {
        "persona": "a member of the airspace desk at the platform company",
        "interviewee": "a member of the platform's airspace desk",
    },
}
ROLE_NAMES = "fleet technician, dispatcher, airspace desk"


class RunFailed(Exception):
    """The run cannot produce a complete, untruncated record; it is kept, never resumed."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def parse_brief(text):
    """Split the brief into units: ('3.b2' -> (section heading, verbatim text))."""
    units = {}
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    for section in sections:
        heading, _, body = section.partition("\n")
        number = heading.split(".", 1)[0].strip()
        paragraphs = bullets = 0
        for block in re.split(r"\n\s*\n", body.strip()):
            for line in block.splitlines():
                line = line.rstrip()
                if not line or re.fullmatch(r"\*\*[^*]+\*\*", line) or line == "---":
                    continue
                if line.startswith("- "):
                    bullets += 1
                    units[f"{number}.b{bullets}"] = ("## " + heading.strip(), line)
                else:
                    paragraphs += 1
                    units[f"{number}.p{paragraphs}"] = ("## " + heading.strip(), line)
    return units


def parse_slices(text):
    """Read the restricted YAML of brief-slices.yaml."""
    slices, interviewer = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].rstrip()
        m = re.match(r'^interviewer:\s*\[(.*)\]$', line)
        if m:
            interviewer = [u.strip().strip('"') for u in m.group(1).split(",") if u.strip()]
            continue
        m = re.match(r'^\s+"([^"]+)":\s*\[(.*)\]$', line)
        if m:
            slices[m.group(1)] = [r.strip() for r in m.group(2).split(",") if r.strip()]
    return slices, interviewer


def render(units, ids):
    out, current = [], None
    for uid in ids:
        heading, line = units[uid]
        if heading != current:
            out.append(("\n" if out else "") + heading)
            current = heading
        out.append(line)
    return "\n".join(out)


class Gemini:
    def __init__(self, model, temperature, out, log):
        self.model, self.temperature, self.out, self.log = model, temperature, out, log
        self.count = 0
        self.key = os.environ.get("GEMINI_API_KEY")
        if not self.key:
            sys.exit("GEMINI_API_KEY is not set")
        (out / "requests").mkdir()
        (out / "responses").mkdir()

    def _post(self, body):
        request = urllib.request.Request(
            API.format(model=self.model), data=body, method="POST",
            headers={"Content-Type": "application/json", "x-goog-api-key": self.key})
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.load(response)

    def call(self, session, system, contents, max_output_tokens):
        config = {"maxOutputTokens": max_output_tokens}
        if self.temperature is not None:
            config["temperature"] = self.temperature
        body = json.dumps({
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": r, "parts": [{"text": t}]} for r, t in contents],
            "generationConfig": config,
        }, ensure_ascii=False, indent=1).encode()
        self.count += 1
        number = f"{self.count:03d}"
        (self.out / "requests" / f"{number}.json").write_bytes(body)

        # Network failures, timeouts, rate limits, and server errors are infrastructure:
        # the same request is sent again, its input never changes.
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                payload = self._post(body)
                break
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")
                if e.code not in RETRYABLE_HTTP or attempt == MAX_ATTEMPTS:
                    self._log(number, session, error=f"HTTP {e.code}", detail=detail)
                    raise RunFailed(f"{session}: HTTP {e.code}: {detail[:500]}")
                self._log(number, session, retry=attempt, error=f"HTTP {e.code}")
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
                if attempt == MAX_ATTEMPTS:
                    self._log(number, session, error=repr(e))
                    raise RunFailed(f"{session}: {e!r}")
                self._log(number, session, retry=attempt, error=repr(e))
            time.sleep(min(5 * 2 ** (attempt - 1), 300))

        (self.out / "responses" / f"{number}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
        candidates = payload.get("candidates") or []
        if not candidates:
            self._log(number, session, payload, error="no candidates")
            raise RunFailed(f"{session}: no candidates; promptFeedback={payload.get('promptFeedback')}")
        candidate = candidates[0]
        finish = candidate.get("finishReason")
        text = "".join(p.get("text", "") for p in (candidate.get("content") or {}).get("parts", []))
        self._log(number, session, payload)
        # Anything but a natural stop — token limit, safety, recitation — is a truncated or
        # altered answer; accepting it would make a technically damaged run canonical.
        if finish != "STOP":
            raise RunFailed(f"{session}: finishReason={finish}")
        if not text.strip():
            raise RunFailed(f"{session}: empty response")
        return text.strip()

    def _log(self, number, session, payload=None, **extra):
        entry = {"call": number, "session": session, "time": now()}
        if payload is not None:
            candidate = (payload.get("candidates") or [{}])[0]
            entry.update({
                "responseId": payload.get("responseId"),
                "modelVersion": payload.get("modelVersion"),
                "finishReason": candidate.get("finishReason"),
                "usage": payload.get("usageMetadata"),
            })
        entry.update(extra)
        self.log.write(json.dumps(entry) + "\n")
        self.log.flush()


def interview(gemini, role, interviewer_system, persona_system, max_turns, max_tokens, record):
    asker = [("user", "The interviewee is ready. Ask your first question.")]
    answerer = []
    transcript = []
    for turn in range(1, max_turns + 1):
        question = gemini.call(f"{role}/interviewer/{turn}", interviewer_system, asker, max_tokens)
        if END_MARKER in question:
            record.update(ending="ended_by_interviewer", endingMessage=question)
            return transcript
        asker.append(("model", question))
        answerer.append(("user", question))
        answer = gemini.call(f"{role}/persona/{turn}", persona_system, answerer, max_tokens)
        answerer.append(("model", answer))
        asker.append(("user", answer))
        transcript.append((question, answer))
    record.update(ending="max_turns")
    return transcript


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", required=True, help="exact, versioned API model identifier")
    parser.add_argument("--temperature", type=float,
                        help="omit to use the provider default (nothing is sent)")
    parser.add_argument("--max-turns", type=int, default=30, help="questions per interview")
    parser.add_argument("--max-output-tokens-turn", type=int, default=8192)
    parser.add_argument("--max-output-tokens-analyst", type=int, default=65536)
    parser.add_argument("--out", type=pathlib.Path, help="output directory (must not exist)")
    parser.add_argument("--dry-run", action="store_true", help="print slices and hashes; call nothing")
    args = parser.parse_args()
    if "latest" in args.model:
        sys.exit("--model must be a versioned identifier, not an alias")

    files = {name: (HERE / name).read_text() for name in (
        "world-brief.md", "brief-slices.yaml", "persona-prompt.md",
        "interviewer-prompt.md", "analyst-prompt.md")}
    files["run-procedure.py"] = pathlib.Path(__file__).read_text()

    units = parse_brief(files["world-brief.md"])
    slices, interviewer_units = parse_slices(files["brief-slices.yaml"])
    missing, unknown = sorted(set(units) - set(slices)), sorted(set(slices) - set(units))
    if missing or unknown or not interviewer_units or set(interviewer_units) - set(units):
        sys.exit(f"brief-slices.yaml does not match the brief: missing={missing} unknown={unknown}")
    for uid, roles in slices.items():
        if set(roles) - set(ROLES):
            sys.exit(f"{uid}: unknown role in {roles}")

    order = list(units)
    notes = {role: render(units, [u for u in order if role in slices[u]]) for role in ROLES}
    business = render(units, interviewer_units)
    hashes = {name: sha256(text) for name, text in files.items()}

    if args.dry_run:
        for role in ROLES:
            print(f"===== persona notes: {role} =====\n{notes[role]}\n")
        print(f"===== interviewer business context =====\n{business}\n")
        print(json.dumps(hashes, indent=2))
        return

    if not args.out:
        sys.exit("--out is required unless --dry-run")
    args.out.mkdir(parents=True, exist_ok=False)
    run = {
        "procedure": "user-story procedure v2 (decision register D-36, D-43)",
        "status": "running",
        "started": now(),
        "model": args.model,
        "temperature": args.temperature if args.temperature is not None else "provider default (not sent)",
        "maxTurns": args.max_turns,
        "maxOutputTokens": {"turn": args.max_output_tokens_turn, "analyst": args.max_output_tokens_analyst},
        "inputSha256": hashes,
        "interviews": {},
    }

    try:
        with open(args.out / "calls.jsonl", "w") as log:
            gemini = Gemini(args.model, args.temperature, args.out, log)
            transcripts = []
            for role, names in ROLES.items():
                persona_system = files["persona-prompt.md"].replace(
                    "{{ROLE}}", names["persona"]).replace("{{NOTES}}", notes[role])
                interviewer_system = (files["interviewer-prompt.md"]
                                      .replace("{{BUSINESS}}", business)
                                      .replace("{{ROLES}}", ROLE_NAMES)
                                      .replace("{{ROLE}}", names["interviewee"]))
                record = run["interviews"].setdefault(role, {})
                transcript = interview(gemini, role, interviewer_system, persona_system,
                                       args.max_turns, args.max_output_tokens_turn, record)
                record["questions"] = len(transcript)
                text = f"# Interview — {names['interviewee']}\n\n" + "\n\n".join(
                    f"**Interviewer:** {q}\n\n**Interviewee:** {a}" for q, a in transcript) + "\n"
                (args.out / f"interview-{role}.md").write_text(text)
                transcripts.append(text)

            analysis = gemini.call("analyst", files["analyst-prompt.md"],
                                   [("user", "\n\n---\n\n".join(transcripts))],
                                   args.max_output_tokens_analyst)
            (args.out / "analyst-output.md").write_text(analysis + "\n")
        run["status"] = "completed"
    except RunFailed as e:
        run["status"] = "failed"
        run["failure"] = str(e)
    finally:
        run["finished"] = now()
        (args.out / "run.json").write_text(json.dumps(run, indent=2) + "\n")
    print(f"{run['status']}: {args.out}")
    sys.exit(0 if run["status"] == "completed" else 1)


if __name__ == "__main__":
    main()
