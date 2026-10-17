# Express.js Map

- [todo] architecture-and-setup | sticking points: app creation vs starting the server
- [todo] routing-and-responses | depends on: architecture-and-setup | sticking points: params vs query; sending twice
- [todo] middleware-and-lifecycle | depends on: routing-and-responses | sticking points: registration order; hanging requests
- [todo] request-parsing-and-validation | depends on: middleware-and-lifecycle | sticking points: TypeScript types are not runtime validation
- [todo] crud-and-http | depends on: request-parsing-and-validation | sticking points: PUT vs PATCH; missing resources
- [todo] error-handling | depends on: crud-and-http | sticking points: async propagation; errors after headers are sent
- [todo] modular-routers | depends on: error-handling | sticking points: mount paths; parent route parameters
- [todo] authentication-and-authorization | depends on: modular-routers | sticking points: identity vs permission; middleware order
- [todo] security-and-cookies | depends on: authentication-and-authorization | sticking points: CORS is not authorization
- [todo] configuration-and-static-files | depends on: security-and-cookies | sticking points: unsafe configuration; relative static paths
- [todo] testing | depends on: configuration-and-static-files | sticking points: test isolation; untested failure paths
- [todo] versions-and-pitfalls | depends on: testing | sticking points: Express 4 assumptions in Express 5

## Scope conventions

Use Express 5, comparing Express 4 where behavior differs. All coding uses TypeScript.
Every passing target requires unaided production, graded by agent judgement.

Programming, Node.js, and TypeScript fundamentals are omitted based on the learner's reported experience;
that prerequisite knowledge remains provisional. Production-level scope here covers the API fundamentals below,
not database operations, deployment, or a complete identity provider.

## Topic Scope

### Requirements: architecture-and-setup
Scope: accepted
- setup-model: Explain Express's role, the application object, and the distinction between app configuration and listening.
- setup-app: Create a TypeScript Express app with a working JSON health endpoint and a separate server entry point.
Passing target: Explain the model and write both working files.

### Requirements: routing-and-responses
Scope: accepted
- routing-inputs: Implement routes using HTTP methods, path parameters, and query parameters; explain their values on req.
- routing-outputs: Demonstrate appropriate use of res.json(), res.send(), res.status(), and res.end(), including a bodyless response and prevention of double sends.
Passing target: Complete the route tasks and correctly predict their status, headers, and body.

### Requirements: middleware-and-lifecycle
Scope: accepted
- middleware-order: Trace application-level, router-level, and built-in middleware from incoming request to response, including unmatched requests.
- middleware-flow: Write middleware demonstrating next(), next(err), response termination, and next('route'); identify hanging requests and unintended fall-through.
Passing target: Predict supplied execution traces and implement the control-flow cases correctly.

### Requirements: request-parsing-and-validation
Scope: accepted
- parsing-bodies: Configure JSON and URL-encoded parsing before consumers; explain behavior for malformed JSON, mismatched content types, and oversized bodies.
- validation-boundary: Validate and normalize body, path, and query inputs at runtime; reject missing or invalid fields and prevent uncontrolled assignment of submitted properties.
Passing target: Write handlers that accept valid inputs and reject the specified invalid cases without relying on TypeScript types for validation.

### Requirements: crud-and-http
Scope: accepted
- crud-routes: Implement create, list, retrieve, update, and delete routes using a supplied in-memory store, including missing-resource behavior.
- crud-semantics: Choose and explain appropriate methods, status codes, resource URLs, PUT/PATCH behavior, and response bodies.
Passing target: Complete the CRUD route set and justify its HTTP behavior. Database implementation is not required.

### Requirements: error-handling
Scope: accepted
- errors-centralized: Implement final 404 handling and four-argument centralized error middleware with consistent, non-sensitive client errors.
- errors-async: Handle synchronous exceptions, rejected asynchronous handlers, and callback errors appropriately; delegate errors when headers have already been sent.
Passing target: Write the handlers and correctly trace each failure path under Express 5.

### Requirements: modular-routers
Scope: accepted
- routers-structure: Split the CRUD API into application setup, resource router, and handlers without unnecessary abstraction.
- routers-mounting: Demonstrate router mounting, router-local middleware, and parent parameters using mergeParams.
Passing target: Produce working modules and explain the resulting paths, middleware scope, and parameter visibility.

### Requirements: authentication-and-authorization
Scope: accepted
- auth-identity: Implement authentication middleware against a supplied credential verifier; reject absent or invalid credentials and make verified identity available downstream.
- auth-permissions: Implement resource-level authorization that distinguishes unauthenticated from forbidden requests and prevents access to another user's resource.
Passing target: Implement and explain successful, unauthenticated, and forbidden flows without trusting client-supplied identity. Building a credential issuer is excluded.

### Requirements: security-and-cookies
Scope: accepted
- security-browser: Configure a restricted CORS policy; explain preflight requests, credentials, cookie flags, and when cookie authentication requires CSRF protection.
- security-controls: Apply security headers, request-size limits, and rate limiting; explain HTTPS and trusted-proxy assumptions without exposing secrets or internal errors.
Passing target: Write the relevant middleware configuration and correctly analyze allowed and rejected request scenarios.

### Requirements: configuration-and-static-files
Scope: accepted
- config-environment: Read and validate required environment configuration, fail clearly on invalid startup values, and keep secrets out of responses and logs.
- config-static: Mount express.static at an explicit URL prefix using a stable filesystem path, without exposing private files.
Passing target: Implement both configurations and explain startup failure and static-file lookup behavior.

### Requirements: testing
Scope: accepted
- testing-supertest: Write isolated Supertest tests for successful CRUD operations, response statuses/bodies, and bodyless responses.
- testing-failures: Test invalid inputs, missing resources, unauthenticated/forbidden access, and asynchronous failures without starting a fixed-port server.
Passing target: Run a repeatable suite that verifies every listed case without shared mutable state leaking between tests.

### Requirements: versions-and-pitfalls
Scope: accepted
- versions-migration: Explain and correct Express 4/5 differences in rejected-promise handling, route-path syntax, req.body defaults, query parsing, and removed response signatures.
- pitfalls-review: Diagnose supplied examples involving middleware order, missing return after a response, double sends, missing responses, and misplaced error middleware.
Passing target: Correct the examples and explain their observable behavior; no full application rewrite required.
