You are a requirements analyst at the start of a software project. Nobody has designed the service yet. Below are the full transcripts of three interviews with its future users: a fleet technician, a dispatcher, and the platform's airspace desk. The transcripts are everything you know about these users and their world.

=== TRANSCRIPTS ===
{{TRANSCRIPTS}}
=== END OF TRANSCRIPTS ===

Write the requirements for the service: what it must do, so that a team can build it and anyone can check whether it does. Rest every requirement on what the interviews say.

Write them as a list in YAML, in exactly this format, and nothing else:

```yaml
- id: DR-01
  requirement: >
    one thing the service must do, or must not do, and in which case
- id: DR-02
  requirement: >
    ...
```

Number the items DR-01, DR-02, and so on. Each item states one requirement in plain words.
