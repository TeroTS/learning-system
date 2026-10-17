# Python Refresher Map

- [todo] core-data-model | sticking points: mutable default arguments; is vs ==; shallow vs deep copy; hash/eq contract
- [todo] collections-and-comprehensions | depends on: core-data-model | sticking points: dict ordering guarantees; set/dict comprehension scope; collections module choice
- [todo] iterators-and-generators | depends on: collections-and-comprehensions | sticking points: one-shot iterators exhausted; yield from vs return; lazy evaluation surprises
- [todo] functions-and-closures | depends on: core-data-model | sticking points: late binding in closures; nonlocal; positional-only / and keyword-only * parameters
- [todo] decorators-and-context-managers | depends on: functions-and-closures, iterators-and-generators | sticking points: functools.wraps; decorators with arguments; exception handling in __exit__ / contextmanager
- [todo] classes-and-dataclasses | depends on: core-data-model, functions-and-closures | sticking points: super() and MRO; class vs instance attributes; dataclass field(default_factory) / frozen / slots / kw_only
- [todo] exceptions | depends on: classes-and-dataclasses | sticking points: raise from vs implicit chaining; bare except; ExceptionGroup and except*
- [todo] type-hints | depends on: classes-and-dataclasses, functions-and-closures | sticking points: Protocol vs ABC; invariance of list[T]; PEP 695 generics vs TypeVar; TypedDict total/Required/NotRequired
- [todo] structural-pattern-matching | depends on: classes-and-dataclasses, collections-and-comprehensions | sticking points: capture vs value patterns; __match_args__; guard order
- [todo] async-programming | depends on: iterators-and-generators, decorators-and-context-managers, exceptions | sticking points: blocking calls in event loop; TaskGroup vs gather; cancellation and timeouts
- [todo] modern-python-features | depends on: type-hints, structural-pattern-matching, async-programming, exceptions | sticking points: which version introduced what; 3.14 deferred annotations
- [todo] idioms-and-pitfalls | depends on: modern-python-features | sticking points: EAFP vs LBYL; pathlib/f-strings/enumerate over legacy forms

## Topic Scope

### Requirements: core-data-model
Scope: accepted
- cdm-mutability: Classify built-in types by mutability and predict output of aliasing/mutation code, including mutable default arguments.
- cdm-identity-equality: Explain and predict `is` vs `==`, including `None` checks and small-int/str interning caveats.
- cdm-copying: Predict results of assignment, shallow copy and deep copy on nested structures.
- cdm-hash-eq: Explain the `__hash__`/`__eq__` contract and why mutable objects are unhashable.
Passing target: Complete all four requirements unaided (no docs or REPL), with correct predictions and explanations at the hardest level.

### Requirements: collections-and-comprehensions
Scope: accepted
- cc-choose: Choose among list, tuple, dict, set, deque, defaultdict, Counter and namedtuple for a stated need, justifying by complexity or semantics.
- cc-comprehensions: Write list, dict, set and nested comprehensions and generator expressions, and predict scope behaviour.
- cc-unpacking: Use starred unpacking, dict merge `|`/`|=` and `zip(strict=True)` correctly.
Passing target: Complete all three requirements unaided (no docs or REPL), with correct code and justification at the hardest level.

### Requirements: iterators-and-generators
Scope: accepted
- ig-protocol: Implement the iterator protocol; explain iterable vs iterator and exhaustion.
- ig-generators: Write generator functions, use `yield from` and generator return values, and predict lazy evaluation.
- ig-itertools: Solve tasks with `itertools` (including `batched`, `pairwise`, `chain`, `islice`) instead of manual loops.
Passing target: Complete all three requirements unaided (no docs or REPL), with working code and correct predictions at the hardest level.

### Requirements: functions-and-closures
Scope: accepted
- fc-parameters: Write signatures using positional-only `/`, keyword-only `*`, `*args` and `**kwargs`, and predict which calls are valid.
- fc-closures: Predict and fix closure late-binding behaviour; use `nonlocal` correctly.
- fc-first-class: Use functions as values, including `functools.partial`, lambda limits and `key=` functions.
Passing target: Complete all three requirements unaided (no docs or REPL), with correct code and predictions at the hardest level.

### Requirements: decorators-and-context-managers
Scope: accepted
- dcm-decorators: Write a decorator with and without arguments, preserving metadata with `functools.wraps`.
- dcm-stdlib-decorators: Use `functools.cache`/`lru_cache`, `cached_property`, `property`, `staticmethod` and `classmethod` correctly.
- dcm-context-managers: Write a context manager as a class and with `contextlib.contextmanager`, handling exceptions; use parenthesised multi-item `with` and `ExitStack`.
Passing target: Complete all three requirements unaided (no docs or REPL), with working, exception-correct code at the hardest level.

### Requirements: classes-and-dataclasses
Scope: accepted
- cd-classes: Write classes with inheritance, `super()` and MRO; explain class vs instance attributes.
- cd-dunder: Implement relevant dunder methods (`__repr__`, `__eq__`, ordering, `__len__`/`__iter__`).
- cd-dataclasses: Use `@dataclass` with `frozen`, `slots`, `kw_only`, `field(default_factory)` and `__post_init__`; choose dataclass vs NamedTuple vs plain class for a stated need.
- cd-enum: Use `Enum`/`StrEnum` and `auto()` appropriately.
Passing target: Complete all four requirements unaided (no docs or REPL), with correct code and justification at the hardest level.

### Requirements: exceptions
Scope: accepted
- ex-handling: Write correct `try`/`except`/`else`/`finally` with narrow exception types; explain bare-except pitfalls.
- ex-custom: Design a custom exception hierarchy for a service and use `raise ... from` chaining.
- ex-groups: Use `ExceptionGroup`, `except*` and `add_note()`, and predict their behaviour.
Passing target: Complete all three requirements unaided (no docs or REPL), with correct code and predictions at the hardest level.

### Requirements: type-hints
Scope: accepted
- th-basics: Annotate using `X | None`, built-in generics, `Callable`, `Literal`, `Final` and `Self`.
- th-generics: Write generic functions and classes with PEP 695 syntax and `type` aliases; explain variance (list vs Sequence).
- th-structural: Use `Protocol` and `TypedDict` (`Required`, `NotRequired`, `ReadOnly`); choose Protocol vs ABC.
- th-advanced: Use `@override`, `TypeGuard`/`TypeIs`, `ParamSpec` for decorators; explain deferred annotation evaluation.
Passing target: Complete all four requirements unaided (no docs or REPL), with type-checker-correct code and correct explanations at the hardest level.

### Requirements: structural-pattern-matching
Scope: accepted
- spm-patterns: Write `match` statements using literal, capture, sequence, mapping, class, OR and `as` patterns with guards.
- spm-semantics: Predict match results, including capture vs dotted value patterns and `__match_args__`.
Passing target: Complete both requirements unaided (no docs or REPL), with working code and correct predictions at the hardest level.

### Requirements: async-programming
Scope: accepted
- ap-basics: Explain coroutines, the event loop and `await`; predict execution order.
- ap-concurrency: Run concurrent work with `TaskGroup`, `asyncio.timeout` and `gather`; handle cancellation and errors.
- ap-pitfalls: Identify and fix blocking calls in async code (`asyncio.to_thread`); use `async with` and `async for`.
Passing target: Complete all three requirements unaided (no docs or REPL), with working code and correct predictions at the hardest level.

### Requirements: modern-python-features
Scope: accepted
- mpf-timeline: Name and correctly use key 3.10–3.14 features not covered above: improved error messages, `tomllib`, PEP 701 f-strings, `copy.replace`, free-threading/JIT awareness, template strings (t-strings), unparenthesised `except` lists.
- mpf-upgrade: Rewrite a given 3.7-style snippet into idiomatic 3.14 code.
Passing target: Complete both requirements unaided (no docs or REPL), with correct version attribution and working code at the hardest level.

### Requirements: idioms-and-pitfalls
Scope: accepted
- ip-review: Review a given backend code sample and identify every non-idiomatic, outdated or buggy construct with justification.
- ip-rewrite: Rewrite the sample idiomatically so a senior reviewer would raise no modern-Python findings.
Passing target: Complete both requirements unaided (no docs or REPL), identifying all issues and producing a correct rewrite at the hardest level.
