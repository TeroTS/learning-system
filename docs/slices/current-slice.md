# Current Slice

Status: done

## Slice Goal
- Let the learner see what each of their explanation formats missed or got wrong against the subject's sources.

## Slice Boundary
- Learner runs `listener` and supplies transcribed speech, writing, and/or a drawing description; the skill grades each supplied explanation against subject sources, shows format-specific findings, appends supported missed points to `mistakes.md`, and writes one session line containing the grades.

## Stories In Scope
- `US-10 Explain back to the listener`

## Stories Completed In This Slice
- `US-10 Explain back to the listener`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (confirmed-card add CLI), 3 (goal and level context), 5 (mistake log), 6 (graded session line), 7 (sources are the only grading basis and read-only), and 8 (portable skill).

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject folder, learner explanations labeled by supplied format, applicable sources, and append-only mistake/session logs.
- Source-backed criteria and per-format grades remain in the conversation; no saved explanations, transcripts, or new grading model.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/listener/SKILL.md`.
- Read-only `subjects/<subject>/sources/`.
- Appends to `mistakes.md` and `sessions.md`; existing `scripts/cards.py add` only for confirmed suggestions.

## Tests Required
- Review instructions against US-10: production before feedback, source-only grading, independent feedback/grade for every supplied format, and specific missed or incorrect ideas tied to source evidence.
- Check one or multiple formats, absent optional formats, unclear transcripts/drawing descriptions, unsupported audio/image input, contradictory explanations, source-derived grade basis, and no confirmed mistakes.
- Check missing, insufficient, or conflicting sources; no unsupported grade, correction, or card; no invented speech delivery or unseen drawing details.
- Check automatic mistake capture without duplicate inflation, confirmed-only card additions, safe subject paths, local dates, one graded session line, preservation of existing logs, and failed/uncertain persistence.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live listener grading, confirmations, and agent-owned logs cannot be exercised by repository end-to-end tests. Existing CLI tests cover card addition, not the skill's confirmation behavior.

## Not Now
- US-11 sparring partner and US-12 clerk; diagnostician and other learning roles.
- Audio transcription, image recognition, mandatory multiple-format submissions, global grading scales, goal/map changes, stored explanations, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable listener skill grades each supplied explanation separately, reporting source-backed coverage and specific missing or incorrect ideas without judging unsupplied formats.
- Missing sources are explicitly reported and prevent grading; unsupported portions stay unverified rather than becoming invented mistakes.
- Supported mistakes are captured automatically, confirmed cards use the existing CLI, and exactly one session line records all supplied-format grades and limitations.
- Only permitted logs and confirmed card additions change; instruction review and existing automated checks pass.

## Completion Summary
- Added the portable listener skill: source-only grading of each supplied transcribed, written, or described-drawing explanation, with separate grades and specific missing or incorrect ideas.
- Instructions use an explicit source-backed grade basis, accept accurate paraphrases, distinguish partial verification, and avoid inventing speech delivery or unseen drawing content.
- Missing sources prevent grading; supported mistakes are captured automatically with affected formats, confirmed cards use the existing CLI, and one session line contains all supplied-format grades and limitations.
- Instruction review covered US-10 and the listed contracts, including single/multiple formats, absent optional formats, ambiguous inputs, unsupported audio/images, source conflicts, deduplicated mistakes, safe paths, and failed or uncertain persistence.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner session or automated agent-session end-to-end test was run; grading, confirmation, and agent-owned log behavior were reviewed as instructions.

## Next Slice Recommendation
- `US-11 Spar in a timed simulation`. Keep US-12 Organise notes with the clerk and US-13 Diagnose recurring mistakes in view for session/card handling and the eventual use of stored mistakes, but outside that slice.
