# Current Slice

Status: done

## Slice Goal
- Let the learner see their messy notes as a clean outline or proposed cards, with no new substantive content.

## Slice Boundary
- Learner runs `clerk` with their notes; the skill restructures only that material into the selected outline or card proposals, shows the result, appends one session line, and adds proposed cards through the CLI only after explicit confirmation.

## Stories In Scope
- `US-12 Organise notes with the clerk`

## Stories Completed In This Slice
- `US-12 Organise notes with the clerk`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (confirmed-card add CLI), 2 (non-empty card front/back), 6 (one session line), and 8 (portable skill); Contract 7 source files remain unchanged.

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject, learner-supplied notes, selected output form, and append-only session log.
- Outline, proposals, and confirmations stay in the conversation; no new notes file, outline store, or mistake data.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/clerk/SKILL.md`.
- Conversation-only outline or proposed cards.
- `subjects/<subject>/sessions.md`; existing `scripts/cards.py add` for explicitly confirmed proposals.

## Tests Required
- Review instructions against US-12: supplied notes satisfy production, output form is clarified, all substantive output is traceable to learner content, and formatting does not silently change meaning.
- Check duplicates, contradictions, uncertainty, incomplete notes/questions, empty input, and card pairs without a supported back; no invented corrections, explanations, headings that imply new facts, or imported source content.
- Check original notes remain unchanged, outline is not persisted into another subject file, cards need explicit confirmation, declined/unconfirmed cards are not added, and uncertain additions are not blindly retried.
- Check safe subject paths, local dates, contracted single-line formatting, existing log preservation, one session line, and failed or partial persistence.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live note transformation and confirmations cannot be exercised by repository end-to-end tests. Existing CLI tests cover card addition, not this skill's content-preservation or confirmation behavior.

## Not Now
- US-13 diagnostician; other learning roles.
- Correcting or grading notes, enriching from sources, mistake capture, goal/map changes, saved outlines/transcripts, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable clerk skill returns the learner's own content as an outline or card proposals without filling gaps or adding facts.
- Uncertainty and contradictions are preserved, original notes and sources remain untouched, and incomplete card backs are not invented.
- Cards are added only after explicit confirmation through the existing CLI, and exactly one session line records the outcome and any limitations.
- Instruction review and existing automated checks pass.

## Completion Summary
- Added the portable clerk skill: learner notes become the selected outline or card proposals using only supplied content and faithful restructuring.
- Instructions preserve qualifications, contradictions, unfinished thoughts, and original files; outlines stay in the conversation rather than being saved into unrelated subject files.
- Card proposals do not invent missing backs, and only explicitly confirmed pairs are added through the existing CLI; one session line records the actual transformation and additions.
- Instruction review covered US-12 and the listed contracts, including missing/ambiguous notes, duplicate handling, unsupported additions, revised or declined proposals, safe paths, and failed or uncertain persistence.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner session or automated agent-session end-to-end test was run; content preservation, confirmation, and session logging were reviewed as instructions.

## Next Slice Recommendation
- `US-13 Diagnose recurring mistakes`. This is the final explicit story remaining in `SPEC.md`; do not invent follow-up story IDs or additional scope after it.
