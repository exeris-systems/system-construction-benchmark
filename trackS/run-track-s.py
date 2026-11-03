#!/usr/bin/env python3
"""Run Track S: the instruments' calibration, and later the subjects (decision register D-45 to D-48).

Modes:
  persona-control   ask each persona its fixed control questions (persona-control.yaml), in one
                    conversation per role, several times, and record every exchange
  persona-holdout   the same, with the held-out questions (persona-holdout.yaml)
  persona-holdout-2 the same, with the second held-out set (persona-holdout-2.yaml)
  persona-holdout-3 the same, with the third held-out set (persona-holdout-3.yaml)
  persona-holdout-4 the same, with the fourth held-out set (persona-holdout-4.yaml)

With --persona-check, each answer is checked sentence by sentence against the persona's notes
(persona-check-prompt.md) by the same model: a sentence stays only when the check keeps it and its
quoted source is found in the notes.

  grader-control    ask the grader to grade the cases of grader-control.yaml, whose verdicts are known
  grade             grade every answer of a completed persona run (--graded) with the grader

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
RUNS = HERE.parent / "runs" / "track-s"
CONTROL_FILE = "persona-control.yaml"
HOLDOUT_FILE = "persona-holdout.yaml"
CHECK_FILE = "persona-check-prompt.md"
GRADER_FILE = "grader-prompt.md"
GRADER_CONTROL_FILE = "grader-control.yaml"
# The persona passes a deciding run at this many passing answers of 72, with no contradiction (D-50).
PASS_AT = 65
# A quoted source shorter than this matches too much of any notes to show where a sentence comes from.
MIN_SOURCE_WORDS = 4
# What the persona says when the check drops every sentence of its answer.
NOTHING_LEFT = "I don't know."
# Each persona mode asks the questions of one set file and writes its answers under the mode's name.
QUESTION_SETS = {"persona-control": CONTROL_FILE, "persona-holdout": HOLDOUT_FILE,
                 "persona-holdout-2": "persona-holdout-2.yaml", "persona-holdout-3": "persona-holdout-3.yaml",
                 "persona-holdout-4": "persona-holdout-4.yaml"}
GRADE_MODES = ("grader-control", "grade")
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

def _is_structure(line):
    """Blank lines, bold sub-headings and rules are structure, not units."""
    return not line or line == "---" or (line.startswith("**") and line.endswith("**"))


def _section_units(heading, body):
    """The units of one section, numbered by kind in order of appearance."""
    number = heading.split(".", 1)[0].strip()
    counts = {"b": 0, "p": 0}
    for line in (raw.rstrip() for raw in body.strip().splitlines()):
        if _is_structure(line):
            continue
        kind = "b" if line.startswith("- ") else "p"
        counts[kind] += 1
        yield f"{number}.{kind}{counts[kind]}", ("## " + heading.strip(), line)


def parse_brief(text):
    """Split the brief into units: ('3.b2' -> (section heading, verbatim text))."""
    units = {}
    for section in re.split(r"^## ", text, flags=re.M)[1:]:
        heading, _, body = section.partition("\n")
        units.update(_section_units(heading, body))
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


def split_sentences(text):
    """The answer's sentences, in order: each non-empty line, split after a full stop, ! or ?."""
    sentences = []
    for line in text.splitlines():
        sentences += [s for s in re.split(r"(?<=[.!?])\s+", line.strip()) if s]
    return sentences


def parse_check(text, count):
    """The check's {verdict, source} for each of count sentences, or None if the reply is not exactly that."""
    try:
        reply = json.loads(text)
    except ValueError:
        return None
    # The entries may come bare, without the object around them; what is checked is the entries.
    items = reply.get("sentences") if isinstance(reply, dict) else reply
    if not isinstance(items, list) or len(items) != count:
        return None
    parsed = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("verdict"), str):
            return None
        verdict, source = item["verdict"].strip().upper(), item.get("source")
        if verdict not in ("KEEP", "DROP") or not isinstance(source, (str, type(None))):
            return None
        parsed.append({"verdict": verdict, "source": source})
    return parsed


def normalize(text):
    """Lower case, letters and digits only, single spaces: a quote matches however it is punctuated."""
    text = text.lower().replace("\u2019", "'").replace("\u2018", "'")
    return " ".join(re.sub(r"[^a-z0-9']+", " ", text).split())


def source_holds(sentence, source, notes):
    """Why a kept sentence's source does not hold, or None when it does."""
    if source == "DONT_KNOW":
        said = normalize(sentence)
        return None if ("don't know" in said or "do not know" in said) else "DONT_KNOW, but the sentence does not say so"
    if source == "FEELING":
        return None
    if not source or len(normalize(source).split()) < MIN_SOURCE_WORDS:
        return f"no source of at least {MIN_SOURCE_WORDS} words"
    return None if normalize(source) in normalize(notes) else "the source is not in the notes"


def parse_grade(text):
    """The grader's {verdict, contradicts, reason}, or None if the reply is not exactly that."""
    try:
        grade = json.loads(text)
    except ValueError:
        return None
    if not isinstance(grade, dict) or not isinstance(grade.get("verdict"), str):
        return None
    verdict = grade["verdict"].strip().upper()
    if verdict not in ("PASS", "FAIL") or not isinstance(grade.get("contradicts"), bool):
        return None
    return {"verdict": verdict, "contradicts": grade["contradicts"], "reason": str(grade.get("reason", ""))}


def render(units, ids):
    out, current = [], None
    for uid in ids:
        heading, line = units[uid]
        if heading != current:
            out.append(("\n" if out else "") + heading)
            current = heading
        out.append(line)
    return "\n".join(out)


def parse_control(text, name=CONTROL_FILE):
    """Read the restricted YAML of a question set file: role -> [{id, kind, question, expect}]."""
    roles, role, item = {}, None, None
    for raw in text.splitlines():
        if raw.lstrip().startswith("#") or not raw.strip():
            continue
        if not raw[0].isspace():
            role = raw.rstrip().rstrip(":")
            roles[role] = []
            continue
        entry = raw.strip()
        if entry.startswith("- "):
            item = {}
            roles[role].append(item)
            entry = entry[2:]
        key, sep, value = entry.partition(":")
        if role is None or item is None or not sep or not key.isidentifier():
            sys.exit(f"{name}: cannot read line: {raw!r}")
        item[key] = value.strip()
    return roles


# --- providers ------------------------------------------------------------------------------------

def role_problem(role, provider, model, rpm, max_tokens, temperature=None):
    """Why a role's settings cannot run, or None. Checked before a run directory exists."""
    if provider not in PROVIDERS:
        return f"{role}: unknown provider {provider!r}; known: {sorted(PROVIDERS)}"
    if "latest" in model:
        return f"{role}: {model}: use an exact identifier, not an alias"
    if rpm <= 0:
        return f"{role}: calls per minute must be positive, got {rpm}"
    if max_tokens <= 0:
        return f"{role}: max output tokens must be positive, got {max_tokens}"
    if temperature is not None and temperature < 0:
        return f"{role}: temperature must not be negative, got {temperature}"
    if not os.environ.get(PROVIDERS[provider]["key"]):
        return f"{role}: {PROVIDERS[provider]['key']} is not set"
    return None


class Client:
    """One provider and model for one role, paced below its per-minute limit."""

    def __init__(self, role, provider, model, rpm, max_tokens, recorder, temperature=None, seed=None):
        problem = role_problem(role, provider, model, rpm, max_tokens, temperature)
        if problem:
            raise RunFailed(problem)
        self.role, self.provider, self.model = role, provider, model
        self.temperature, self.seed = temperature, seed
        self.spec = PROVIDERS[provider]
        self.interval, self.max_tokens, self.recorder = 60 / rpm, max_tokens, recorder
        self.key = os.environ[self.spec["key"]]
        self.last = 0.0

    def _headers(self):
        if self.spec["kind"] == "openai":
            return {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
        return {"Content-Type": "application/json", "x-goog-api-key": self.key}

    def describe(self):
        """The model's own description, checked against the requested identifier; generates nothing."""
        url = f"{self.spec['base']}/models/{self.model}"
        request = urllib.request.Request(url, headers=self._headers())
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                headers, info = dict(response.headers), json.load(response)
        except ValueError as e:
            self.recorder.log("describe", self, "describe", error=f"invalid JSON: {e}")
            raise RunFailed(f"{self.role}: model check: response body is not JSON")
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            self.recorder.log("describe", self, "describe", headers=dict(e.headers), http=e.code, body=detail[:2000])
            raise RunFailed(f"{self.role}: model check: HTTP {e.code}: {detail[:500]}")
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
            self.recorder.log("describe", self, "describe", error=repr(e))
            raise RunFailed(f"{self.role}: model check: {e!r}")
        self.recorder.log("describe", self, "describe", headers=headers)
        if not isinstance(info, dict):
            raise RunFailed(f"{self.role}: model check: response is not a JSON object")
        name = info.get("name")
        served = info.get("id") or (name.removeprefix("models/") if isinstance(name, str) else None)
        if served != self.model:
            raise RunFailed(f"{self.role}: requested {self.model}, the provider describes {served!r}")
        return info

    def _body(self, system, turns):
        if self.spec["kind"] == "openai":
            messages = [{"role": "system", "content": system}]
            messages += [{"role": "assistant" if r == "model" else "user", "content": t} for r, t in turns]
            body = {"model": self.model, "messages": messages, "max_tokens": self.max_tokens}
            sampling = {"temperature": self.temperature, "random_seed": self.seed}
            return {**body, **{k: v for k, v in sampling.items() if v is not None}}
        config = {"maxOutputTokens": self.max_tokens, "temperature": self.temperature, "seed": self.seed}
        return {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": r, "parts": [{"text": t}]} for r, t in turns],
            "generationConfig": {k: v for k, v in config.items() if v is not None},
        }

    def _url(self):
        if self.spec["kind"] == "openai":
            return f"{self.spec['base']}/chat/completions"
        return f"{self.spec['base']}/models/{self.model}:generateContent"

    def _parse(self, payload):
        if self.spec["kind"] == "openai":
            choice = (payload.get("choices") or [{}])[0]
            content = (choice.get("message") or {}).get("content") or ""
            # A reasoning model answers in chunks; only its text chunks are the answer, never its thinking.
            if isinstance(content, list):
                content = "".join(c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text")
            return (content, choice.get("finish_reason"),
                    payload.get("id"), payload.get("model"), payload.get("usage"))
        candidate = (payload.get("candidates") or [{}])[0]
        text = "".join(p.get("text", "") for p in (candidate.get("content") or {}).get("parts", []))
        return (text, candidate.get("finishReason"), payload.get("responseId"),
                payload.get("modelVersion"), payload.get("usageMetadata"))

    def _pace(self):
        wait = self.last + self.interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self.last = time.monotonic()

    def _send(self, session, number, body):
        """POST until a response arrives; only infrastructure errors are retried, with the same body."""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            self._pace()
            request = urllib.request.Request(self._url(), data=body, method="POST", headers=self._headers())
            try:
                with urllib.request.urlopen(request, timeout=600) as response:
                    return dict(response.headers), json.load(response)
            except ValueError as e:
                # A success status with a body that is not JSON, or not UTF-8, is the provider's fault,
                # not the model's. ValueError covers both JSONDecodeError and UnicodeDecodeError.
                self.recorder.log(number, self, session, retry=attempt, error=f"invalid JSON: {e}")
                if attempt == MAX_ATTEMPTS:
                    raise RunFailed(f"{session}: response body is not JSON")
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
        raise RunFailed(f"{session}: no response")

    def call(self, session, system, turns, json_reply=False):
        # A subject runs on the provider's defaults, the one setting nobody can suspect of being chosen.
        # An instrument's temperature and seed are fixed by the procedure and sent, so its answers do
        # not depend on a default the provider may change.
        request = self._body(system, turns)
        if json_reply and self.spec["kind"] == "openai":
            request["response_format"] = {"type": "json_object"}
        elif json_reply:
            request["generationConfig"]["responseMimeType"] = "application/json"
        body = json.dumps(request, ensure_ascii=False, indent=1).encode()
        number = self.recorder.request(body)
        headers, payload = self._send(session, number, body)
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
    set_file = QUESTION_SETS[args.mode]
    control = parse_control(files[set_file], set_file)
    recorder = Recorder(out)
    persona = Client("persona", args.persona_provider, args.persona_model, args.persona_rpm,
                     args.persona_max_tokens, recorder, args.persona_temperature, args.persona_seed)
    run["instruments"] = {"persona": {"provider": persona.provider, "model": persona.model,
                                      "description": persona.describe()}}
    transcript = {}
    for repetition in range(1, args.repetitions + 1):
        for role, questions in control.items():
            system = files["persona-prompt.md"].replace("{{ROLE}}", ROLES[role]).replace("{{NOTES}}", notes[role])
            turns, answers = [], []
            for q in questions:
                session = f"{role}/{repetition}/{q['id']}"
                turns.append(("user", q["question"]))
                answer = persona.call(session, system, turns)
                record = {**q, "answer": answer}
                if args.persona_check:
                    record = {**q, **check(persona, files[CHECK_FILE], role, notes[role], session, q["question"], answer)}
                # The persona's history holds the answers the subject would hear, checked or not.
                turns.append(("model", record["answer"]))
                answers.append(record)
            transcript.setdefault(role, []).append({"repetition": repetition, "answers": answers})
    (out / f"{args.mode}.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=1) + "\n")


def check(persona, prompt, role, notes, session, question, draft):
    """Keep only the sentences of the draft that the check keeps and grounds in the notes; never rewrite one."""
    sentences = split_sentences(draft)
    system = prompt.replace("{{ROLE}}", ROLES[role]).replace("{{NOTES}}", notes)
    listed = "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, 1))
    asked = (f"Question: {question}\n\nThe answer has {len(sentences)} sentences:\n{listed}\n\n"
             f"Reply with exactly {len(sentences)} entries.")
    reply = persona.call(f"{session}/check", system, [("user", asked)], json_reply=True)
    items = parse_check(reply, len(sentences))
    if items is None:
        raise RunFailed(f"{session}/check: the reply is not one verdict and source for each of {len(sentences)} sentences")
    kept = []
    for sentence, item in zip(sentences, items):
        # A sentence the check keeps still goes when its source is not where the check says it is:
        # the quote is tested against the notes by the script, not taken on the check's word.
        item["dropped"] = None if item["verdict"] == "KEEP" else "check"
        if item["verdict"] == "KEEP":
            item["dropped"] = source_holds(sentence, item["source"], notes)
        if item["dropped"] is None:
            kept.append(sentence)
    return {"draft": draft, "sentences": sentences, "check": items,
            "answer": " ".join(kept) if kept else NOTHING_LEFT}


def grade_one(grader, prompt, role, notes, session, item, answer):
    system = prompt.replace("{{ROLE}}", ROLES[role]).replace("{{NOTES}}", notes)
    asked = (f"Kind: {item['kind']}\nQuestion: {item['question']}\nWhat the notes support: {item['expect']}\n\n"
             f"Answer:\n{answer}")
    grade = parse_grade(grader.call(session, system, [("user", asked)], json_reply=True))
    if grade is None:
        raise RunFailed(f"{session}: the grade is not a verdict, a contradicts flag and a reason")
    return grade


def summarize(grades):
    """Passing answers by kind, contradicting fact answers, and whether the persona passes (D-50)."""
    kinds = {}
    for g in grades:
        k = kinds.setdefault(g["kind"], {"passing": 0, "of": 0})
        k["of"] += 1
        k["passing"] += g["verdict"] == "PASS"
    passing = sum(k["passing"] for k in kinds.values())
    contradicting = [g["session"] for g in grades if g["kind"] == "fact" and g["contradicts"]]
    return {"byKind": kinds, "passing": passing, "of": len(grades), "contradictingFact": contradicting,
            "passes": len(grades) == 72 and passing >= PASS_AT and not contradicting}


def grader_control(args, files, notes, out, run, grader):
    cases = parse_control(files[GRADER_CONTROL_FILE], GRADER_CONTROL_FILE)
    results = []
    for role, items in cases.items():
        for case in items:
            grade = grade_one(grader, files[GRADER_FILE], role, notes[role], f"{role}/{case['id']}", case, case["answer"])
            results.append({"role": role, **case, "grade": grade,
                            "agrees": grade["verdict"] == case["verdict"].upper()})
    agreeing = sum(r["agrees"] for r in results)
    passed_contradiction = [r["id"] for r in results if r.get("contradicts") == "true" and r["grade"]["verdict"] == "PASS"]
    summary = {"agreeing": agreeing, "of": len(results), "passedContradictions": passed_contradiction}
    (out / "grader-control.json").write_text(json.dumps({"summary": summary, "cases": results},
                                                        ensure_ascii=False, indent=1) + "\n")


def grade_run(args, files, notes, out, run, grader):
    graded = json.loads(files["graded-run.json"])
    answers = json.loads(files["graded-answers.json"])
    grades = []
    for role, reps in answers.items():
        for rep in reps:
            for item in rep["answers"]:
                session = f"{role}/{rep['repetition']}/{item['id']}"
                grade = grade_one(grader, files[GRADER_FILE], role, notes[role], session, item, item["answer"])
                grades.append({"session": session, "id": item["id"], "kind": item["kind"], **grade})
    result = {"graded": {"run": str(args.graded), "mode": graded["mode"]}, "summary": summarize(grades),
              "grades": grades}
    (out / "grades.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=sorted(QUESTION_SETS) + list(GRADE_MODES))
    parser.add_argument("--persona-provider", default="mistral")
    parser.add_argument("--persona-model", help="exact model identifier; required by the persona modes")
    parser.add_argument("--persona-rpm", type=float, default=30)
    parser.add_argument("--persona-max-tokens", type=int, default=2048)
    parser.add_argument("--persona-temperature", type=float, help="sent when given; else the provider default")
    parser.add_argument("--persona-seed", type=int, help="sent when given; else none")
    parser.add_argument("--persona-check", action="store_true", help=f"check each answer against the notes ({CHECK_FILE})")
    parser.add_argument("--grader-provider", default="mistral")
    parser.add_argument("--grader-model", help="exact model identifier; required by the grading modes")
    parser.add_argument("--grader-rpm", type=float, default=20)
    parser.add_argument("--grader-max-tokens", type=int, default=1024)
    parser.add_argument("--grader-temperature", type=float, help="sent when given; else the provider default")
    parser.add_argument("--grader-seed", type=int, help="sent when given; else none")
    parser.add_argument("--graded", type=pathlib.Path, help="the completed persona run that mode grade grades")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--out", type=pathlib.Path, help="output directory (must not exist)")
    parser.add_argument("--dry-run", action="store_true", help="check inputs and print hashes; call nothing")
    args = parser.parse_args()
    grading = args.mode in GRADE_MODES

    names = ["world-brief.md", "brief-slices.yaml"]
    if grading:
        names += [GRADER_FILE] + ([GRADER_CONTROL_FILE] if args.mode == "grader-control" else [])
    else:
        names += ["persona-prompt.md", QUESTION_SETS[args.mode]] + ([CHECK_FILE] if args.persona_check else [])
    files = {name: (HERE / name).read_text() for name in names}
    files["run-track-s.py"] = pathlib.Path(__file__).read_text()

    units = parse_brief(files["world-brief.md"])
    slices, _ = parse_slices(files["brief-slices.yaml"])
    missing, unknown = sorted(set(units) - set(slices)), sorted(set(slices) - set(units))
    if missing or unknown:
        sys.exit(f"brief-slices.yaml does not match the brief: missing={missing} unknown={unknown}")
    notes = {role: render(units, [u for u in units if role in slices[u]]) for role in ROLES}

    if args.mode == "grade":
        if not args.graded:
            sys.exit("--graded is required by mode grade")
        graded_dir = args.graded.resolve()
        try:
            files["graded-run.json"] = (graded_dir / "run.json").read_text()
            graded = json.loads(files["graded-run.json"])
            files["graded-answers.json"] = (graded_dir / f"{graded['mode']}.json").read_text()
        except (OSError, ValueError, KeyError) as e:
            sys.exit(f"--graded {args.graded}: not a persona run record: {e}")
        if graded.get("status") != "completed" or graded.get("mode") not in QUESTION_SETS:
            sys.exit(f"--graded {args.graded}: only a completed persona run is graded")
        # The grader reads the notes the persona had; a changed brief would grade against other notes.
        for name in ("world-brief.md", "brief-slices.yaml"):
            if graded["inputSha256"].get(name) != sha256(files[name]):
                sys.exit(f"--graded {args.graded}: {name} has changed since that run")
    hashes = {name: sha256(text) for name, text in files.items()}

    if grading:
        role, settings = "grader", (args.grader_provider, args.grader_model, args.grader_rpm,
                                    args.grader_max_tokens, args.grader_temperature)
        if args.mode == "grader-control":
            cases = parse_control(files[GRADER_CONTROL_FILE], GRADER_CONTROL_FILE)
            calls = sum(len(c) for c in cases.values())
        else:
            calls = sum(len(rep["answers"]) for reps in json.loads(files["graded-answers.json"]).values() for rep in reps)
        plan = {"calls": calls}
    else:
        role, settings = "persona", (args.persona_provider, args.persona_model, args.persona_rpm,
                                     args.persona_max_tokens, args.persona_temperature)
        set_file = QUESTION_SETS[args.mode]
        control = parse_control(files[set_file], set_file)
        if set(control) != set(ROLES):
            sys.exit(f"{set_file} roles {sorted(control)} do not match {sorted(ROLES)}")
        plan = {"controlQuestions": {r: len(q) for r, q in control.items()},
                "calls": sum(len(q) for q in control.values()) * args.repetitions * (2 if args.persona_check else 1)}

    if args.dry_run:
        print(json.dumps({"inputSha256": hashes, **plan}, indent=2))
        return
    if not args.out:
        sys.exit("--out is required unless --dry-run")
    # A run record belongs under runs/ and nowhere else: the path is resolved before it is trusted.
    out = args.out.resolve()
    if not out.is_relative_to(RUNS.resolve()):
        sys.exit(f"--out must be a new directory under {RUNS}")
    # Everything that can stop the run before its first call is checked before its directory exists,
    # so a kept run directory always holds a run that started.
    if settings[1] is None:
        sys.exit(f"--{role}-model is required by mode {args.mode}")
    problem = role_problem(role, *settings)
    if problem:
        sys.exit(problem)
    if args.repetitions <= 0:
        sys.exit(f"--repetitions must be positive, got {args.repetitions}")
    out.mkdir(parents=True, exist_ok=False)
    args.out = out
    run = {"track": "S", "mode": args.mode, "status": "running", "started": now(),
           "parameters": {k: v for k, v in vars(args).items() if k not in ("out", "dry_run")},
           "inputSha256": hashes}
    try:
        if grading:
            recorder = Recorder(out)
            grader = Client("grader", args.grader_provider, args.grader_model, args.grader_rpm,
                            args.grader_max_tokens, recorder, args.grader_temperature, args.grader_seed)
            run["instruments"] = {"grader": {"provider": grader.provider, "model": grader.model,
                                             "description": grader.describe()}}
            (grader_control if args.mode == "grader-control" else grade_run)(args, files, notes, out, run, grader)
        else:
            persona_control(args, files, notes, args.out, run)
        run["status"] = "completed"
    except RunFailed as e:
        run["status"], run["failure"] = "failed", str(e)
    except BaseException as e:  # any other stop, an interrupt included, is recorded, then re-raised
        run["status"], run["failure"] = "failed", f"unexpected: {e!r}"
        raise
    finally:
        run["finished"] = now()
        (args.out / "run.json").write_text(json.dumps(run, indent=2, default=str) + "\n")
    print(f"{run['status']}: {args.out}")
    sys.exit(0 if run["status"] == "completed" else 1)


if __name__ == "__main__":
    main()
