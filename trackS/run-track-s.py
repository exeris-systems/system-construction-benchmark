#!/usr/bin/env python3
"""Run Track S: the instruments' calibration, and later the subjects (decision register D-45 to D-48).

Modes:
  persona-control   ask each persona its fixed control questions (persona-control.yaml), in one
                    conversation per role, several times, and record every exchange

Each role names a provider and a model. Every request and response is written to the output
directory verbatim, with every response header that reports a rate limit and the body of every 429,
so the run record documents the quotas it ran under. The output is committed unedited.

Requires only the Python standard library. API keys are read from the environment
(MISTRAL_API_KEY, GEMINI_API_KEY) and are never written to the output.
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
RETRYABLE_HTTP = (429, 500, 502, 503, 504)
MAX_ATTEMPTS = 8

PROVIDERS = {
    "mistral": {"kind": "openai", "base": "https://api.mistral.ai/v1", "key": "MISTRAL_API_KEY"},
    "gemini": {"kind": "gemini", "base": "https://generativelanguage.googleapis.com/v1beta",
               "key": "GEMINI_API_KEY"},
}
# The finish reasons that mean the model stopped on its own. Anything else — a token limit, a
# safety block — is a truncated or altered answer, and a run that accepted one would carry it.
NATURAL_STOP = {"openai": {"stop"}, "gemini": {"STOP"}}

ROLES = {
    "technician": "a fleet technician at one of the drone operating companies",
    "dispatcher": "a dispatcher at one of the drone operating companies",
    "desk": "a member of the airspace desk at the platform company",
}


class RunFailed(Exception):
    """The run cannot produce a complete, untruncated record; it is kept, never resumed."""


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


# --- the brief and its slices ---------------------------------------------------------------------

def parse_brief(text):
    """Split the brief into units: ('3.b2' -> (section heading, verbatim text))."""
    units = {}
    for section in re.split(r"^## ", text, flags=re.M)[1:]:
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


def parse_control(text):
    """Read the restricted YAML of persona-control.yaml: role -> [{id, kind, question, expect}]."""
    roles, role, item = {}, None, None
    for raw in text.splitlines():
        line = raw.split(" #", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line:
            continue
        m = re.match(r"^(\w+):$", line)
        if m:
            role = m.group(1)
            roles[role] = []
            continue
        m = re.match(r"^\s+-\s+(\w+):\s*(.+)$", line) or re.match(r"^\s+(\w+):\s*(.+)$", line)
        if not m or role is None:
            sys.exit(f"persona-control.yaml: cannot read line: {raw!r}")
        if line.lstrip().startswith("- "):
            item = {}
            roles[role].append(item)
        item[m.group(1)] = m.group(2).strip()
    return roles


# --- providers ------------------------------------------------------------------------------------

class Client:
    """One provider and model for one role, paced below its per-minute limit."""

    def __init__(self, role, provider, model, rpm, max_tokens, recorder):
        if provider not in PROVIDERS:
            sys.exit(f"{role}: unknown provider {provider!r}; known: {sorted(PROVIDERS)}")
        if "latest" in model:
            sys.exit(f"{role}: {model}: use an exact identifier, not an alias")
        self.role, self.provider, self.model = role, provider, model
        self.spec = PROVIDERS[provider]
        self.interval, self.max_tokens, self.recorder = 60 / rpm, max_tokens, recorder
        self.key = os.environ.get(self.spec["key"])
        if not self.key:
            sys.exit(f"{role}: {self.spec['key']} is not set")
        self.last = 0.0

    def _headers(self):
        if self.spec["kind"] == "openai":
            return {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
        return {"Content-Type": "application/json", "x-goog-api-key": self.key}

    def describe(self):
        """The model's own description; this endpoint generates nothing."""
        url = f"{self.spec['base']}/models/{self.model}"
        request = urllib.request.Request(url, headers=self._headers())
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)

    def _body(self, system, turns):
        if self.spec["kind"] == "openai":
            messages = [{"role": "system", "content": system}]
            messages += [{"role": "assistant" if r == "model" else "user", "content": t} for r, t in turns]
            return {"model": self.model, "messages": messages, "max_tokens": self.max_tokens}
        return {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": r, "parts": [{"text": t}]} for r, t in turns],
            "generationConfig": {"maxOutputTokens": self.max_tokens},
        }

    def _url(self):
        if self.spec["kind"] == "openai":
            return f"{self.spec['base']}/chat/completions"
        return f"{self.spec['base']}/models/{self.model}:generateContent"

    def _parse(self, payload):
        if self.spec["kind"] == "openai":
            choice = (payload.get("choices") or [{}])[0]
            return ((choice.get("message") or {}).get("content") or "", choice.get("finish_reason"),
                    payload.get("id"), payload.get("model"), payload.get("usage"))
        candidate = (payload.get("candidates") or [{}])[0]
        text = "".join(p.get("text", "") for p in (candidate.get("content") or {}).get("parts", []))
        return (text, candidate.get("finishReason"), payload.get("responseId"),
                payload.get("modelVersion"), payload.get("usageMetadata"))

    def call(self, session, system, turns):
        # Temperature and similar settings are never sent: the provider default is the one value
        # nobody can suspect of being chosen.
        body = json.dumps(self._body(system, turns), ensure_ascii=False, indent=1).encode()
        number = self.recorder.request(body)
        for attempt in range(1, MAX_ATTEMPTS + 1):
            wait = self.last + self.interval - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self.last = time.monotonic()
            request = urllib.request.Request(self._url(), data=body, method="POST", headers=self._headers())
            try:
                with urllib.request.urlopen(request, timeout=600) as response:
                    headers = dict(response.headers)
                    payload = json.load(response)
                break
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")
                self.recorder.log(number, self, session, headers=dict(e.headers), http=e.code,
                                  retry=attempt, body=detail if e.code == 429 else detail[:2000])
                # An exhausted quota is an infrastructure error (program plan §9.1): the run stops,
                # is kept, and is never charged to a subject.
                if e.code not in RETRYABLE_HTTP or attempt == MAX_ATTEMPTS:
                    raise RunFailed(f"{session}: HTTP {e.code}: {detail[:500]}")
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
                self.recorder.log(number, self, session, retry=attempt, error=repr(e))
                if attempt == MAX_ATTEMPTS:
                    raise RunFailed(f"{session}: {e!r}")
            time.sleep(min(5 * 2 ** (attempt - 1), 300))

        self.recorder.response(number, payload)
        text, finish, response_id, version, usage = self._parse(payload)
        self.recorder.log(number, self, session, headers=headers, finish=finish,
                          responseId=response_id, modelVersion=version, usage=usage)
        if finish not in NATURAL_STOP[self.spec["kind"]]:
            raise RunFailed(f"{session}: finish reason {finish}")
        if not text.strip():
            raise RunFailed(f"{session}: empty response")
        return text.strip()


class Recorder:
    """Writes the raw record: requests/, responses/, calls.jsonl."""

    def __init__(self, out):
        self.out, self.count = out, 0
        (out / "requests").mkdir()
        (out / "responses").mkdir()
        self.calls = open(out / "calls.jsonl", "w")

    def request(self, body):
        self.count += 1
        number = f"{self.count:04d}"
        (self.out / "requests" / f"{number}.json").write_bytes(body)
        return number

    def response(self, number, payload):
        (self.out / "responses" / f"{number}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n")

    def log(self, number, client, session, headers=None, **fields):
        entry = {"call": number, "role": client.role, "provider": client.provider,
                 "model": client.model, "session": session, "time": now()}
        if headers is not None:
            entry["rateLimitHeaders"] = {k: v for k, v in headers.items() if "ratelimit" in k.lower()}
        entry.update({k: v for k, v in fields.items() if v is not None})
        self.calls.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self.calls.flush()


# --- modes ----------------------------------------------------------------------------------------

def persona_control(args, files, notes, out, run):
    control = parse_control(files["persona-control.yaml"])
    if set(control) != set(ROLES):
        sys.exit(f"persona-control.yaml roles {sorted(control)} do not match {sorted(ROLES)}")
    recorder = Recorder(out)
    persona = Client("persona", args.persona_provider, args.persona_model, args.persona_rpm,
                     args.persona_max_tokens, recorder)
    run["instruments"] = {"persona": {"provider": persona.provider, "model": persona.model,
                                      "description": persona.describe()}}
    transcript = {}
    for repetition in range(1, args.repetitions + 1):
        for role, questions in control.items():
            system = files["persona-prompt.md"].replace("{{ROLE}}", ROLES[role]).replace("{{NOTES}}", notes[role])
            turns, answers = [], []
            for q in questions:
                turns.append(("user", q["question"]))
                answer = persona.call(f"{role}/{repetition}/{q['id']}", system, turns)
                turns.append(("model", answer))
                answers.append({**q, "answer": answer})
            transcript.setdefault(role, []).append({"repetition": repetition, "answers": answers})
    (out / "persona-control.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=1) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=["persona-control"])
    parser.add_argument("--persona-provider", default="mistral")
    parser.add_argument("--persona-model", required=True, help="exact model identifier")
    parser.add_argument("--persona-rpm", type=float, default=30)
    parser.add_argument("--persona-max-tokens", type=int, default=2048)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--out", type=pathlib.Path, help="output directory (must not exist)")
    parser.add_argument("--dry-run", action="store_true", help="check inputs and print hashes; call nothing")
    args = parser.parse_args()

    names = ["world-brief.md", "brief-slices.yaml", "persona-prompt.md", "persona-control.yaml"]
    files = {name: (HERE / name).read_text() for name in names}
    files["run-track-s.py"] = pathlib.Path(__file__).read_text()

    units = parse_brief(files["world-brief.md"])
    slices, _ = parse_slices(files["brief-slices.yaml"])
    missing, unknown = sorted(set(units) - set(slices)), sorted(set(slices) - set(units))
    if missing or unknown:
        sys.exit(f"brief-slices.yaml does not match the brief: missing={missing} unknown={unknown}")
    notes = {role: render(units, [u for u in units if role in slices[u]]) for role in ROLES}
    hashes = {name: sha256(text) for name, text in files.items()}
    control = parse_control(files["persona-control.yaml"])

    if args.dry_run:
        print(json.dumps({"inputSha256": hashes,
                          "controlQuestions": {r: len(q) for r, q in control.items()},
                          "calls": sum(len(q) for q in control.values()) * args.repetitions}, indent=2))
        return
    if not args.out:
        sys.exit("--out is required unless --dry-run")
    args.out.mkdir(parents=True, exist_ok=False)
    run = {"track": "S", "mode": args.mode, "status": "running", "started": now(),
           "parameters": {k: v for k, v in vars(args).items() if k not in ("out", "dry_run")},
           "inputSha256": hashes}
    try:
        persona_control(args, files, notes, args.out, run)
        run["status"] = "completed"
    except RunFailed as e:
        run["status"], run["failure"] = "failed", str(e)
    finally:
        run["finished"] = now()
        (args.out / "run.json").write_text(json.dumps(run, indent=2, default=str) + "\n")
    print(f"{run['status']}: {args.out}")
    sys.exit(0 if run["status"] == "completed" else 1)


if __name__ == "__main__":
    main()
