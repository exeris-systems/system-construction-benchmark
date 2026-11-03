You check an answer that {{ROLE}} gave when an analyst interviewed them. Their notes are everything they know.

=== THEIR NOTES (read-only) ===
{{NOTES}}
=== END OF NOTES ===

You receive the analyst's question and the answer, split into numbered sentences. Decide for each sentence whether it stays (KEEP) or goes (DROP), and give the source of every sentence you keep. You never change a sentence; you only keep it or drop it.

KEEP a sentence only when every part of it has a source:

- words copied exactly from the notes, at least four words long, that say what the sentence says;
- DONT_KNOW, when the sentence only says the speaker does not know;
- FEELING, when the sentence only says how the speaker feels about, or what worries them in, a situation the notes describe.

DROP a sentence when any part of it has no source. In particular, DROP it when any part of it:

- states a number, name, type, brand, frequency, time, rule, duty, event, cause, or consequence that the notes do not give;
- says who does something, or who would know something, when the notes do not say so;
- speaks for an organisation other than the speaker's own, or speaks as if the speaker worked for another one;
- says how a system or service works or should work: what it should show, tell, do, check, record, or prevent, how or where it keeps information, or which screens, buttons, or features it has.

A sentence that is partly in the notes and partly not is DROPPED. When you are not sure, DROP.

Reply with JSON only, one entry per sentence, in order:
{"sentences": [{"verdict": "KEEP", "source": "words copied from the notes"}, {"verdict": "KEEP", "source": "DONT_KNOW"}, {"verdict": "DROP", "source": null}]}
