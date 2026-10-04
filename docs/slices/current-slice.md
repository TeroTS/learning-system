# Current Slice

Status: done

## Slice Goal
- Let the learner see all due cards in a deterministic order without changing subject data.

## Slice Boundary
- The agent runs `scripts/cards.py due` for the learner's subject; the script selects every card due on or before today and prints a JSON array on stdout, with no authoritative state transition.

## Stories In Scope
- `US-04 List due cards`

## Stories Completed In This Slice
- `US-04 List due cards`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contract 1 (due CLI, common options, exit codes, due/id ordering, read-only behavior) and Contract 2 (validated card shape).

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject folder and validated card storage from US-03; missing `cards.json` means an empty array.

## Operations / Endpoints / Surfaces In This Slice
- `python3 scripts/cards.py due <subject> [--today YYYY-MM-DD] [--subjects-dir PATH]`.
- Read-only access to `subjects/<subject>/cards.json`.

## Tests Required
- Test first: overdue, due-today and future cards; deterministic due/id ordering; empty or missing storage; local-date default and strict explicit dates.
- Validate subject paths and all stored cards, even future cards; errors return 1 with stderr, no learner content, and unchanged data.
- Real subprocess end-to-end tests demonstrate listing due cards twice with identical output and unchanged storage, and missing-file and invalid-data behavior.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.

## Not Now
- US-05 grading, review skill, mistakes and session writes.
- Other learning roles, new scheduling rules, concurrency controls, and sample learner data.

## Done When
- The due CLI prints exactly a JSON array of cards with `due <= today`, sorted by due date then numeric id.
- Missing storage prints `[]` without creating a file; invalid input or stored data fails without modifying files.
- Existing add behavior is preserved, shared validation is reused, and real end-to-end tests and unchanged coverage pass.

## Completion Summary
- Added `scripts/cards.py due`: JSON-array stdout for all cards due on or before the explicit or local date, sorted by due date then numeric id.
- Missing storage returns `[]` without creating files; listing and validation failures preserve existing card bytes.
- Shared subject-path and card-data validation protects both add and due; invalid future cards are rejected rather than silently skipped.
- End-to-end tests were observed failing because the due command was missing, then passed with the implementation. Real subprocess checks cover deterministic listing, read-only storage, missing files, invalid data, and usage errors.
- `make test` and `make check` passed: 36 tests, formatting, lint, and 100% statement/branch coverage (unchanged). `git diff --check` passed.

## Next Slice Recommendation
- `US-05 Review due cards`: implement grading and the review skill using the existing add/due CLI and contracted mistake/session logs.
