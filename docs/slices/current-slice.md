# Current Slice

Status: done

## Slice Goal
- Let the learner get past one stuck step and demonstrate an unaided redo of the task from the start.

## Slice Boundary
- Learner runs `explainer`, names a task and stuck step, receives an explanation of only that step, and attempts the entire task again without help; one session line records whether the redo succeeded unaided.

## Stories In Scope
- `US-06 Get unstuck with the explainer`

## Stories Completed In This Slice
- `US-06 Get unstuck with the explainer`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 3 (`goal.md` and missing-level handling), 6 (session log), 7 (read-only sources and no grading without sources), and 8 (portable skill); Contract 1 subject-name pattern.

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject folder, optional recorded goal and learner-supplied sources, and an append-only session log.
- Task, stuck step, learner attempt, and redo outcome remain in the current conversation, not a stored transcript.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/explainer/SKILL.md`.
- `subjects/<subject>/sessions.md` at skill runtime only.

## Tests Required
- Review instructions against US-06: production before explanation, one question per turn, recorded or stated level, explanation limited to the stuck step, and a full unaided redo before normal completion.
- Check vague task/step, missing goal or sources, failed or aided redo, abandonment before redo, unsafe subject names, existing log preservation, and failed or uncertain appends.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; preserve 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live explanations and learner redo behavior cannot be exercised by repository end-to-end tests.

## Not Now
- US-07 Socratic questioner and US-08 examiner; other learning roles.
- Mistake capture, card suggestions, goal/map updates, learner transcripts, sample data, and agent-session test infrastructure.

## Done When
- The portable explainer skill collects a concrete task, stuck step, learner attempt, and current level without supplying a full solution.
- Only the stuck step is explained; the learner must attempt the task again from the start without help before the session can be called complete.
- Exactly one contracted session line records the observed outcome and any verification limitations; no other subject files are changed.
- Instruction review and existing automated checks pass.

## Completion Summary
- Added the portable explainer skill: concrete task and stuck-step collection, learner production before explanation, and depth fitted to the recorded or stated level.
- Instructions limit explanation to the stuck step and require a fresh, unaided redo from the start before normal completion; failed, aided, partial, and abandoned attempts are not mislabeled as success.
- Writes only one contracted session line, preserving earlier entries and distinguishing source-verified outcomes from learner-reported or unverified outcomes.
- Instruction review covered US-06 and the listed contracts, including missing goal/sources, vague requests, unsafe subject paths, interrupted redo, and failed or uncertain log appends.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner session or automated agent-session end-to-end test was run; the skill's explanation, redo, and log behavior were reviewed as instructions.

## Next Slice Recommendation
- `US-07 Find gaps with the Socratic questioner`. Keep US-08 Get examined on a topic and US-09 Check work with the checker in view for shared mistake/session logs and confirmed-card suggestions, but outside that slice.
