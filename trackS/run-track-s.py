#!/usr/bin/env python3
"""Run Track S: the instruments' calibration, and later the subjects (decision register D-45 to D-48).

Modes:
  persona-control   ask each persona its fixed control questions (persona-control.yaml), in one
                    conversation per role, several times, and record every exchange
  persona-holdout   the same, with the held-out questions (persona-holdout.yaml)
  persona-holdout-2 the same, with the second held-out set (persona-holdout-2.yaml)
  persona-holdout-3 the same, with the third held-out set (persona-holdout-3.yaml)
  persona-holdout-4 the same, with the fourth held-out set (persona-holdout-4.yaml)
  persona-holdout-5 the same, with the fifth held-out set (persona-holdout-5.yaml)

With --persona-check, each answer is checked sentence by sentence against the persona's notes
(persona-check-prompt.md) by the same model: a sentence stays only when the check keeps it and its
quoted source is found in the notes.

  grader-control    ask the grader to grade the cases of grader-control.yaml, whose verdicts are known
  grade             grade every answer of a completed persona run (--graded) with the grader

  judge-control     ask a judge to judge the mutant contracts of judge-control.yaml, whose coverage of
                    the reference requirements is known, several times
  ceiling           judge the whole brief, every unit an item, as a contract, several times: the
                    reference requirements no subject can derive from what the personas know

  subject-naive     run a subject in S-naive: one conversation in which it may ask the personas
  subject-instructed run a subject in S-instructed: one interview per role, then the analyst
  judge             judge the contract of a completed subject run (--judged) with one judge

  follow-up-control ask a judge to classify the pairs of follow-up-control.yaml, whose labels are
                    known, several times
  follow-up         classify every question of a completed subject run (--judged) as a follow-up
                    of the answer before it or not, with one judge

Each role names a provider and a model. Every request and response is written to the output
directory verbatim, with every response header that reports a rate limit and the body of every 429,
so the run record documents the quotas it ran under. The output is committed unedited.

Requires only the Python standard library. API keys are read from the environment
(MISTRAL_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY) and are never written to the output.
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
JUDGE_FILE = "judge-prompt.md"
JUDGE_CONTROL_FILE = "judge-control.yaml"
FOLLOW_UP_FILE = "follow-up-prompt.md"
FOLLOW_UP_CONTROL_FILE = "follow-up-control.yaml"
# A classifier passes when it agrees with at least this many of the 40 labelled pairs, in every
# repetition (D-59).
FOLLOW_UP_PASS_AT = 37
# The judge's inputs from the contract, named by their path from the repository root.
REFERENCE_FILE = "contract/system-requirements.yaml"
ANTI_FILE = "contract/anti-requirements.md"
SUBJECT_MODES = {"subject-naive": "subject-naive-prompt.md",
                 "subject-instructed": ("subject-interviewer-prompt.md", "subject-analyst-prompt.md")}
# The limits of D-57: they end the questioning, never the run.
MAX_QUESTIONS_NAIVE = 90
MAX_QUESTIONS_INTERVIEW = 30
END_MARKER = "END OF INTERVIEW"
ROLE_NAMES = "fleet technician, dispatcher, airspace desk"
INTERVIEWEES = {"technician": "a fleet technician", "dispatcher": "a dispatcher",
                "desk": "a member of the platform's airspace desk"}
# The turns the script itself writes to a subject; each is part of what every subject receives.
NAIVE_START = "Begin."
NAIVE_NO_ROLE = "There is no such role. The roles are technician, dispatcher and desk."
NAIVE_NO_MORE = "You cannot ask any more questions. Write the requirements now."
INTERVIEW_START = "The interviewee is ready. Ask your first question."
ANALYST_START = "Write the requirements."
ASK_LINE = re.compile(r"ASK\s+([A-Za-z]+)\s*:\s*(\S.*)")
COVERAGE = ("covered", "partial", "missing")
CLASSES = ("reference", "user_visible", "technical", "other")
# The persona passes a deciding run at this many passing answers of 72, with no contradiction (D-50).
PASS_AT = 65
# A quoted source shorter than this matches too much of any notes to show where a sentence comes from.
MIN_SOURCE_WORDS = 4
# What the persona says when the check drops every sentence of its answer.
NOTHING_LEFT = "I don't know."
# Each persona mode asks the questions of one set file and writes its answers under the mode's name.
QUESTION_SETS = {"persona-control": CONTROL_FILE, "persona-holdout": HOLDOUT_FILE,
                 "persona-holdout-2": "persona-holdout-2.yaml", "persona-holdout-3": "persona-holdout-3.yaml",
                 "persona-holdout-4": "persona-holdout-4.yaml", "persona-holdout-5": "persona-holdout-5.yaml"}
GRADE_MODES = ("grader-control", "grade")
JUDGE_MODES = ("judge-control", "judge", "ceiling", "follow-up-control", "follow-up")
RETRYABLE_HTTP = (429, 500, 502, 503, 504)
MAX_ATTEMPTS = 8

PROVIDERS = {
    "mistral": {"kind": "openai", "base": "https://api.mistral.ai/v1", "key": "MISTRAL_API_KEY"},
    "gemini": {"kind": "gemini", "base": "https://generativelanguage.googleapis.com/v1beta",
               "key": "GEMINI_API_KEY"},
    "anthropic": {"kind": "anthropic", "base": "https://api.anthropic.com/v1", "key": "ANTHROPIC_API_KEY"},
}
ANTHROPIC_VERSION = "2026-10-21"
# Sampling settings the provider refuses for every current model; depth is set by effort instead.
NO_SAMPLING = {"anthropic"}
# The finish reasons that mean the model stopped on its own. Anything else — a token limit, a
# safety block — is a truncated or altered answer, and a run that accepted one would carry it.
NATURAL_STOP = {"openai": {"stop"}, "gemini": {"STOP"}, "anthropic": {"end_turn"}}

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

def role_problem(role, provider, model, rpm, max_tokens, temperature=None, seed=None, effort=None):
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
    if PROVIDERS[provider]["kind"] in NO_SAMPLING and (temperature is not None or seed is not None):
        return f"{role}: {provider} takes no temperature or seed; set its effort instead"
    if effort is not None and PROVIDERS[provider]["kind"] != "anthropic":
        return f"{role}: effort is an {sorted(NO_SAMPLING)} setting, not one of {provider}"
    if not os.environ.get(PROVIDERS[provider]["key"]):
        return f"{role}: {PROVIDERS[provider]['key']} is not set"
    return None


class Client:
    """One provider and model for one role, paced below its per-minute limit."""

    def __init__(self, role, provider, model, rpm, max_tokens, recorder, temperature=None, seed=None, effort=None):
        problem = role_problem(role, provider, model, rpm, max_tokens, temperature, seed, effort)
        if problem:
            raise RunFailed(problem)
        self.role, self.provider, self.model = role, provider, model
        self.temperature, self.seed, self.effort = temperature, seed, effort
        self.spec = PROVIDERS[provider]
        self.interval, self.max_tokens, self.recorder = 60 / rpm, max_tokens, recorder
        self.key = os.environ[self.spec["key"]]
        self.last = 0.0

    def _headers(self):
        if self.spec["kind"] == "openai":
            return {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
        if self.spec["kind"] == "anthropic":
            return {"Content-Type": "application/json", "x-api-key": self.key, "anthropic-version": ANTHROPIC_VERSION}
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
            messages += [{"role": "assistant" if r == "model" else "user", "content": t} for r, t, *_ in turns]
            body = {"model": self.model, "messages": messages, "max_tokens": self.max_tokens}
            sampling = {"temperature": self.temperature, "random_seed": self.seed}
            return {**body, **{k: v for k, v in sampling.items() if v is not None}}
        if self.spec["kind"] == "anthropic":
            # A model turn goes back with every block the model returned, its thinking unchanged: the
            # API reads a conversation whose earlier turns were edited as a different one.
            messages = [{"role": "assistant" if r == "model" else "user", "content": raw[0] if raw else t}
                        for r, t, *raw in turns]
            body = {"model": self.model, "max_tokens": self.max_tokens, "system": system, "messages": messages}
            if self.effort is not None:
                body["output_config"] = {"effort": self.effort}
            return body
        config = {"maxOutputTokens": self.max_tokens, "temperature": self.temperature, "seed": self.seed}
        return {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": r, "parts": [{"text": t}]} for r, t, *_ in turns],
            "generationConfig": {k: v for k, v in config.items() if v is not None},
        }

    def _url(self):
        if self.spec["kind"] == "openai":
            return f"{self.spec['base']}/chat/completions"
        if self.spec["kind"] == "anthropic":
            return f"{self.spec['base']}/messages"
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
        if self.spec["kind"] == "anthropic":
            # Thinking blocks are the model's reasoning, never its answer; only text blocks are kept.
            text = "".join(b.get("text", "") for b in payload.get("content") or [] if b.get("type") == "text")
            return (text, payload.get("stop_reason"), payload.get("id"), payload.get("model"), payload.get("usage"))
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

    def turn(self, text):
        """The model turn to append to a conversation after the last call, as the provider needs it back."""
        return ("model", text, self.last_content) if self.last_content else ("model", text)

    def call(self, session, system, turns, json_reply=False, schema=None):
        # A subject runs on the provider's defaults, the one setting nobody can suspect of being chosen.
        # An instrument's temperature and seed are fixed by the procedure and sent, so its answers do
        # not depend on a default the provider may change.
        request = self._body(system, turns)
        if json_reply and self.spec["kind"] == "openai":
            request["response_format"] = {"type": "json_object"}
        elif json_reply and self.spec["kind"] == "anthropic":
            # Without a schema the reply is held to JSON by the prompt alone, as with the other providers.
            if schema is not None:
                request.setdefault("output_config", {})["format"] = {"type": "json_schema", "schema": schema}
        elif json_reply:
            request["generationConfig"]["responseMimeType"] = "application/json"
        body = json.dumps(request, ensure_ascii=False, indent=1).encode()
        number = self.recorder.request(body)
        headers, payload = self._send(session, number, body)
        self.recorder.response(number, payload)
        text, finish, response_id, version, usage = self._parse(payload)
        self.last_content = payload.get("content") if self.spec["kind"] == "anthropic" else None
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
    # A reply of the wrong shape is asked for once more, as the same request; both are recorded.
    items = None
    for attempt in ("check", "check-again"):
        reply = persona.call(f"{session}/{attempt}", system, [("user", asked)], json_reply=True)
        items = parse_check(reply, len(sentences))
        if items is not None:
            break
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


# --- the judge ------------------------------------------------------------------------------------

def parse_reference(text):
    """The parameters and requirements of system-requirements.yaml: ([(name, value)], [(id, requirement)])."""
    parameters, requirements, section, current, block = [], [], None, None, None
    for raw in text.splitlines():
        if raw and not raw[0].isspace():
            section = raw.split(":")[0]
            continue
        line = raw.split("  #")[0].rstrip() if section == "parameters" else raw.rstrip()
        if section == "parameters" and line.strip():
            name, _, value = line.strip().partition(":")
            parameters.append((name.strip(), value.strip()))
        elif section == "requirements":
            stripped = line.strip()
            if stripped.startswith("- id:"):
                current, block = {"id": stripped[len("- id:"):].strip(), "lines": []}, False
                requirements.append(current)
            elif current is not None and stripped == "requirement: >":
                block = True
            elif current is not None and block and len(line) - len(line.lstrip()) >= 6:
                current["lines"].append(stripped)
            elif stripped:
                block = False
    return parameters, [(r["id"], " ".join(r["lines"])) for r in requirements]


def parse_anti(text):
    """The bullets of anti-requirements.md: (user-visible, technical)."""
    lists, current = {"User-visible": [], "Technical": []}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = lists.get(line[3:].strip())
        elif current is not None and line.startswith("- "):
            current.append(line[2:].strip())
    return lists["User-visible"], lists["Technical"]


def judge_system(prompt, files):
    parameters, requirements = parse_reference(files[REFERENCE_FILE])
    out_of_scope, technical = parse_anti(files[ANTI_FILE])
    return (prompt.replace("{{REFERENCE}}", "\n\n".join(f"{i}: {r}" for i, r in requirements))
            .replace("{{PARAMETERS}}", "\n".join(f"{n} = {v}" for n, v in parameters))
            .replace("{{OUT_OF_SCOPE}}", "\n".join(f"- {a}" for a in out_of_scope))
            .replace("{{TECHNICAL}}", "\n".join(f"- {a}" for a in technical)))


def build_mutants(control):
    """Each mutant's contract and what a judge must report for it, from judge-control.yaml.

    Items are renumbered in their final order, so an id reveals nothing of how the contract was made.
    """
    base = {b["id"]: b for b in control["base"]}
    partials = {p["id"]: p["requirement"] for p in control["partials"]}
    additions = {a["id"]: a for a in control["additions"]}
    mutants = []
    for m in control["mutants"]:
        remove, partial, add = (m[k].split() for k in ("remove", "partial", "add"))
        unknown = [i for i in (remove + partial) if i not in base and i != "all"] + [i for i in add if i not in additions]
        if unknown:
            sys.exit(f"{JUDGE_CONTROL_FILE}: mutant {m['id']} names unknown entries {unknown}")
        kept = [] if remove == ["all"] else [b for b in control["base"] if b["id"] not in remove]
        entries = []
        for b in kept:
            text = partials[b["id"]] if b["id"] in partial else b["requirement"]
            entries.append({"requirement": text, "class": "reference", "covers": b["covers"]})
            entries += [{"requirement": additions[a]["requirement"], "class": additions[a]["class"], "covers": None}
                        for a in add if additions[a]["after"] == b["id"]]
        items = [{"id": f"DR-{n:02d}", **e} for n, e in enumerate(entries, 1)]
        coverage = {b["covers"]: "missing" for b in control["base"]}
        for b in kept:
            coverage[b["covers"]] = "partial" if b["id"] in partial else "covered"
        mutants.append({"id": m["id"], "name": m["name"], "items": items, "coverage": coverage})
    return mutants


def contract_text(items):
    if not items:
        return "The contract has no items."
    listed = "\n".join(f"- id: {i['id']}\n  requirement: {i['requirement']}" for i in items)
    return f"The contract has {len(items)} items:\n\n{listed}"


JUDGEMENT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["requirements", "items"],
    "properties": {
        "requirements": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["id", "coverage", "items"],
            "properties": {"id": {"type": "string"}, "coverage": {"type": "string", "enum": list(COVERAGE)},
                           "items": {"type": "array", "items": {"type": "string"}}}}},
        "items": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["id", "class", "requirements"],
            "properties": {"id": {"type": "string"}, "class": {"type": "string", "enum": list(CLASSES)},
                           "requirements": {"type": "array", "items": {"type": "string"}}}}},
    },
}


def parse_judgement(text, requirement_ids, item_ids):
    """The judge's reply, or None unless it lists every requirement and every item exactly once."""
    try:
        reply = json.loads(text)
    except ValueError:
        return None
    if not isinstance(reply, dict) or not isinstance(reply.get("requirements"), list) or not isinstance(reply.get("items"), list):
        return None
    requirements, items = {}, {}
    for r in reply["requirements"]:
        if (not isinstance(r, dict) or not isinstance(r.get("id"), str) or r.get("coverage") not in COVERAGE
                or not isinstance(r.get("items"), list)):
            return None
        requirements[r.get("id")] = {"coverage": r["coverage"], "items": [str(i) for i in r["items"]]}
    for i in reply["items"]:
        if (not isinstance(i, dict) or not isinstance(i.get("id"), str) or i.get("class") not in CLASSES
                or not isinstance(i.get("requirements"), list)):
            return None
        items[i.get("id")] = {"class": i["class"], "requirements": [str(r) for r in i["requirements"]]}
    if (len(requirements) != len(reply["requirements"]) or set(requirements) != set(requirement_ids)
            or len(items) != len(reply["items"]) or set(items) != set(item_ids)):
        return None
    return {"requirements": requirements, "items": items}


def score(judgement):
    """The contract's measures from one judgement (program plan §6.4, decision register D-45, D-47)."""
    coverage = [r["coverage"] for r in judgement["requirements"].values()]
    classes = [i["class"] for i in judgement["items"].values()]
    counted = len(classes) - classes.count("technical")
    return {"covered": coverage.count("covered"), "partial": coverage.count("partial"), "of": len(coverage),
            "recall": coverage.count("covered") / len(coverage) if coverage else None,
            "precision": classes.count("reference") / counted if counted else None,
            "outOfScope": classes.count("user_visible"), "technical": classes.count("technical")}


def disagreements(mutant, judgement):
    """Every place where the judgement differs from what the mutant was built to be."""
    found = []
    for rid, expected in mutant["coverage"].items():
        got = judgement["requirements"][rid]["coverage"]
        if got != expected:
            found.append(f"{rid}: {got}, expected {expected}")
    for item in mutant["items"]:
        got = judgement["items"][item["id"]]
        if got["class"] != item["class"]:
            found.append(f"{item['id']}: {got['class']}, expected {item['class']}")
        elif item["class"] == "reference" and item["covers"] not in got["requirements"]:
            found.append(f"{item['id']}: does not name {item['covers']}")
    return found


def judge_one(judge, system, session, requirement_ids, items):
    """One judgement of one contract. A reply of the wrong shape fails the run; it is never asked for
    again, since a second draw on the same contract could replace a judgement the calibration counts."""
    reply = judge.call(session, system, [("user", contract_text(items))], json_reply=True, schema=JUDGEMENT_SCHEMA)
    judgement = parse_judgement(reply, requirement_ids, [i["id"] for i in items])
    if judgement is None:
        raise RunFailed(f"{session}: the judgement does not list every requirement and every item exactly once")
    return judgement


def judge_control(args, files, out, run, judge):
    """Judge every mutant several times; the judge passes only when every judgement is exactly right (D-48)."""
    mutants = build_mutants(parse_control(files[JUDGE_CONTROL_FILE], JUDGE_CONTROL_FILE))
    system = judge_system(files[JUDGE_FILE], files)
    requirement_ids = [i for i, _ in parse_reference(files[REFERENCE_FILE])[1]]
    results = []
    for repetition in range(1, args.repetitions + 1):
        for m in mutants:
            judgement = judge_one(judge, system, f"{m['id']}/{repetition}", requirement_ids, m["items"])
            found = disagreements(m, judgement)
            results.append({"mutant": m["id"], "name": m["name"], "repetition": repetition, "exact": not found,
                            "disagreements": found, "score": score(judgement), "judgement": judgement})
    summary = {"exact": sum(r["exact"] for r in results), "of": len(results),
               "passes": bool(results) and all(r["exact"] for r in results)}
    (out / "judge-control.json").write_text(json.dumps(
        {"summary": summary, "mutants": [{k: m[k] for k in ("id", "name", "items", "coverage")} for m in mutants],
         "judgements": results}, ensure_ascii=False, indent=1) + "\n")


def ceiling_items(units):
    """Every unit of the brief as one contract item, numbered in the brief's order (D-60)."""
    return [{"id": f"DR-{n:02d}", "requirement": line[2:] if line.startswith("- ") else line, "unit": uid}
            for n, (uid, (_, line)) in enumerate(units.items(), 1)]


def ceiling_run(args, files, out, run, judge):
    """Judge the whole brief, every unit an item, as a contract: a reference requirement the brief does
    not cover is one no subject can derive from what the personas know (D-45, D-60)."""
    items = ceiling_items(parse_brief(files["world-brief.md"]))
    system = judge_system(files[JUDGE_FILE], files)
    requirement_ids = [i for i, _ in parse_reference(files[REFERENCE_FILE])[1]]
    judgements = [judge_one(judge, system, f"ceiling/{repetition}", requirement_ids, items)
                  for repetition in range(1, args.repetitions + 1)]
    requirements = {r: [j["requirements"][r]["coverage"] for j in judgements] for r in requirement_ids}
    summary = {"repetitions": [{c: [j["requirements"][r]["coverage"] for r in requirement_ids].count(c)
                                for c in COVERAGE} for j in judgements],
               "of": len(requirement_ids),
               "sameInEveryRepetition": sum(len(set(c)) == 1 for c in requirements.values())}
    (out / "ceiling.json").write_text(json.dumps(
        {"summary": summary, "requirements": requirements, "items": items,
         "judgements": [{"repetition": n, "judgement": j} for n, j in enumerate(judgements, 1)]},
        ensure_ascii=False, indent=1) + "\n")


# --- the subjects ---------------------------------------------------------------------------------

def business(brief):
    """Brief §1, the only part of the brief a subject receives (D-47), without its heading."""
    match = re.search(r"^## 1\.[^\n]*\n(.*?)(?=^## )", brief, re.S | re.M)
    if not match:
        sys.exit("world-brief.md: no section 1")
    return match.group(1).strip()


def question(message):
    """(role, question) when the message is exactly one ASK line; else None, and the message is not a question."""
    match = ASK_LINE.fullmatch(message.strip())
    return (match.group(1).lower(), match.group(2).strip()) if match and "\n" not in message.strip() else None


def read_contract(message):
    """The items of a requirements message: its yaml block if it has one, else the whole message.

    Only entries with both an id and a requirement are items; nothing is repaired (D-57).
    """
    block = re.search(r"```ya?ml[ \t]*\n(.*?)```", message, re.S)
    lines = (block.group(1) if block else message).splitlines()
    items, current, field = [], None, None
    for line in lines:
        stripped, indent = line.strip(), len(line) - len(line.lstrip())
        entry = re.fullmatch(r"-\s+id:\s*(.*)", stripped)
        if entry:
            current, field = {"id": entry.group(1).strip().strip("\"'"), "requirement": ""}, None
            items.append(current)
            continue
        if current is None:
            continue
        key = re.fullmatch(r"([A-Za-z_]+):\s*(.*)", stripped)
        if key and indent <= 4:
            field = key.group(1) if key.group(1) == "requirement" else None
            value = key.group(2).strip()
            if field and value not in (">", "|", ">-", "|-"):
                current["requirement"] = value.strip("\"'")
        elif field and stripped:
            current["requirement"] = (current["requirement"] + " " + stripped).strip()
    return [i for i in items if i["id"] and i["requirement"]]


def subject_client(args, recorder):
    # A subject runs on its provider's defaults: no temperature, seed or effort is sent (Rules).
    return Client("subject", args.subject_provider, args.subject_model, args.subject_rpm,
                  args.subject_max_tokens, recorder)


def persona_client(args, recorder):
    return Client("persona", args.persona_provider, args.persona_model, args.persona_rpm,
                  args.persona_max_tokens, recorder, args.persona_temperature, args.persona_seed)


def persona_system(files, notes, role):
    return files["persona-prompt.md"].replace("{{ROLE}}", ROLES[role]).replace("{{NOTES}}", notes[role])


def describe(run, *clients):
    run["instruments"] = {c.role: {"provider": c.provider, "model": c.model, "description": c.describe()}
                          for c in clients}


def subject_naive(args, files, notes, out, run):
    recorder = Recorder(out)
    subject, persona = subject_client(args, recorder), persona_client(args, recorder)
    describe(run, subject, persona)
    system = (files["subject-naive-prompt.md"].replace("{{BUSINESS}}", business(files["world-brief.md"]))
              .replace("{{ROLES}}", ROLE_NAMES).replace("{{ROLE_KEYS}}", "`technician`, `dispatcher` or `desk`")
              .replace("{{MAX_QUESTIONS}}", str(MAX_QUESTIONS_NAIVE)))
    turns, conversations, exchanges, asked = [("user", NAIVE_START)], {r: [] for r in ROLES}, [], 0
    while True:
        message = subject.call(f"subject/{len(turns)}", system, turns)
        turns.append(subject.turn(message))
        ask = question(message)
        # After the limit the subject has been told it can ask no more; a question then is its last
        # message, read as its requirements like any other, so the run always ends.
        if ask is None or asked >= MAX_QUESTIONS_NAIVE:
            break
        asked += 1
        role, text = ask
        if role in ROLES:
            conversations[role].append(("user", text))
            answer = persona.call(f"persona/{role}/{len(conversations[role]) // 2 + 1}",
                                  persona_system(files, notes, role), conversations[role])
            conversations[role].append(("model", answer))
        else:
            answer = NAIVE_NO_ROLE
        exchanges.append({"role": role, "question": text, "answer": answer})
        # Once the last question is answered, the subject is told it can ask no more.
        turns.append(("user", answer if asked < MAX_QUESTIONS_NAIVE else f"{answer}\n\n{NAIVE_NO_MORE}"))
    items = read_contract(message)
    result = {"variant": "S-naive", "exchanges": exchanges, "requirements": message, "items": items,
              "unreadable": not items,
              "metrics": {"elicitation_initiated": asked > 0, "turns_before_first_artifact": asked,
                          "questions": {r: sum(e["role"] == r for e in exchanges) for r in ROLES},
                          "limitReached": asked >= MAX_QUESTIONS_NAIVE}}
    (out / "subject.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")


def interview(subject, persona, system, persona_prompt, role):
    turns, answering, transcript = [("user", INTERVIEW_START)], [], []
    while len(transcript) < MAX_QUESTIONS_INTERVIEW:
        message = subject.call(f"interviewer/{role}/{len(transcript) + 1}", system, turns)
        if any(line.strip() == END_MARKER for line in message.splitlines()):
            return transcript, "ended_by_interviewer", message
        turns.append(subject.turn(message))
        answering.append(("user", message))
        answer = persona.call(f"persona/{role}/{len(transcript) + 1}", persona_prompt, answering)
        answering.append(("model", answer))
        turns.append(("user", answer))
        transcript.append({"question": message, "answer": answer})
    return transcript, "max_questions", None


def subject_instructed(args, files, notes, out, run):
    recorder = Recorder(out)
    subject, persona = subject_client(args, recorder), persona_client(args, recorder)
    describe(run, subject, persona)
    interviewer, analyst = SUBJECT_MODES["subject-instructed"]
    interviews, texts = {}, []
    for role in ROLES:
        system = (files[interviewer].replace("{{BUSINESS}}", business(files["world-brief.md"]))
                  .replace("{{ROLES}}", ROLE_NAMES).replace("{{ROLE}}", INTERVIEWEES[role])
                  .replace("{{MAX_QUESTIONS}}", str(MAX_QUESTIONS_INTERVIEW)))
        transcript, ending, last = interview(subject, persona, system, persona_system(files, notes, role), role)
        interviews[role] = {"transcript": transcript, "ending": ending, "endingMessage": last}
        texts.append(f"# Interview — {INTERVIEWEES[role]}\n\n" + "\n\n".join(
            f"Interviewer: {e['question']}\n\nInterviewee: {e['answer']}" for e in transcript))
    # The analyst is a new session of the same subject and sees the transcripts and nothing else (D-45).
    message = subject.call("analyst", files[analyst].replace("{{TRANSCRIPTS}}", "\n\n---\n\n".join(texts)),
                           [("user", ANALYST_START)])
    items = read_contract(message)
    result = {"variant": "S-instructed", "interviews": interviews, "requirements": message, "items": items,
              "unreadable": not items,
              "metrics": {"questions_per_interview": {r: len(i["transcript"]) for r, i in interviews.items()},
                          "limitReached": {r: i["ending"] == "max_questions" for r, i in interviews.items()}}}
    (out / "subject.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")


def judge_run(args, files, out, run, judge):
    """Judge one subject run's contract, its items numbered in their order as in the calibration."""
    subject = json.loads(files["judged-subject.json"])
    judged = json.loads(files["judged-run.json"])
    items = [{"id": f"DR-{n:02d}", "requirement": i["requirement"], "read": i["id"]}
             for n, i in enumerate(subject["items"], 1)]
    requirement_ids = [i for i, _ in parse_reference(files[REFERENCE_FILE])[1]]
    judgement = judge_one(judge, judge_system(files[JUDGE_FILE], files), "judge", requirement_ids, items)
    vendor = judged["instruments"]["subject"]["provider"]
    # The judge of the other vendor scores; the judge of the subject's own family only measures the
    # judge effect, and its judgement is never scored (D-55).
    result = {"judged": {"run": str(args.judged), "mode": judged["mode"], "subject": judged["instruments"]["subject"]},
              "scored": judge.provider != vendor, "items": items, "score": score(judgement), "judgement": judgement}
    (out / "judgement.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")


# --- follow-ups -----------------------------------------------------------------------------------

FOLLOW_UP_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["questions"],
    "properties": {"questions": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["id", "follow_up"],
        "properties": {"id": {"type": "string"}, "follow_up": {"type": "boolean"}}}}},
}


def pairs_text(pairs):
    return "\n\n".join(f"{p['id']}\nThe answer just before it: {p['previous']}\nThe question: {p['question']}"
                       for p in pairs)


def parse_follow_ups(text, ids):
    """{id: follow_up} for exactly the given ids, or None."""
    try:
        reply = json.loads(text)
    except ValueError:
        return None
    entries = reply.get("questions") if isinstance(reply, dict) else None
    if not isinstance(entries, list):
        return None
    labels = {}
    for e in entries:
        if not isinstance(e, dict) or not isinstance(e.get("id"), str) or not isinstance(e.get("follow_up"), bool):
            return None
        labels[e["id"]] = e["follow_up"]
    return labels if len(labels) == len(entries) and set(labels) == set(ids) else None


def classify(judge, system, session, pairs):
    """The labels of one conversation's pairs; a reply of the wrong shape fails the run, never asked again."""
    reply = judge.call(session, system, [("user", pairs_text(pairs))], json_reply=True, schema=FOLLOW_UP_SCHEMA)
    labels = parse_follow_ups(reply, [p["id"] for p in pairs])
    if labels is None:
        raise RunFailed(f"{session}: the reply does not label every question exactly once")
    return labels


def follow_up_control(args, files, out, run, judge):
    conversations = parse_control(files[FOLLOW_UP_CONTROL_FILE], FOLLOW_UP_CONTROL_FILE)
    results, agreeing = [], {}
    for repetition in range(1, args.repetitions + 1):
        for cid, pairs in conversations.items():
            labels = classify(judge, files[FOLLOW_UP_FILE], f"{cid}/{repetition}", pairs)
            for p in pairs:
                agrees = labels[p["id"]] == (p["follow_up"] == "true")
                agreeing[repetition] = agreeing.get(repetition, 0) + agrees
                results.append({"conversation": cid, "id": p["id"], "repetition": repetition,
                                "expected": p["follow_up"] == "true", "got": labels[p["id"]], "agrees": agrees})
    of = sum(len(p) for p in conversations.values())
    summary = {"agreeing": agreeing, "of": of, "passAt": FOLLOW_UP_PASS_AT,
               "passes": bool(agreeing) and all(a >= FOLLOW_UP_PASS_AT for a in agreeing.values())}
    (out / "follow-up-control.json").write_text(json.dumps({"summary": summary, "pairs": results},
                                                           ensure_ascii=False, indent=1) + "\n")


def subject_pairs(subject):
    """Per role, every question after the first with the answer the same role gave just before it."""
    if subject["variant"] == "S-instructed":
        sequences = {r: i["transcript"] for r, i in subject["interviews"].items()}
    else:
        sequences = {r: [e for e in subject["exchanges"] if e["role"] == r] for r in ROLES}
    return {r: [{"id": f"Q{k + 1}", "previous": seq[k - 1]["answer"], "question": seq[k]["question"]}
                for k in range(1, len(seq))] for r, seq in sequences.items() if len(seq) > 1}


def follow_up_run(args, files, out, run, judge):
    subject = json.loads(files["judged-subject.json"])
    judged = json.loads(files["judged-run.json"])
    roles = {}
    for role, pairs in subject_pairs(subject).items():
        labels = classify(judge, files[FOLLOW_UP_FILE], f"follow-up/{role}", pairs)
        roles[role] = {"pairs": [{**p, "follow_up": labels[p["id"]]} for p in pairs],
                       "followUps": sum(labels.values()), "of": len(pairs)}
    follow_ups, of = sum(r["followUps"] for r in roles.values()), sum(r["of"] for r in roles.values())
    # As for the contract, the judge of the other vendor scores; the subject's own family is unscored.
    result = {"judged": {"run": str(args.judged), "mode": judged["mode"], "subject": judged["instruments"]["subject"]},
              "scored": judge.provider != judged["instruments"]["subject"]["provider"], "roles": roles,
              "follow_up_ratio": follow_ups / of if of else None, "followUps": follow_ups, "of": of}
    (out / "follow-ups.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=sorted(QUESTION_SETS) + list(GRADE_MODES) + list(JUDGE_MODES) + list(SUBJECT_MODES))
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
    parser.add_argument("--judge-provider", default="gemini")
    parser.add_argument("--judge-model", help="exact model identifier; required by the judge modes")
    parser.add_argument("--judge-rpm", type=float, default=5)
    parser.add_argument("--judge-max-tokens", type=int, default=32768)
    parser.add_argument("--judge-temperature", type=float, help="sent when given; else the provider default")
    parser.add_argument("--judge-seed", type=int, help="sent when given; else none")
    parser.add_argument("--judge-effort", help="anthropic only: the effort level, sent when given")
    parser.add_argument("--subject-provider", default="anthropic")
    parser.add_argument("--subject-model", help="exact model identifier; required by the subject modes")
    parser.add_argument("--subject-rpm", type=float, default=10)
    parser.add_argument("--subject-max-tokens", type=int, default=32000)
    parser.add_argument("--judged", type=pathlib.Path, help="the completed subject run that mode judge judges")
    parser.add_argument("--graded", type=pathlib.Path, help="the completed persona run that mode grade grades")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--out", type=pathlib.Path, help="output directory (must not exist)")
    parser.add_argument("--dry-run", action="store_true", help="check inputs and print hashes; call nothing")
    args = parser.parse_args()
    grading, judging, subjecting = args.mode in GRADE_MODES, args.mode in JUDGE_MODES, args.mode in SUBJECT_MODES

    names = ["world-brief.md", "brief-slices.yaml"]
    if subjecting:
        prompts = SUBJECT_MODES[args.mode]
        names += ["persona-prompt.md"] + ([prompts] if isinstance(prompts, str) else list(prompts))
    elif args.mode.startswith("follow-up"):
        names += [FOLLOW_UP_FILE] + ([FOLLOW_UP_CONTROL_FILE] if args.mode == "follow-up-control" else [])
    elif judging:
        names += [JUDGE_FILE] + ([JUDGE_CONTROL_FILE] if args.mode == "judge-control" else [])
    elif grading:
        names += [GRADER_FILE] + ([GRADER_CONTROL_FILE] if args.mode == "grader-control" else [])
    else:
        names += ["persona-prompt.md", QUESTION_SETS[args.mode]] + ([CHECK_FILE] if args.persona_check else [])
    files = {name: (HERE / name).read_text() for name in names}
    if args.mode in ("judge-control", "judge", "ceiling"):
        files.update({name: (HERE.parent / name).read_text() for name in (REFERENCE_FILE, ANTI_FILE)})
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
    if args.mode in ("judge", "follow-up"):
        if not args.judged:
            sys.exit(f"--judged is required by mode {args.mode}")
        judged_dir = args.judged.resolve()
        try:
            files["judged-run.json"] = (judged_dir / "run.json").read_text()
            files["judged-subject.json"] = (judged_dir / "subject.json").read_text()
            judged = json.loads(files["judged-run.json"])
        except (OSError, ValueError) as e:
            sys.exit(f"--judged {args.judged}: not a subject run record: {e}")
        if judged.get("status") != "completed" or judged.get("mode") not in SUBJECT_MODES:
            sys.exit(f"--judged {args.judged}: only a completed subject run is judged")
    hashes = {name: sha256(text) for name, text in files.items()}

    judge_settings = (args.judge_provider, args.judge_model, args.judge_rpm, args.judge_max_tokens,
                      args.judge_temperature, args.judge_seed, args.judge_effort)
    persona_settings = (args.persona_provider, args.persona_model, args.persona_rpm, args.persona_max_tokens,
                        args.persona_temperature, args.persona_seed, None)
    if subjecting:
        roles = [("subject", (args.subject_provider, args.subject_model, args.subject_rpm, args.subject_max_tokens,
                              None, None, None)), ("persona", persona_settings)]
        plan = {"limits": {"questions": MAX_QUESTIONS_NAIVE} if args.mode == "subject-naive"
                else {"questionsPerInterview": MAX_QUESTIONS_INTERVIEW}}
    elif args.mode == "judge":
        roles = [("judge", judge_settings)]
        plan = {"items": len(json.loads(files["judged-subject.json"])["items"]), "calls": 1}
    elif args.mode == "ceiling":
        roles = [("judge", judge_settings)]
        plan = {"items": len(units), "calls": args.repetitions}
    elif args.mode == "follow-up":
        roles = [("judge", judge_settings)]
        pairs = subject_pairs(json.loads(files["judged-subject.json"]))
        plan = {"pairs": {r: len(p) for r, p in pairs.items()}, "calls": len(pairs)}
    elif args.mode == "follow-up-control":
        roles = [("judge", judge_settings)]
        conversations = parse_control(files[FOLLOW_UP_CONTROL_FILE], FOLLOW_UP_CONTROL_FILE)
        plan = {"pairs": sum(len(p) for p in conversations.values()), "calls": len(conversations) * args.repetitions}
    elif judging:
        roles = [("judge", judge_settings)]
        mutants = build_mutants(parse_control(files[JUDGE_CONTROL_FILE], JUDGE_CONTROL_FILE))
        plan = {"mutants": {m["id"]: {"items": len(m["items"]),
                                      **{c: list(m["coverage"].values()).count(c) for c in COVERAGE}} for m in mutants},
                "calls": len(mutants) * args.repetitions}
    elif grading:
        roles = [("grader", (args.grader_provider, args.grader_model, args.grader_rpm,
                             args.grader_max_tokens, args.grader_temperature, args.grader_seed, None))]
        if args.mode == "grader-control":
            cases = parse_control(files[GRADER_CONTROL_FILE], GRADER_CONTROL_FILE)
            calls = sum(len(c) for c in cases.values())
        else:
            calls = sum(len(rep["answers"]) for reps in json.loads(files["graded-answers.json"]).values() for rep in reps)
        plan = {"calls": calls}
    else:
        roles = [("persona", persona_settings)]
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
    for role, settings in roles:
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
        if subjecting:
            (subject_naive if args.mode == "subject-naive" else subject_instructed)(args, files, notes, out, run)
        elif judging:
            recorder = Recorder(out)
            judge = Client("judge", args.judge_provider, args.judge_model, args.judge_rpm, args.judge_max_tokens,
                           recorder, args.judge_temperature, args.judge_seed, args.judge_effort)
            run["instruments"] = {"judge": {"provider": judge.provider, "model": judge.model,
                                            "description": judge.describe()}}
            {"judge-control": judge_control, "judge": judge_run, "ceiling": ceiling_run,
             "follow-up-control": follow_up_control, "follow-up": follow_up_run}[args.mode](args, files, out, run, judge)
        elif grading:
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
