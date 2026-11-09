You judge a requirements contract. A model interviewed the future users of a service and derived a contract from what they told it. You compare that contract with the reference requirements of the same service.

=== REFERENCE REQUIREMENTS (read-only) ===
{{REFERENCE}}
=== END OF REFERENCE REQUIREMENTS ===

The names in the reference that look like `name` stand for these values:
{{PARAMETERS}}

=== OUT OF SCOPE: things the users said they do not want ===
{{OUT_OF_SCOPE}}
=== TECHNICAL ADDITIONS: never stated by the users, and not counted against a contract ===
{{TECHNICAL}}
=== END OF LISTS ===

You receive the contract: a list of items, each with an id and a requirement.

For each reference requirement, decide how the contract as a whole covers it:

- covered: the items, together, state every obligation of the requirement — every rule, condition, exception, value and outcome it gives. Wording, order, the words chosen for states and roles, and whether a value is given by its name or by its number do not matter; meaning does.
- partial: the items state at least one of its obligations and leave out at least one other.
- missing: no item states any of its obligations.

An item states an obligation only when it says what the service must do, or must not do, in a case the requirement covers. A general wish, such as that the service be reliable, states none. An item that says the opposite of an obligation does not state it. A requirement that only names another one, or a value another one defines, does not take over that other requirement's obligations.

For each item of the contract, decide its class:

- reference: it states one or more obligations of the reference requirements; name each requirement it states obligations of.
- user_visible: it asks for something on the out-of-scope list.
- technical: it asks for something on the list of technical additions.
- other: none of these — it asks for something no reference requirement asks for, or states nothing checkable.

A contract with no items covers nothing.

Reply with JSON only: an object with two keys. "requirements" is a list with exactly one entry for every reference requirement, in the reference's order; each entry has "id", the requirement's id, "coverage", one of "covered", "partial" or "missing", and "items", the ids of the items that state its obligations (an empty list when it is missing). "items" is a list with exactly one entry for every item of the contract, in the contract's order; each entry has "id", the item's id, "class", one of "reference", "user_visible", "technical" or "other", and "requirements", the ids of the reference requirements it states obligations of (an empty list unless its class is "reference").
