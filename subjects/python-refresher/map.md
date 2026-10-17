# Python Basics Refresher Map

- [todo] syntax-and-control-flow | sticking points: truthiness; operator precedence; loop boundaries
- [todo] core-data-model | depends on: syntax-and-control-flow | sticking points: aliasing; mutation versus rebinding; is versus ==
- [todo] collections | depends on: core-data-model | sticking points: empty sets; missing keys; mutation methods returning None
- [todo] strings-and-comprehensions | depends on: collections | sticking points: negative indices; exclusive slice stops; unnecessary comprehensions
- [todo] functions | depends on: strings-and-comprehensions | sticking points: mutable defaults; argument binding; implicit None
- [todo] scope-and-closures | depends on: functions | sticking points: local assignment; late binding; lambda limitations
- [todo] iterators-generators-and-decorators | depends on: scope-and-closures | sticking points: iterator exhaustion; lazy execution; wrappers dropping return values
- [todo] classes-and-dataclasses | depends on: iterators-generators-and-decorators | sticking points: class versus instance attributes; shared mutable fields
- [todo] exceptions-and-context-managers | depends on: classes-and-dataclasses | sticking points: broad catches; cleanup; exception suppression
- [todo] modules-and-packages | depends on: exceptions-and-context-managers | sticking points: import-time execution; module versus package; circular imports
- [todo] type-hints | depends on: modules-and-packages | sticking points: optional versus defaulted parameters; annotations not enforcing runtime types
- [todo] idioms-and-pitfalls | depends on: type-hints | sticking points: mutation while iterating; in-place return values; unnecessarily manual loops

## Topic Scope

### Requirements: syntax-and-control-flow
Scope: accepted
- scf-basics: Write and predict assignments, arithmetic, comparisons, Boolean expressions, and truthiness checks.
- scf-control: Write `if`/`elif`/`else`, `for`, and `while` code using `range`, `break`, and `continue`.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: core-data-model
Scope: accepted
- cdm-basic-types: Distinguish `None`, Boolean, integer, float, and string values; predict basic conversions and truthiness.
- cdm-basic-mutation: Classify built-in types by mutability and predict mutation, rebinding, and aliasing in short snippets.
- cdm-basic-comparison: Explain identity versus equality, use `is None`, and predict comparisons without relying on interning.
Passing target: Complete all three requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: collections
Scope: accepted
- col-builtins: Choose, create, access, iterate, and update lists, tuples, sets, and dictionaries; explain ordering, uniqueness, and basic key hashability.
- col-operations: Use membership, unpacking, dictionary `get`/`items`, set operations, and shallow copies; predict effects on nested mutable values.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: strings-and-comprehensions
Scope: accepted
- str-operations: Use indexing, slicing, f-strings, `split`, `join`, `strip`, and `replace`; predict results and explain string immutability.
- str-comprehensions: Write list, set, and dictionary comprehensions with filtering; translate between comprehensions and equivalent loops.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: functions
Scope: accepted
- fun-calls: Define functions with return values, positional and keyword arguments, defaults, `*args`, and `**kwargs`; use call unpacking and identify invalid calls.
- fun-defaults: Predict repeated calls involving mutable defaults and correct unintended shared state using a `None` default.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: scope-and-closures
Scope: accepted
- scope-binding: Predict local, enclosing, global, and built-in name lookup; use `global` and `nonlocal` in small examples.
- scope-functions: Write a closure and a lambda-based sorting key; predict and fix late-bound loop-variable capture.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: iterators-generators-and-decorators
Scope: accepted
- igd-iteration: Distinguish iterable from iterator; use `iter` and `next`; write a generator function and generator expression, predicting execution and exhaustion.
- igd-decoration: Write and apply a simple function decorator that forwards arguments and return values and preserves metadata with `functools.wraps`.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: classes-and-dataclasses
Scope: accepted
- cls-basics: Write a class with instance attributes and methods, then a single-inheritance subclass using overriding and `super()`.
- cls-dataclasses: Write a dataclass, use `field(default_factory=...)`, and explain its generated initializer, representation, and equality compared with a plain class.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: exceptions-and-context-managers
Scope: accepted
- ex-handling: Write correct `try`/`except`/`else`/`finally` with narrow exception types; explain bare-except pitfalls.
- ecm-resources: Raise and re-raise exceptions; use `with` for files and write a simple `contextlib.contextmanager` with cleanup on success and failure.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: modules-and-packages
Scope: accepted
- mod-structure: Organize a small program into modules and a regular package with `__init__.py`; use absolute and package-relative imports appropriately.
- mod-execution: Explain import-time execution and the `if __name__ == "__main__"` guard; distinguish running a file from `python -m package.module` and identify a simple circular import.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: type-hints
Scope: accepted
- typing-basics: Annotate parameters, return values, collections, and nullable values using built-in generics and `X | None`.
- typing-purpose: Explain static checking versus runtime behavior and identify straightforward annotation mismatches in short snippets.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.

### Requirements: idioms-and-pitfalls
Scope: accepted
- idiom-review: Identify and fix mutable defaults, aliasing mistakes, incorrect identity comparisons, collection mutation during iteration, and misuse of in-place method return values.
- idiom-rewrite: Rewrite short loops using `enumerate`, `zip`, direct iteration, or comprehensions where appropriate; choose a narrow exception handler or explicit check for a stated scenario.
Passing target: Complete both requirements unaided, without docs or REPL, with correct code, predictions, and explanations as requested. No advanced features beyond the checklist are required.
