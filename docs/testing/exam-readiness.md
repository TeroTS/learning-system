# Exam-readiness regression scenarios

## Running the checks

```bash
.venv/bin/python -m unittest tests.test_exam_readiness
make test
make coverage
make check
```

The automated checks protect required instructions and gate placement; they do not test an agent's behavior.
For behavioral replay, give an agent the relevant skill and one scenario below in an isolated temporary repository,
with synthetic subject files. Inspect its next response and any file changes. Do not use or modify learner files.
A readiness refusal must not count as a failed scored attempt. Apply normal session logging when the session ends.

## Common fixture

Topic: `unions-and-narrowing`. Goal: safely handle values in a TypeScript task API.

```md
# TypeScript Map

- [todo] object-and-function-types
- [todo] unions-and-narrowing | depends on: object-and-function-types | sticking points: unknown vs any, missing values, runtime type checks
```

Unless specified otherwise, the current session ends with a correct unaided `typeof` narrowing correction.
Session evidence records resolved production on runtime type checks and missing values, but nothing comparing
`unknown` with `any`. There are no applicable sources, so the existing agent-judgement rule applies.

## Scenarios

| Case | Skill / input | Required next behavior |
| --- | --- | --- |
| Single correction | `socratic-questioner`; common fixture | Name the uncovered `unknown` vs `any` concept and offer continued learning; do not offer a whole-topic exam. |
| Single redo | `explainer`; same evidence, successful unaided narrowing redo | Same coverage gap; no automatic exam offer. |
| Vague history | Either learning skill; historical entry says only "topic understood" | Treat coverage as unknown, not complete; leave history unchanged. |
| Complete evidence | Either learning skill; add concrete resolved production comparing `unknown` and `any` | Offer an exam handoff after finishing the session; wait for confirmation. Readiness is not a pass. |
| Premature consent | `examiner`; another skill offered an exam and learner answered "ok" | Independently identify missing coverage; do not ask the first scored question or reinterpret consent as diagnostic. |
| Explicit diagnostic | `examiner`; learner requests a diagnostic despite missing coverage | Disclose the gap and normal map-status effects; obtain informed confirmation before asking a scored question. Retain the whole-topic target. |
| Interrupted exam | `examiner`; ready exam starts, learner stops before answering | Stop; record interruption with no answers graded; preserve map bytes. |
| Passive exposure | Either learning skill; agent previously explained `unknown` vs `any`, learner produced nothing | Treat that concept as uncovered; explanation alone is not evidence. |
| Unresolved attempt | Either learning skill; learner compared `unknown` and `any` incorrectly, with no correction | Name the unresolved concept; no readiness claim. |
| Aided but resolved | Either learning skill; learner's own comparison is correct after assistance | Count coverage, retain the aided outcome; do not claim unaided mastery. |
| Missing scope | Any of the three skills; map missing or topic ambiguous | Clarify scope and evidence, not assume readiness or invent a map. |

## Verification record

- Instruction review against these scenarios: completed. Both handoffs and the examiner use the same readiness rule;
  concept-specific session logging preserves the existing format and historical entries.
- Automated instruction-contract checks: observed failing before the skill changes and passing afterward.
- Live independent agent replay: not run. This repository has no behavioral evaluation runner; the scenarios above
  are the replay checklist, not a claim that agent compliance has been proven.
