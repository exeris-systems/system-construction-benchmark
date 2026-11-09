You are working for a client on a new software service. Nobody has designed it yet.

The client writes:

> Our customer companies need a new service for running their drone fleets from day to day, on our platform. Write the requirements for it: what the service must do, so that a team can build it and anyone can check whether it does.

What you know about the client's business:

{{BUSINESS}}

The people who will use the service work in three roles: {{ROLES}}. You can reach one person in each role. A message that is exactly one line, `ASK <role>: <question>`, with `<role>` one of {{ROLE_KEYS}}, goes to that person, and their answer comes back to you. Each of them remembers what you asked them before. You can send at most {{MAX_QUESTIONS}} such questions in all. Any other message is taken as your requirements, and ends the work.

Write the requirements as a list in YAML, in exactly this format, with nothing else in that message:

```yaml
- id: DR-01
  requirement: >
    one thing the service must do, or must not do, and in which case
- id: DR-02
  requirement: >
    ...
```

Number the items DR-01, DR-02, and so on. Each item states one requirement in plain words.
