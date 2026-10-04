# Current Slice

Status: done

## Slice Goal
- Let the learner see their demonstrated level and first failure point on one topic, with only that topic's map status updated.

## Slice Boundary
- Learner runs `examiner` on a topic and answers progressively harder questions one at a time until the first clear failure or guess, or demonstrates the goal-fitted target; the skill reports the level and stopping point, changes only that topic to `learning` or `passed`, captures mistakes, and appends one scored session line.

## Stories In Scope
- `US-08 Get examined on a topic`

## Stories Completed In This Slice
- `US-08 Get examined on a topic`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (confirmed-card add CLI), 3 (goal and level), 4 (target-topic status only; absent topic leaves map unchanged), 5 (mistakes), 6 (scored session), 7 (source-only grading), and 8 (portable skill).

## Decision Inputs
- `DECISIONS.md`: Core Business Rules (examiner asks increasingly hard questions until failure); Interface / Contract Expectations (no grading without sources).

## Shared State Required Now
- Existing subject, optional goal, one selected map topic, applicable learner-supplied sources, and append-only mistake/session logs.
- A finite source-supported difficulty ladder fitted to the goal, with a stated target for passing; answers and exam progression remain in the conversation.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/examiner/SKILL.md`.
- Only the selected topic's status token in `subjects/<subject>/map.md`.
- Appends to `mistakes.md` and `sessions.md`; existing `scripts/cards.py add` only for confirmed suggestions.

## Tests Required
- Review instructions against US-08: one question at a time, each scored question harder, production before feedback, immediate stop on clear failure or guess, and source-supported level and score reporting.
- Check first-question failure, correct guesses, all target levels completed, ambiguous answers, missing goal/sources, learner interruption, and insufficient or conflicting evidence.
- Check only the exact selected topic's status changes; absent, duplicate, or malformed topics leave the map unchanged; preserve all other map bytes and handle write failures safely.
- Check automatic mistake capture, confirmed-only cards, local dates, existing log preservation, exactly one scored session line, and failed/uncertain writes or adds.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live exams, topic-status edits, and agent-owned logs cannot be exercised by repository end-to-end tests. Existing CLI tests cover card addition, not learner confirmation.

## Not Now
- US-09 checker and US-10 listener; other learning roles.
- Bulk exams, map creation or reordering, prerequisite status changes, fixed global score thresholds, stored transcripts, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable examiner skill tests one topic with source-supported, progressively harder questions and stops at the first clear failure or guess.
- It reports the highest demonstrated level, explicit score basis, and failure or target-completion point; incomplete or ungraded sessions do not falsely pass.
- Only the examined topic's existing status changes to `learning` on failure/guess or `passed` on demonstrated target completion; supported mistakes and one session line are appended.
- Cards are suggested from session mistakes and added only on explicit confirmation; instruction review and existing automated checks pass.

## Completion Summary
- Added the portable examiner skill: one-topic, source-supported questions with increasing difficulty, immediate stop on first clear failure or guess, and an announced goal-fitted target for passing.
- Instructions report demonstrated level and score basis, automatically capture supported mistakes, and update only the selected topic's existing status token while preserving all other map content.
- Missing sources, inconclusive evidence, or interruption do not produce a false pass; missing, duplicate, or malformed map entries are reported without map changes.
- Card suggestions use supported session mistakes and require explicit confirmation through the existing CLI; exactly one scored or explicitly ungraded session line is appended.
- Instruction review covered US-08 and the listed contracts, including first-question failure, correct guesses, target completion, ambiguous answers, absent goals/maps/sources, partial writes, safe paths, and retry safety.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner exam or automated agent-session end-to-end test was run; questioning, map-status edits, confirmations, and log behavior were reviewed as instructions.

## Next Slice Recommendation
- `US-09 Check work with the checker`. Keep US-10 Explain back to the listener and US-11 Spar in a timed simulation in view for shared source-supported feedback, mistake/session logs, and confirmed-card suggestions, but outside that slice.
