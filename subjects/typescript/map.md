# TypeScript Map

- [passed] variables-and-control-flow | sticking points: coercion, operator results, execution paths
- [todo] declarations-and-scope | depends on: variables-and-control-flow | sticking points: reassignment vs mutation, hoisting, temporal dead zone
- [todo] inference-and-literals | depends on: declarations-and-scope | sticking points: literal widening, annotations, as const
- [todo] collections-and-destructuring | depends on: inference-and-literals | sticking points: tuples vs arrays, shallow copies, aliasing
- [todo] functions-and-parameters | depends on: collections-and-destructuring | sticking points: missing returns, optional vs default parameters
- [todo] interfaces-and-type-aliases | depends on: functions-and-parameters | sticking points: structural compatibility, declaration merging
- [todo] unions-intersections-and-narrowing | depends on: interfaces-and-type-aliases | sticking points: safe property access, conflicting intersections, discriminants
- [todo] special-types | depends on: unions-intersections-and-narrowing | sticking points: any vs unknown, never vs void, strict null checking
- [todo] optional-and-nullish-values | depends on: special-types | sticking points: omitted vs undefined vs null, falsy vs nullish
- [todo] generics | depends on: functions-and-parameters, unions-intersections-and-narrowing | sticking points: input/output relationships, constraints, keyof
- [todo] classes-and-inheritance | depends on: interfaces-and-type-aliases | sticking points: private vs #private, abstract members, overriding
- [todo] assertions-guards-and-validation | depends on: special-types, optional-and-nullish-values | sticking points: assertions do not validate, type-predicate correctness
- [todo] utility-types | depends on: generics, optional-and-nullish-values | sticking points: shallow transformations, derived types, no runtime validation
- [todo] promises-and-async | depends on: functions-and-parameters, special-types | sticking points: Promise vs resolved value, absence vs rejection, concurrency
- [todo] modules-and-configuration | depends on: interfaces-and-type-aliases, promises-and-async | sticking points: type vs runtime exports, runtime-compatible configuration
- [todo] pitfalls-and-idioms | depends on: assertions-guards-and-validation, utility-types, modules-and-configuration | sticking points: unchecked assertions, unhandled rejection, exhaustive handling

## Topic Scope

Every passing target requires completing the topic's entire checklist unaided through short coding, prediction,
or explanation tasks. No CRUD project or time limit. Sticking points are annotations, not additional requirements.

### Requirements: variables-and-control-flow
Scope: accepted
- basics-values: Identify primitive types and predict arithmetic, comparison, logical-operator, and coercion results.
- basics-flow: Write a short function using conditions and iteration; explain its execution paths.
Passing target: Correctly predict supplied expressions and implement/explain the function.

### Requirements: declarations-and-scope
Scope: accepted
- scope-bindings: Explain reassignment versus mutation for const, and choose appropriately between let and const.
- scope-lifetime: Predict block/function scope, shadowing, and access-before-declaration behavior for let, const, and var.
Passing target: Correctly explain declaration choices and predict scope examples.

### Requirements: inference-and-literals
Scope: accepted
- inference-types: Predict inferred types and identify where explicit annotations clarify or constrain a declaration.
- inference-literals: Explain literal widening and use literal unions and as const appropriately.
Passing target: Predict inferred types and write declarations meeting supplied constraints.

### Requirements: collections-and-destructuring
Scope: accepted
- collections-shapes: Define and use typed arrays, tuples, and objects; distinguish tuple positions from array elements.
- collections-unpacking: Use destructuring, defaults, rest, and spread; explain shallow-copy and aliasing behavior.
Passing target: Write a small data transformation and correctly explain its types and mutation effects.

### Requirements: functions-and-parameters
Scope: accepted
- functions-signatures: Type function parameters and return paths, including possible missing results.
- functions-arguments: Use optional, default, and rest parameters; predict behavior for omitted arguments and explicit undefined.
Passing target: Implement and explain functions covering both requirements.

### Requirements: interfaces-and-type-aliases
Scope: accepted
- shapes-declarations: Express object contracts using both interfaces and type aliases; explain structural compatibility.
- shapes-differences: Explain extension, declaration merging, and aliases for unions; justify a suitable choice.
Passing target: Define compatible contracts and explain the relevant differences without treating either construct as universally preferable.

### Requirements: unions-intersections-and-narrowing
Scope: accepted
- composition-types: Define unions and intersections; explain allowed values, safe property access, and conflicting property types.
- composition-narrowing: Narrow unions using primitive checks, property checks, and discriminants.
Passing target: Predict accepted/rejected assignments and implement a correctly narrowed branching function.

### Requirements: special-types
Scope: accepted
- special-boundaries: Compare any and unknown, including compile-time checks versus runtime behavior.
- special-results: Distinguish never, void, null, and undefined; use them appropriately for non-returning functions, ignored results, and missing values under strict null checking.
Passing target: Correctly classify examples and write appropriate signatures and safe access checks.

### Requirements: optional-and-nullish-values
Scope: accepted
- optional-properties: Model optional properties and distinguish omission, explicit undefined, and null, stating relevant compiler assumptions.
- optional-operators: Use optional chaining and nullish coalescing while preserving valid false, 0, and empty-string values; contrast with truthiness defaults.
Passing target: Implement and explain missing-value handling for all listed cases.

### Requirements: generics
Scope: accepted
- generic-relationships: Write a reusable generic function that preserves the relationship between input and output types.
- generic-constraints: Use constraints and keyof for safe property access; explain inference and rejected calls.
Passing target: Implement and explain both an unconstrained transformation and constrained property-access function without falling back to any.

### Requirements: classes-and-inheritance
Scope: accepted
- classes-members: Implement a class with constructor initialization and public, protected, and private members; distinguish TypeScript private from JavaScript #private.
- classes-abstraction: Extend an abstract class, implement its abstract member, and explain inherited versus overridden behavior.
Passing target: Implement the class hierarchy and correctly explain access restrictions and runtime behavior.

### Requirements: assertions-guards-and-validation
Scope: accepted
- safety-assertions: Explain why type assertions and non-null assertions perform no runtime validation; identify unsafe uses.
- safety-validation: Write a user-defined type guard for unknown object input, validating required and optional fields without rejecting valid falsy values.
Passing target: Audit assertion examples and implement/explain a guard covering valid, missing, null, and wrong-type inputs.

### Requirements: utility-types
Scope: accepted
- utilities-objects: Apply Partial, Required, Pick, Omit, Record, and Readonly; explain resulting shapes and shallow behavior.
- utilities-derived: Use Exclude, Extract, NonNullable, Parameters, ReturnType, and Awaited to derive types; explain that utilities do not validate runtime data.
Passing target: Derive requested types and correctly predict accepted/rejected assignments.

### Requirements: promises-and-async
Scope: accepted
- promises-results: Type Promise results and async functions; distinguish Promise objects, resolved values, missing results, and rejection.
- promises-errors: Write an awaited caller with error handling; explain sequential versus concurrent execution and safely inspect an unknown caught value.
Passing target: Implement and explain success, absence, and rejection paths, plus an appropriate concurrency choice.

### Requirements: modules-and-configuration
Scope: accepted
- modules-boundaries: Split a small example across modules using named/default exports and type-only imports; distinguish type and runtime exports.
- modules-config: Explain a supplied configuration's strict, target, module, moduleResolution, include, and outDir settings in its stated runtime context.
Passing target: Produce consistent imports/exports and explain how the supplied configuration affects checking, output, and resolution.

### Requirements: pitfalls-and-idioms
Scope: accepted
- idioms-audit: Identify and correct accidental any, unchecked assertions, truthiness-based missing checks, and unhandled Promise rejection in short examples.
- idioms-design: Refactor a loosely typed example using inference, a discriminated union with exhaustive handling, and an appropriate existing utility type.
Passing target: Correct the listed pitfalls and explain why the refactored example is safer.
