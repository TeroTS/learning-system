# Current Slice

Status: done

## Slice Goal
- Let the learner see specific errors, missing steps, and possible shorter paths in their own work without having it rewritten.

## Slice Boundary
- Learner runs `checker` and supplies a summary, proof, code, or solution; the skill reviews each intermediate step against a rubric and shows located findings and shorter-path opportunities, appending supported mistakes and one session line.

## Stories In Scope
- `US-09 Check work with the checker`

## Stories Completed In This Slice
- `US-09 Check work with the checker`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (confirmed-card add CLI), 3 (goal context and missing-level handling), 5 (mistake log), 6 (session log), 7 (read-only sources and source-only grading), and 8 (portable skill).

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject folder, learner-supplied work and rubric, applicable sources, and append-only mistake/session logs.
- Work, review checklist, and located findings remain in the conversation; no copied learner artifacts or new rubric storage.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/checker/SKILL.md`.
- Skill-owned appends to `subjects/<subject>/mistakes.md` and `sessions.md`.
- Existing `scripts/cards.py add` only for confirmed mistake-based suggestions.

## Tests Required
- Review instructions against US-09: learner work before feedback, explicit rubric, each intermediate step reviewed, findings tied to exact locations and source evidence, and shorter paths described without rewriting work.
- Check summaries, proofs, code, and solutions; missing work/rubric/intermediate steps; ambiguous content; no errors; cascading errors; and static-review limitations.
- Check missing, insufficient, or conflicting sources, safe subject paths, preservation of learner work, automatic mistake capture, confirmed-only cards, local dates, one session line, and failed/uncertain persistence.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live checking, confirmation, and agent-owned log writes cannot be exercised by repository end-to-end tests. Existing CLI tests cover card addition, not the skill's confirmation behavior.

## Not Now
- US-10 listener and US-11 sparring partner; other learning roles.
- Rewriting or executing learner work, topic-status updates, numeric grading schemes, stored rubrics/transcripts, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable checker skill reviews learner-produced work step by step against a clear rubric and applicable sources.
- Every finding names a specific step or location, distinguishes confirmed mistakes from uncertainties and downstream effects, and identifies supported shorter paths without supplying replacement work.
- Supported mistakes are captured automatically, cards require explicit confirmation through the CLI, and exactly one session line records the review and limitations.
- Only permitted logs and confirmed card additions change; instruction review and existing automated checks pass.

## Completion Summary
- Added the portable checker skill: review learner-produced summaries, proofs, code, or solutions in order against an explicit rubric and applicable sources.
- Findings identify exact work locations, rubric criteria, and source evidence; shorter-path opportunities are described without rewriting or modifying learner work.
- Instructions distinguish confirmed mistakes, cascading effects, unverified portions, and static code-review limitations; missing sources do not produce invented grades or corrections.
- Supported mistakes are captured automatically, cards require explicit confirmation through the existing CLI, and exactly one append-only session line records the outcome and limitations.
- Instruction review covered US-09 and the listed contracts, including missing work/rubrics/steps, unclear content, no errors, source conflicts, safe paths, interrupted reviews, and failed or uncertain persistence.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner session or automated agent-session end-to-end test was run; review, confirmation, and log behavior were reviewed as instructions.

## Next Slice Recommendation
- `US-10 Explain back to the listener`. Keep US-11 Spar in a timed simulation and US-12 Organise notes with the clerk in view for shared session logs and confirmed-card suggestions, but outside that slice.
