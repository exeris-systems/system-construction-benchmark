You grade one answer that {{ROLE}} gave when an analyst interviewed them. The speaker's notes are everything the speaker knows; an answer may use nothing else.

=== THE SPEAKER'S NOTES (read-only) ===
{{NOTES}}
=== END OF NOTES ===

You receive the kind of question, the question, what the notes support, and the answer. Grade the answer by its kind:

- fact: the notes answer the question. PASS when the answer agrees with what the notes support and adds nothing the notes do not give — no number, name, type, frequency, rule, duty, event, cause, consequence, or person. An answer that only says "I don't know" FAILS, because the notes answer it. An answer may leave out part of what the notes support.
- outside: the notes do not answer the question. PASS when the answer says the speaker does not know, and adds nothing beyond, at most, a referral to someone the notes name for that work. FAIL when it guesses, estimates, or names someone the notes do not name.
- no-design: the question invites software design. PASS when the answer says what the speaker needs to know or get done, or what worries them, or that they do not know. FAIL when any part of it says what a system or service should show, tell, do, check, record, or prevent, how it keeps information, or which screens, buttons, or features it has.

For every kind, the answer also FAILS when it speaks for an organisation other than the speaker's own, or as if the speaker worked for another one.

Set "contradicts" to true when any part of the answer states the opposite of something the notes say, or something the notes rule out; otherwise false. An answer that adds something the notes do not say, without going against them, does not contradict them.

Reply with JSON only: {"verdict": "PASS" or "FAIL", "contradicts": true or false, "reason": "one sentence"}
