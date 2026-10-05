# TypeScript Scope Proposal

Status: pending learner approval. This is a repository-maintenance proposal, not an accepted subject map.

## Intended amendment

Keep all existing TypeScript topic names, dependencies, order, sticking points and `todo` statuses. Add the scope
sections below to `subjects/typescript/map.md` only after explicit approval. Historical sessions, mistakes, cards
and sources remain unchanged. No additional concepts may become required without another approved amendment.

This proposal follows the task-tracking API goal. It is not a claim to cover every TypeScript language feature.
Exhaustive `never` checks, custom type predicates, generics, classes and advanced type manipulation are optional
extras outside this proposal. No implementations or answers are supplied here.

## Proposed scope sections

### Requirements: object-and-function-types
- object-shape: Define a task object type with required fields and an optional description; explain allowed omissions.
- object-parameters: Type function parameters for a task operation and identify invalid argument shapes.
- object-return: Type and explain every return path of a function returning a string or undefined, including fall-through behavior.
Passing target: Write and explain a task type and function unaided, satisfying all three criteria with consistent branches.

### Requirements: unions-and-narrowing
- union-unknown: Explain unknown versus any for unchecked method calls and predict both compile-time and runtime behavior.
- union-missing: Distinguish undefined, empty string and false in truthiness checks, explicit missing-value checks and optional chaining.
- union-runtime: Write a safe title reader for unknown input using primitive, object, null, property-existence and string-value checks.
- union-discriminant: Branch on a discriminated union and access only properties available in the selected branch.
Passing target: Complete all four criteria unaided through predictions, explanations, a safe title reader and a discriminated-union branch.

### Requirements: async-functions
- async-return: Type an async task lookup as a Promise of its actual possible results, including undefined for a missing task.
- async-await: Call the lookup with await, distinguish its Promise from its resolved result and handle the missing result before use.
- async-reject: Explain and demonstrate how a caller handles a rejected lookup separately from a resolved missing result.
Passing target: Write and explain lookup and caller code unaided covering success, absence and rejection.

### Requirements: request-validation
- validation-unknown: Treat parsed request data as unknown and explain why TypeScript annotations do not validate JSON.
- validation-fields: Validate required and optional task fields, rejecting null and wrong types before use.
- validation-false: Preserve a valid false completion value and distinguish it from a missing or invalid field.
Passing target: Write and explain validation unaided for valid data, missing fields, null, wrong types and false values.

### Requirements: api-contracts
- contract-first: Define the task API in OpenAPI 3 YAML before handlers, including operation IDs, shared error schema and key examples; validate it.
- contract-generation: Identify and run pinned, deterministic generation commands for backend contracts/models and a TypeScript client.
- contract-use: Implement an operation against generated contracts without duplicating models; change YAML and regenerate when behavior changes.
Passing target: Produce and explain a validated contract and its generation/use workflow unaided for a task operation.

### Requirements: create-and-update-inputs
- input-create: Define create fields in the contract, excluding server-controlled IDs, and distinguish required from optional input.
- input-update: Model update input and apply the intended difference between omission and explicit values without overwriting omitted fields.
- input-utilities: Explain Partial and Pick on supplied types, their lack of runtime validation, and why they do not replace generated API models.
Passing target: Produce and explain create/update schemas and update application unaided, protecting IDs and preserving omitted fields.

### Requirements: crud-handlers
- crud-identity: Find tasks by stable ID, not array position, and distinguish missing records from existing ones.
- crud-lifecycle: Implement create, read, update and delete against generated contracts, preserving unmodified fields and intended state transitions.
- crud-responses: Return contract-defined response types/statuses for successful operations and missing tasks; keep async signatures consistent.
Passing target: Implement and explain the task CRUD lifecycle unaided, including stable identity, updates, deletion and missing records.

### Requirements: error-handling
- error-classify: Distinguish invalid requests, missing tasks and unexpected failures; map them to contract-defined error responses.
- error-boundary: Handle asynchronous failures at the handler boundary without swallowing them or returning a false success.
- error-safe: Return the shared error shape without internal details and log diagnostic information without request content or secrets.
Passing target: Implement and explain the three failure categories unaided, with consistent safe responses and diagnostic handling.

### Requirements: api-tests
- tests-lifecycle: Automate the full create/read/update/delete lifecycle with assertions on responses and stored state.
- tests-validation: Cover invalid bodies, omitted update fields, false values and missing IDs with meaningful contract-based assertions.
- tests-failure: Test an unexpected async failure, its safe response and absence of unintended state mutation; run tests with coverage.
Passing target: Write and run tests unaided demonstrating all three criteria and explain what each failure case protects.

## Provisional evidence mapping

These states are conditional on approval of the exact criteria above; they do not establish accepted readiness.
Applicable TypeScript sources are absent. Historical entries explicitly marked unverified stay unknown; do not
retroactively regrade them by general knowledge.

| Requirement | Provisional state | Evidence |
| --- | --- | --- |
| object-shape | unknown | `subjects/typescript/sessions.md:3` is a provisional interview summary, not verified criterion-specific production. |
| object-parameters | unknown | No recorded resolved production matching the criterion. |
| object-return | unknown | `subjects/typescript/sessions.md:5-7` describe unverified return attempts and a redo without a verified outcome; line 8 covers optional chaining, not all return paths. |
| union-unknown | resolved, unaided | `subjects/typescript/sessions.md:13` records the comparison and runtime prediction successfully redone unaided. |
| union-missing | unknown, partial evidence | `subjects/typescript/sessions.md:12,14` cover undefined and empty string; false-value production is not recorded. |
| union-runtime | resolved, aided | `subjects/typescript/sessions.md:10,14` record primitive and object title readers, including null/property/string checks. |
| union-discriminant | resolved, unaided | `subjects/typescript/sessions.md:14` records discriminated-union branching and property access. |
| All requirements in later topics | unknown | No recorded resolved production matching those requirements. |

The interrupted exams at `subjects/typescript/sessions.md:11,15` contain no production and do not erase previous
resolved evidence. No topic has a completed exam or a passed status.

## Prescribed next action after approval

Apply the shared gate to the unchanged map: `object-and-function-types` is the first unpassed topic and has
unknown coverage. Offer `object-shape`, the first unknown criterion, with a confirmed learning-role handoff.
An explicit request to work on `unions-and-narrowing` instead requires disclosure and confirmation of the unmet
object-and-function-types dependency. Within that topic, `union-missing` is the first unknown requirement.
Do not automatically restart either interrupted exam or add exhaustiveness as a blocker.
