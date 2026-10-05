# Progression and exam-readiness regression scenarios

## Running the checks

```bash
.venv/bin/python -m unittest tests.test_exam_readiness
make test
make coverage
make check
```

Automated checks protect instruction contracts and gate placement, not agent behavior. For independent behavioral
replay, give an agent the relevant skill and one case in an isolated temporary repository with synthetic subject
files and `docs/contracts.md`. Inspect its next response and file changes. Never modify learner files for replay.
A gate refusal is not a failed scored attempt. Apply normal session logging only when a skill session ends.

## Common fixture

Goal: safely handle values in a TypeScript task API. No applicable sources; use the announced judgement fallback.
The prerequisite has a completed unaided exam; the selected topic has accepted scope but incomplete coverage.

```md
# TypeScript Map

- [passed] object-and-function-types
- [todo] unions-and-narrowing | depends on: object-and-function-types | sticking points: unknown vs any, missing values, runtime type checks

## Topic Scope

### Requirements: object-and-function-types
Scope: accepted
- object-return: Type a function whose return is a string or undefined and explain its branches.
Passing target: Write and explain the function unaided, including both return branches.

### Requirements: unions-and-narrowing
Scope: accepted
- union-unknown: Explain the checking difference between unknown and any and predict runtime behavior.
- union-missing: Distinguish undefined from empty string and false in checks and optional chaining.
- union-runtime: Read an unknown object's title using null, object, property and string checks.
Passing target: Complete all three requirements unaided, including predictions and a safe title reader.
```

Synthetic session evidence:

```md
# Sessions

- 2026-10-04 | examiner | object-and-function-types | object-return: resolved, unaided, wrote and explained both branches; target completed; 1/1; graded: agent judgement
- 2026-10-04 | socratic-questioner | unions-and-narrowing | union-missing: resolved, unaided, distinguished undefined, empty string and false; union-runtime: resolved, aided, wrote safe title reader; graded: agent judgement
```

## Scenarios

| Case | Input/change | Required next behavior |
| --- | --- | --- |
| General continuation | “Continue TypeScript” | Cite unknown `union-unknown`; offer it, not the next topic or an exam. |
| Single correction | Socratic session finishes with corrected title reader | `union-unknown` is still unknown; no exam offer. |
| Single redo | Successful explainer title-reader redo | Same gate; one successful task does not satisfy unrelated criteria. |
| Vague history | Add “topic understood” | No new coverage; leave history unchanged. |
| Complete evidence | Add resolved production for `union-unknown` | Offer accepted exam; no automatic pass or next-topic move. |
| Invented blocker | Agent considers exhaustiveness | It is absent from accepted scope; cannot block readiness or appear in passing criteria. |
| Legacy scope | Remove accepted scope sections | Offer mapmaker approval; neither normal nor diagnostic exam can start. |
| Premature consent | Examiner receives “ok” to an invalid exam offer | Independently gate; do not reinterpret consent as a diagnostic. |
| Explicit diagnostic | Learner requests diagnostic while `union-unknown` is unknown | Disclose gaps and normal status effects; obtain confirmation; keep whole accepted target. |
| Interrupted exam | Ready exam starts; learner stops without answering | Preserve map; record interruption, no score invented, no earlier evidence erased. |
| Clear failure | Ready exam; first answer is demonstrably wrong or admitted guess | Stop immediately; set only selected topic to `learning`; record tested IDs, not unasked success. |
| Completed exam | All accepted target criteria demonstrated unaided on fresh tasks | Set only selected topic to `passed`; offer the next dependency-ready topic through the gate. |
| Copied learning task | Examiner proposes the previously learned Task/getDescription exercise | Replace it before asking; same accepted concepts, different application and reasoning task. |
| Cosmetic change | Same exercise with renamed identifiers or swapped string values | Reject as recycled; names/values alone do not establish transfer. |
| Fresh application | Different context/data and reasoning task, all requirements still within accepted scope | Use it; standard type syntax may recur without adding concepts or changing the target. |
| Unknown task history | Legacy session summary does not identify previous examples | Choose a new scenario; report freshness unverified rather than proven novelty. |
| Duplicate discovered mid-exam | A presented question repeats a solved learning exercise | Withdraw unscored, replace at the same level before feedback; no learner failure or scored retry. |
| Explainer redo | Learner redoes the original task from the start | Preserve the required redo; do not convert it into a scored exam task. |
| Socratic follow-up | Learner's own attempt is reused to clarify reasoning | Allowed within learning; freshness restriction applies to scored exam tasks. |
| Historical pass | Learner declines a new exam after requesting instruction changes | Preserve the recorded pass and history; repository maintenance creates no learning-session entry. |
| Passive exposure | Agent explains `union-unknown`; learner produces nothing | Requirement remains unknown. |
| Aided resolution | Learner correctly produces `union-unknown` after help | Coverage resolved, aided; exam still required for a pass. |
| New mistake | Append substantive wrong `union-runtime` answer after earlier success | Latest applicable outcome controls: unresolved; offer that requirement in checklist order if it is the first gap. |
| No-production interruption | Append interrupted session after resolved production | Earlier resolved evidence remains applicable. |
| Changed criterion | Propose materially changed `union-runtime` criterion | New ID, no automatic evidence transfer, explicit approval before saving. |
| Scope amendment | Add approved scope to a legacy map | Preserve unaffected topic state and history; disclose any affected passed-topic reset. |
| Declined scope | Learner declines proposal | Map unchanged; do not claim accepted scope or resume an exam. |
| Unmet dependency | Change prerequisite to `todo` | Offer prerequisite first; explicit topic selection is not an override. |
| Dependency override | Learner requests bypass | Disclose unmet dependency and obtain confirmation; bypass applies only to disclosed request, no prerequisite pass. |
| Skip topic | Learner explicitly requests next topic | Disclose unfinished scope/dependencies and confirm; skip does not confer passes. |
| Re-exam | Learner explicitly requests re-exam of a passed topic | Use its accepted target and gate, not an automatic next-topic redirect. |
| Completion | All topics passed with accepted scope and resolved evidence | Report completion; no additional concepts invented. |
| Invalid completion | All topics marked passed but scope missing or a later misconception recorded | First invalid scope or unresolved requirement in map order blocks completion. |
| Broken map | Duplicate topic/requirement, dangling or cyclic dependency | Report ambiguity and offer mapmaker repair, not guessed routing. |

## Verification record

- Baseline: `make coverage` passed, 52 tests, 100% script coverage.
- Updated instruction-contract tests observed failing before instruction changes: 43 assertion failures across 9 tests.
- Rule review: the synthetic cases above have been compared against the shared progression table and affected instructions.
- Independent live agent replay: not run. This is a replay checklist, not a claim of proven agent compliance.
- Initial progression results are recorded in `docs/plans/deterministic-learning-progression.md`.
- Exam-freshness follow-up: two new instruction-contract tests observed failing before skill changes (12 assertion
  failures, no test errors). Final checks: 12 progression/freshness checks pass; `make check` passes all 60 tests,
  with 100% script coverage unchanged; `git diff --check` passes. Independent live replay remains unrun;
  these checks do not establish agent compliance.
