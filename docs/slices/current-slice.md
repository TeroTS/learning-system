# Current Slice

Status: done

## Slice Goal
- Let the learner see root misunderstandings behind recurring mistakes across subjects, with specific supporting evidence.

## Slice Boundary
- Learner runs `diagnostician`; the skill reads mistakes and sessions across all subjects, reports root misunderstandings with the specific mistakes supporting each, and appends exactly one session line to each subject with related findings.

## Stories In Scope
- `US-13 Diagnose recurring mistakes`

## Stories Completed In This Slice
- `US-13 Diagnose recurring mistakes`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contract 5 (read-only mistake evidence), Contract 6 (one diagnostician session line per subject with findings), and Contract 8 (portable skill); Contract 1 subject-name pattern.

## Decision Inputs
- None.

## Shared State Required Now
- Existing subjects' mistake and session logs, evidence locations, and the set of subjects supporting reported findings.
- Candidate patterns and the learner's hypothesis remain in the conversation; no diagnosis file, new mistake records, cards, or transcript store.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/diagnostician/SKILL.md`.
- Read all `subjects/*/mistakes.md` and `subjects/*/sessions.md` within safe subject folders.
- Append only to `sessions.md` of subjects with related reported findings.

## Tests Required
- Review instructions against US-13: all-subject reads, learner production before explanations, specific evidence for every root misunderstanding, and cross-subject patterns without forced connections.
- Check empty store, missing/empty mistake logs, session-only failures, isolated mistakes, duplicate entries, prior diagnostic outputs, historical improvement, ambiguous or contradictory evidence, and missing session context.
- Check unreadable/malformed logs and unsafe paths are reported as coverage limitations rather than mistaken for no data; no fabricated citations or unsupported new correctness judgments.
- Check exactly one session line per affected subject despite multiple findings, none for merely scanned subjects or no findings, local dates, prior log preservation, and partial/uncertain append failures.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage and confirm the expected eleven skill files exist.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; live diagnosis, learner interaction, and cross-subject log writes cannot be exercised by repository end-to-end tests.

## Not Now
- No additional explicit story follows US-13 in SPEC.md.
- Remediation sessions, card suggestions, new mistakes, map/goal changes, persisted diagnosis reports, transcript storage, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable diagnostician reads mistake/session evidence across all subjects and reports only defensible recurring root misunderstandings, each citing specific recorded mistakes.
- No mistakes means an explicit no-mistakes result and no diagnosis; weak or incomplete evidence does not become a fabricated root misunderstanding.
- Only subjects with related findings receive exactly one appended session line; no other learner files are changed and failures are reported accurately.
- Instruction review, expected skill inventory, and existing automated checks pass; implementation stops when the explicit story backlog is exhausted.

## Completion Summary
- Added the portable diagnostician skill: all-subject mistake/session reads, learner hypothesis before explanations, and evidence-backed root misunderstandings with exact mistake citations.
- Instructions distinguish recurring misconceptions from isolated or duplicated mistakes, historical patterns from current evidence, and diagnostic hypotheses from unsupported new correctness judgments.
- No mistakes or no defensible findings produces no diagnosis or session writes; unreadable/malformed data is reported rather than silently treated as an empty store.
- Exactly one session line is appended per subject supporting reported findings, with no changes to other learner files and explicit partial-write/retry handling.
- Instruction review covered US-13 and the listed contracts, including cross-subject patterns, missing context, circular evidence, unsafe aliases/paths, local dates, and failed or uncertain appends.
- Confirmed all eleven contracted skill files exist. `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live learner diagnosis or automated agent-session end-to-end test was run; diagnosis, interaction, and cross-subject logging were reviewed as instructions.

## Next Slice Recommendation
- No explicit next story remains in `SPEC.md`. US-01 through US-13 have implementation artifacts; stop implementation unless the learner explicitly requests additional work.
