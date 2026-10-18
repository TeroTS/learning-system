# React.js Map

- [todo] react-mental-model | sticking points: rendering vs DOM updates
- [todo] components-and-props | depends on: react-mental-model | sticking points: component vs element; read-only props
- [todo] conditional-ui-and-lists | depends on: components-and-props | sticking points: stable keys and component identity
- [todo] events-and-state | depends on: components-and-props | sticking points: state snapshots; mutation; queued updates
- [todo] forms-and-shared-state | depends on: events-and-state | sticking points: controlled inputs; duplicated state
- [todo] effects-and-lifecycle | depends on: events-and-state | sticking points: unnecessary effects; stale closures; cleanup
- [todo] refs-and-dom | depends on: effects-and-lifecycle | sticking points: refs do not trigger rendering
- [todo] custom-hooks | depends on: effects-and-lifecycle | sticking points: sharing logic vs sharing state
- [todo] context | depends on: forms-and-shared-state | sticking points: provider scope; unnecessary context
- [todo] routing | depends on: conditional-ui-and-lists, events-and-state | sticking points: URL state; nested routes
- [todo] rest-api-data | depends on: custom-hooks, conditional-ui-and-lists | sticking points: HTTP failures; request races
- [todo] styling | depends on: forms-and-shared-state | sticking points: className; CSS scope; accessible interactions
- [todo] memoization | depends on: custom-hooks, context | sticking points: referential equality; premature optimization
- [todo] testing-and-debugging | depends on: rest-api-data, routing, styling, memoization, refs-and-dom | sticking points: testing behavior rather than internals
- [todo] modern-react-patterns | depends on: testing-and-debugging | sticking points: urgent vs non-urgent updates; Suspense limitations

## Topic Scope

### Requirements: react-mental-model
Scope: accepted
- mental-declarative: Explain declarative UI as a function of inputs and contrast it with manually updating DOM elements.
- mental-rendering: Explain React elements, the component tree, render and commit, and reconciliation; distinguish a render from an actual DOM change.
Passing target: Explain both requirements accurately using a small supplied UI scenario, unaided.

### Requirements: components-and-props
Scope: accepted
- components-tsx: Write and mount function components using TSX expressions, fragments, and typed read-only props.
- components-composition: Compose parent and child components using props, children, and callback props; explain their data flow.
Passing target: Implement a small composed UI and explain both requirements unaided.

### Requirements: conditional-ui-and-lists
Scope: accepted
- ui-conditions: Implement conditional UI using branches, ternaries, and logical expressions without accidentally rendering unwanted values.
- ui-keys: Render a typed collection with stable sibling-unique keys and explain how keys affect identity and state during insertion, deletion, and reordering.
Passing target: Implement both requirements and correctly predict the supplied list-reordering behavior unaided.

### Requirements: events-and-state
Scope: accepted
- state-events: Implement typed event handlers and useState-driven interactions; explain what triggers a render and why calling a setter does not change the current render's state snapshot.
- state-updates: Predict batched updates and implement functional updates and immutable object/array changes without mutation.
Passing target: Build a small interactive component and correctly explain its queued updates, covering both requirements unaided.

### Requirements: forms-and-shared-state
Scope: accepted
- forms-controlled: Implement a form with controlled text, checkbox, and select inputs, submission handling, and visible validation feedback.
- forms-sharing: Coordinate sibling components by lifting state to their nearest shared parent; derive values instead of duplicating state.
Passing target: Implement and explain a small coordinated form covering both requirements unaided.

### Requirements: effects-and-lifecycle
Scope: accepted
- effects-lifecycle: Explain mount, update, unmount, render purity, and development Strict Mode checks; distinguish event logic and derived values from external synchronization.
- effects-synchronization: Implement an effect with complete dependencies and cleanup for a subscription or timer; explain reruns and fix a stale closure or effect loop.
Passing target: Correctly classify supplied cases and implement and explain the synchronization task, covering both requirements unaided.

### Requirements: refs-and-dom
Scope: accepted
- refs-dom: Use a typed DOM ref to focus an input after a user action, handling a possibly null element.
- refs-state: Use a ref for a persistent value that need not drive UI; explain ref vs state behavior and why refs must not hide reactive dependencies.
Passing target: Implement both ref uses and explain their rendering behavior unaided.

### Requirements: custom-hooks
Scope: accepted
- hooks-extract: Extract reusable stateful logic into a typed custom hook while following the Rules of Hooks.
- hooks-isolation: Use the hook in two components and demonstrate that their state is independent unless explicitly shared.
Passing target: Implement the hook and both consumers, explaining logic reuse and state isolation unaided.

### Requirements: context
Scope: accepted
- context-implementation: Implement a typed context, provider, and consumer hook with explicit handling of a missing provider.
- context-choice: Explain provider scope and consumer updates, and justify context or ordinary props for supplied sharing scenarios.
Passing target: Implement the shared value and correctly explain both requirements unaided.

### Requirements: routing
Scope: accepted
- routing-navigation: Implement React Router navigation with links, nested routes, an outlet, and a not-found route.
- routing-url-state: Read route parameters and search parameters and use them to select displayed content; explain client-side navigation and direct-URL hosting requirements.
Passing target: Implement and explain a small routed interface covering both requirements unaided.

### Requirements: rest-api-data
Scope: accepted
- data-status: Fetch data from a supplied REST endpoint with explicit loading, success, error, and empty UI states; handle non-success HTTP responses.
- data-lifecycle: Prevent stale requests from overwriting newer results and handle cleanup; explain when an effect, event handler, or router data loader is appropriate.
Passing target: Implement the data UI against a supplied response shape and explain failure and race behavior, covering both requirements unaided.

### Requirements: styling
Scope: accepted
- styling-css: Style components using className, ordinary CSS or CSS Modules, conditional classes, and basic responsive layout.
- styling-accessibility: Use semantic controls, associated labels, visible keyboard focus, and understandable validation/status feedback.
Passing target: Build a responsive styled form or interactive component satisfying both requirements unaided.

### Requirements: memoization
Scope: accepted
- memo-identities: Explain referential equality and the different roles of useMemo, useCallback, and memo, including their limitations.
- memo-evidence: Inspect a supplied rerender/performance scenario and either apply justified memoization with correct dependencies or explain why none is needed.
Passing target: Explain the mechanisms and justify and verify the chosen change or non-change unaided.

### Requirements: testing-and-debugging
Scope: accepted
- testing-behavior: Write React Testing Library tests using accessible queries and user interactions for a component's initial UI, state changes, and form validation.
- testing-async: Test loading, success, empty, and failure behavior with mocked API responses and appropriate asynchronous queries.
- debugging-tools: Use React Developer Tools to inspect props, state, context, and commits; identify and fix a supplied rendering or state bug and verify it with a regression test.
Passing target: Produce passing behavior tests for all listed cases and demonstrate the debugging workflow, covering all three requirements unaided.

### Requirements: modern-react-patterns
Scope: accepted
- modern-transitions: Use useTransition or useDeferredValue in a supplied responsive-UI task and explain urgent vs non-urgent work and why this is not debouncing.
- modern-boundaries: Use lazy and Suspense for code loading and an error boundary for rendering failures; explain why ordinary effect-based fetching does not automatically activate Suspense.
- modern-design: Refactor a supplied component to remove duplicated derived state and unnecessary effects; explain state ownership and distinguish client components from Server Components at a conceptual level.
Passing target: Complete the small implementation/refactoring tasks and accurately explain their limits, covering all three requirements unaided.
