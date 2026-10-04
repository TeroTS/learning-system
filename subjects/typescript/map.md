# TypeScript Map

- [todo] object-and-function-types | sticking points: optional fields, parameter types, return types
- [todo] unions-and-narrowing | depends on: object-and-function-types | sticking points: unknown vs any, missing values, runtime type checks
- [todo] async-functions | depends on: unions-and-narrowing | sticking points: Promise return types, undefined results, rejected promises
- [todo] request-validation | depends on: unions-and-narrowing | sticking points: compile-time types do not validate JSON, false vs missing
- [todo] api-contracts | depends on: object-and-function-types | sticking points: OpenAPI-first design, generated types vs handwritten duplicates
- [todo] create-and-update-inputs | depends on: request-validation, api-contracts | sticking points: omitted vs explicit values, Partial and Pick, protecting IDs
- [todo] crud-handlers | depends on: async-functions, create-and-update-inputs | sticking points: ID vs array index, missing tasks, response types
- [todo] error-handling | depends on: crud-handlers | sticking points: validation vs not-found vs unexpected failures, consistent error responses
- [todo] api-tests | depends on: error-handling | sticking points: CRUD lifecycle, invalid requests, false values, missing IDs
