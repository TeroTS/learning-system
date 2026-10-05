# Plan: Fixed Topic Scope and Predictable Progression

Status: workflow implemented; learner-map amendment pending explicit scope approval.

## Problem

The current readiness rules treat sticking points as a minimum checklist and let each agent infer additional
scope from the goal and sources. Continuation is not explicitly gated. Consequently, an agent can offer the
next topic before checking readiness, then invent a new blocker when challenged.

## Outcome

For the same accepted map and recorded evidence, the rules specify the same next action. Topic scope and passing
criteria are fixed before learning, not reconstructed during each session. Answer grading remains judgement-based
when no applicable source exists; instruction tests cannot guarantee agent compliance.

## 1. Lock the rules before implementation

Update `DECISIONS.md` and `SPEC.md` first, covering map creation, continuation, learning handoffs and exams:

- Each topic has a finite learner-approved list of observable requirements and a passing target.
- Sticking points remain helpful annotations, not an expandable readiness checklist.
- Goals and sources inform the proposed scope and answer grading; they cannot silently expand accepted scope.
- A requirement is resolved only through concrete learner production. Aided success establishes coverage, not mastery.
- Missing, vague or unverified evidence is unknown; a demonstrated misconception without a correction is unresolved.
- Only a completed unaided exam against the accepted target makes a topic `passed`.
- Scope changes and progression overrides require explicit learner approval.
- Retain the existing informed diagnostic-exam exception; it must use an accepted target, not an invented one.

## 2. Extend existing file contracts

Update `docs/contracts.md` before changing skills:

- Keep existing topic lines, names, dependency fields and status tokens compatible.
- Add per-topic sections in `map.md` for requirement IDs, observable success criteria and the passing target.
- Reuse the existing `sessions.md` result field for requirement IDs, outcomes and aided/unaided attribution.
- Derive coverage from evidence rather than maintaining a second mutable coverage store.
- Cite the supporting session entry when reporting coverage. Current-session production can also supply evidence.
- Specify conflict handling: use the latest substantive, applicable outcome for a requirement in append order;
  an interruption with no production does not erase earlier evidence.
- Requirement IDs remain stable for unchanged criteria. A materially changed criterion gets a new ID, so old
  evidence does not automatically satisfy it.
- Preserve historical session lines. Legacy entries count only when their specific demonstrated outcome clearly
  matches an accepted criterion; otherwise coverage remains unknown.

No new dependencies, scheduler, database, card format or tracking file.

## 3. Define one progression decision table

Apply the same table before offering continuation, an exam or the next topic:

| State | Required next action |
| --- | --- |
| Missing or unaccepted scope/target | Offer a mapmaker scope-approval handoff; do not invent completeness. |
| Required dependency not passed | Offer the earliest unmet dependency in map order; disclose any requested override. |
| Unknown or unresolved requirement | Offer the first such requirement in accepted checklist order and cite its evidence state. |
| Every requirement resolved; topic not passed | Offer the accepted topic exam; wait for confirmation. |
| Topic passed | Offer the first unpassed, dependency-ready topic in map order. |
| Every topic passed | Report map completion; do not expand scope automatically. |

A learner-selected topic is checked before automatic topic selection. Role changes still require confirmation.
An explicit skip does not mark a topic passed or satisfy its dependencies. Diagnostics require disclosure and
confirmation of gaps and normal status effects. Readiness alone never changes map status.

## 4. Update all affected instructions

- `AGENTS.md`: require the progression check for general requests such as “continue TypeScript,” before choosing a role.
- `.agents/skills/mapmaker/SKILL.md`: propose complete scope and targets, obtain approval, and support scope amendments.
- `.agents/skills/explainer/SKILL.md` and `.agents/skills/socratic-questioner/SKILL.md`: record requirement-specific
  production and apply the fixed gate; remove runtime scope expansion.
- `.agents/skills/examiner/SKILL.md`: independently check the gate and grade only the accepted target. Question
  wording can vary, but required concepts and passing criteria cannot change during the exam.
- `README.md`: document scope approval, coverage versus passing, and predictable continuation.

Clarify ownership: mapmaker owns scope changes; examiner still changes only the examined topic's status.
Scope-only amendments preserve unaffected statuses. Changing a passed topic's target invalidates that pass;
show the proposed reset and obtain approval before saving. Full map replacement retains its existing disclosed reset rule.

## 5. Test the regression before changing skills

Extend `tests/test_exam_readiness.py` with failing instruction-contract checks for accepted scope, fixed targets,
continuation gating, evidence citations, approvals and independent examiner checks. Add focused map-contract checks
in the same test module where practical.

Update `docs/testing/exam-readiness.md` with synthetic replay cases:

- “Continue learning” cannot offer the next topic while current requirements are unknown or unresolved.
- Complete coverage offers the exam, not an automatic pass or move onward.
- Exhaustiveness cannot become a blocker unless it is an accepted requirement.
- Legacy maps without scope require approval; vague session records remain unknown.
- Aided success counts as coverage but not unaided mastery.
- A later substantive mistake supersedes an earlier resolution; an unanswered interruption does not.
- Failed, interrupted and completed exams retain their distinct status effects.
- A scope amendment preserves unaffected state and does not reuse evidence for changed criteria.
- Dependency gaps, explicit skips and informed diagnostics follow the disclosed exception rules.

Use temporary synthetic subjects, never learner files. Automated checks verify instruction contracts, not live
agent behavior. Record replay results separately and do not claim behavioral verification unless actually run.

## 6. Approve TypeScript scope before resuming

After the workflow fix:

1. Propose explicit requirements and targets for the existing TypeScript map, using the goal and recorded evidence.
2. Separate required concepts from optional extras; do not automatically add exhaustiveness.
3. Obtain learner approval before writing `subjects/typescript/map.md`.
4. Produce a requirement-to-evidence table with session citations; mark ambiguous legacy evidence unknown.
5. Apply the progression table, including unmet prerequisites. Do not automatically start another interrupted exam.

Do not migrate other subjects without approval. Preserve existing mistakes, cards, sources and historical sessions.
Leave the unrelated modification in `subjects/aws-certified-solutions-architect-pro/sessions.md` untouched.

## Verification and completion

```bash
.venv/bin/python -m unittest tests.test_exam_readiness
make test
make coverage
make check
git diff --check
```

- Coverage must not decrease from the pre-change baseline and must meet the configured minimum.
- Decisions, specification, contracts, skills and README agree; remove the contradictory “minimum checklist” rule.
- Contract tests fail before instruction changes and pass afterward.
- Regression replay outcomes and limitations are recorded honestly.
- TypeScript learning resumes only after accepted scope and an evidence-based progression decision.

## Implementation record

- Updated decisions, specification (including US-15), map/session contracts, shared progression table, repository
  routing guidance, four affected skills, README and current-slice handoff.
- Replaced runtime scope inference with approved finite criteria and targets. Added cited evidence states,
  deterministic table ordering, approved amendments and explicit diagnostic/override handling.
- Instruction checks observed failing before skill changes: 43 assertion failures across 9 tests. Final suite has
  10 progression instruction-contract tests; these do not execute or guarantee live agent behavior.
- `.venv/bin/python -m unittest tests.test_exam_readiness`, `make test`, `make coverage`, `make check` and
  `git diff --check` passed. Final suite: 58 tests; script coverage remains 100%, matching the baseline.
- Regression scenario rule review documented in `docs/testing/exam-readiness.md`; independent live agent replay not run.
- `docs/plans/typescript-scope-proposal.md` contains the proposed requirements, targets, provisional evidence citations
  and prescribed next action. It is not an accepted subject map; approval and actual migration remain pending.
- No learner files were modified by this implementation. The unrelated pre-existing AWS session change was preserved.
