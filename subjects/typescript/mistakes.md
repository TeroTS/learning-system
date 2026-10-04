# Mistakes

- 2026-10-04 | socratic-questioner | object-and-function-types: expected console.log(result?.toLowerCase()) to print nothing when result is undefined | Optional chaining evaluates to undefined; console.log still executes and prints undefined (graded: agent judgement).
- 2026-10-04 | socratic-questioner | unions-and-narrowing: used value instanceof string to test an unknown value | string is a TypeScript type, not a runtime constructor; typeof value === "string" checks for a primitive string (graded: agent judgement).
- 2026-10-04 | socratic-questioner | unions-and-narrowing: returned the original value instead of the requested trimmed string | After narrowing to string, return value.trim() to remove surrounding whitespace (graded: agent judgement).
- 2026-10-04 | socratic-questioner | unions-and-narrowing: concluded that JavaScript has no string type after ReferenceError for string | JavaScript has primitive string values; the error means the identifier string is not defined as a runtime value (graded: agent judgement).
- 2026-10-04 | socratic-questioner | unions-and-narrowing: predicted typeof null returns null | typeof null returns the string "object"; an object check must exclude null before reading properties (graded: agent judgement).
- 2026-10-04 | socratic-questioner | unions-and-narrowing: used !=== to compare a value with null | !=== is invalid syntax; === checks strict equality and !== checks strict inequality (graded: agent judgement).
