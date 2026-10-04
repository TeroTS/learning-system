# Current Slice

Status: done

## Slice Goal
- Let the learner recall due cards before seeing their backs and see a result and next due date for each graded answer.

## Slice Boundary
- Learner runs `review` for a subject and answers each due card's front from memory; the skill judges supported answers, shows the result and next due date, records wrong answers and one session line, and `scripts/cards.py grade` changes each reviewed card's box and due date.

## Stories In Scope
- `US-05 Review due cards`

## Stories Completed In This Slice
- `US-05 Review due cards`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (grade CLI, errors, atomic writes), 2 (Leitner transitions and intervals), 5 (mistakes), 6 (sessions), 7 (read-only sources), and 8 (portable skill).

## Decision Inputs
- `DECISIONS.md`: Core Business Rules (`review` judges answers and calls grade); Interface / Contract Expectations (grading only against supplied sources, no grading without a source).

## Shared State Required Now
- Existing subject and validated card storage; learner-supplied sources for correctness judgments; append-only mistake and session logs.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/review/SKILL.md`.
- `python3 scripts/cards.py grade <subject> <id> --result right|wrong [--today YYYY-MM-DD] [--subjects-dir PATH]`.
- CLI-only card updates and skill-owned appends to `mistakes.md` and `sessions.md`.

## Tests Required
- Test first: every right/wrong box transition, box-5 cap, new-box intervals, grading-date scheduling, calendar boundaries, unchanged other card fields, id ordering, and local-date default.
- Unknown ids, missing storage, invalid subject/date/data, usage errors, date overflow, and write failures preserve storage and disclose no learner content.
- Real subprocess integration: list due cards, grade recalled results, observe JSON results and next due dates, and list again to verify rescheduling.
- Review skill instructions for answer-before-back, source-only judgments, missing sources, mistake capture, confirmed-card suggestions, one session line, and safe failure/retry handling.
- No automated skill-Markdown tests per SPEC.md. No agent-session harness exists; CLI end-to-end tests cannot validate live learner interaction or agent-owned log writes.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.

## Not Now
- US-06 explainer and US-07 Socratic questioner; examiner and other learning roles.
- Automatic answer matching, a live agent test harness, new scheduling rules, concurrency controls, and sample learner data.

## Done When
- Grade prints the updated card, persists the exact contracted box transition and new due date atomically, and leaves unrelated cards unchanged.
- The portable review skill withholds backs until attempts, grades only with applicable sources, records wrong answers, and appends exactly one session line.
- Suggested cards are added only on explicit learner confirmation through the existing add CLI; failed or uncertain grades are not blindly retried.
- Tests, real CLI integration, skill instruction review, lint, formatting, and unchanged coverage pass.

## Completion Summary
- Added `scripts/cards.py grade`: every right/wrong Leitner transition, box-5 cap, new-box interval scheduling from the grading date, and atomic id-ordered persistence with unrelated cards unchanged.
- Added the portable review skill: captured/front-only due output before attempts, source-supported judgments, next due dates from grade results, automatic mistake capture, confirmed-card suggestions, and one session line.
- Instruction review covered US-05 and the listed contracts, including no sources, unsupported or conflicting backs, no due cards, interrupted sessions, partial writes, and non-idempotent retry safety.
- Tests were written first and observed failing because grade was missing. Real CLI subprocess integration covers due → grade right/wrong → due, next-day visibility, and unknown-id preservation.
- `make test`, `make coverage`, and `make check` passed: 48 tests, formatting, lint, and 100% statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner review or automated agent-session end-to-end test was run; answer-before-back and agent-owned log appends were reviewed as instructions, not exercised by the CLI integration tests.

## Next Slice Recommendation
- `US-06 Get unstuck with the explainer`. Keep US-07 Find gaps with the Socratic questioner and US-08 Get examined on a topic in view, but outside that slice.
