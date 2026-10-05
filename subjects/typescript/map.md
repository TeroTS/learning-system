# TypeScript Map

- [passed] object-and-function-types | sticking points: optional fields, parameter types, return types
- [passed] unions-and-narrowing | depends on: object-and-function-types | sticking points: unknown vs any, missing values, runtime type checks
- [todo] async-functions | depends on: unions-and-narrowing | sticking points: Promise return types, undefined results, rejected promises
- [todo] request-validation | depends on: unions-and-narrowing | sticking points: compile-time types do not validate JSON, false vs missing
- [todo] api-contracts | depends on: object-and-function-types | sticking points: OpenAPI-first design, generated types vs handwritten duplicates
- [todo] create-and-update-inputs | depends on: request-validation, api-contracts | sticking points: omitted vs explicit values, Partial and Pick, protecting IDs
- [todo] crud-handlers | depends on: async-functions, create-and-update-inputs | sticking points: ID vs array index, missing tasks, response types
- [todo] error-handling | depends on: crud-handlers | sticking points: validation vs not-found vs unexpected failures, consistent error responses
- [todo] api-tests | depends on: error-handling | sticking points: CRUD lifecycle, invalid requests, false values, missing IDs

## Topic Scope

### Requirements: object-and-function-types
Scope: accepted
- object-shape: Define a task object type with required fields and an optional description; explain allowed omissions.
- object-parameters: Type function parameters for a task operation and identify invalid argument shapes.
- object-return: Type and explain every return path of a function returning a string or undefined, including fall-through behavior.
Passing target: Write and explain a task type and function unaided, satisfying all three criteria with consistent branches.

### Requirements: unions-and-narrowing
Scope: accepted
- union-unknown: Explain unknown versus any for unchecked method calls and predict both compile-time and runtime behavior.
- union-missing: Distinguish undefined, empty string and false in truthiness checks, explicit missing-value checks and optional chaining.
- union-runtime: Write a safe title reader for unknown input using primitive, object, null, property-existence and string-value checks.
- union-discriminant: Branch on a discriminated union and access only properties available in the selected branch.
Passing target: Complete all four criteria unaided through predictions, explanations, a safe title reader and a discriminated-union branch.

### Requirements: async-functions
Scope: accepted
- async-return: Type an async task lookup as a Promise of its actual possible results, including undefined for a missing task.
- async-await: Call the lookup with await, distinguish its Promise from its resolved result and handle the missing result before use.
- async-reject: Explain and demonstrate how a caller handles a rejected lookup separately from a resolved missing result.
Passing target: Write and explain lookup and caller code unaided covering success, absence and rejection.

### Requirements: request-validation
Scope: accepted
- validation-unknown: Treat parsed request data as unknown and explain why TypeScript annotations do not validate JSON.
- validation-fields: Validate required and optional task fields, rejecting null and wrong types before use.
- validation-false: Preserve a valid false completion value and distinguish it from a missing or invalid field.
Passing target: Write and explain validation unaided for valid data, missing fields, null, wrong types and false values.

### Requirements: api-contracts
Scope: accepted
- contract-first: Define the task API in OpenAPI 3 YAML before handlers, including operation IDs, shared error schema and key examples; validate it.
- contract-generation: Identify and run pinned, deterministic generation commands for backend contracts/models and a TypeScript client.
- contract-use: Implement an operation against generated contracts without duplicating models; change YAML and regenerate when behavior changes.
Passing target: Produce and explain a validated contract and its generation/use workflow unaided for a task operation.

### Requirements: create-and-update-inputs
Scope: accepted
- input-create: Define create fields in the contract, excluding server-controlled IDs, and distinguish required from optional input.
- input-update: Model update input and apply the intended difference between omission and explicit values without overwriting omitted fields.
- input-utilities: Explain Partial and Pick on supplied types, their lack of runtime validation, and why they do not replace generated API models.
Passing target: Produce and explain create/update schemas and update application unaided, protecting IDs and preserving omitted fields.

### Requirements: crud-handlers
Scope: accepted
- crud-identity: Find tasks by stable ID, not array position, and distinguish missing records from existing ones.
- crud-lifecycle: Implement create, read, update and delete against generated contracts, preserving unmodified fields and intended state transitions.
- crud-responses: Return contract-defined response types/statuses for successful operations and missing tasks; keep async signatures consistent.
Passing target: Implement and explain the task CRUD lifecycle unaided, including stable identity, updates, deletion and missing records.

### Requirements: error-handling
Scope: accepted
- error-classify: Distinguish invalid requests, missing tasks and unexpected failures; map them to contract-defined error responses.
- error-boundary: Handle asynchronous failures at the handler boundary without swallowing them or returning a false success.
- error-safe: Return the shared error shape without internal details and log diagnostic information without request content or secrets.
Passing target: Implement and explain the three failure categories unaided, with consistent safe responses and diagnostic handling.

### Requirements: api-tests
Scope: accepted
- tests-lifecycle: Automate the full create/read/update/delete lifecycle with assertions on responses and stored state.
- tests-validation: Cover invalid bodies, omitted update fields, false values and missing IDs with meaningful contract-based assertions.
- tests-failure: Test an unexpected async failure, its safe response and absence of unintended state mutation; run tests with coverage.
Passing target: Write and run tests unaided demonstrating all three criteria and explain what each failure case protects.
