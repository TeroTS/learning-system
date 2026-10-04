# Current Slice

Status: done

## Slice Goal
- Let the learner add a confirmed card and see its id and next-day due date.

## Slice Boundary
- Learner confirms a suggested card; the agent runs `scripts/cards.py add`; stdout shows the created card with its id and due date, and the existing subject's `cards.json` gains a box-1 card, creating the file if missing.

## Stories In Scope
- `US-03 Add a card`

## Stories Completed In This Slice
- `US-03 Add a card`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contract 1 (add CLI, common options, exit codes, atomic writes) and Contract 2 (card shape, ids, ordering, initial scheduling).

## Decision Inputs
- None.

## Shared State Required Now
- An existing subject folder and a validated JSON array of uniquely identified cards; missing `cards.json` means an empty array.

## Operations / Endpoints / Surfaces In This Slice
- `python3 scripts/cards.py add <subject> --front TEXT --back TEXT [--today YYYY-MM-DD] [--subjects-dir PATH]`.
- `subjects/<subject>/cards.json`.

## Tests Required
- Test first: new file, existing cards, max-id allocation, id ordering, local-date default, explicit-date scheduling across calendar boundaries, and UTF-8 content.
- Validate subject names and folders, empty text, strict ISO dates, malformed JSON and every card field; failures preserve original bytes and emit no learner content.
- Test atomic replacement and temporary-file cleanup on filesystem failures.
- Run a real subprocess end-to-end add and verify JSON stdout, persisted state, stderr, and exit codes; verify default store resolution from outside the repository.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; Python coverage must not decrease from 100%.

## Not Now
- US-04 List due cards; US-05 grade and review; learning-role card suggestions.
- Adaptive scheduling, shared locking, HTTP APIs, and sample learner data.

## Done When
- The add CLI implements the contracted arguments and prints exactly the created card as JSON, with a new positive id, box 1, created today, and due tomorrow.
- Only existing valid subject folders are used; invalid input or data exits 1 with stderr and unchanged card storage; bad usage exits 2.
- Card storage is validated and written atomically in id order, using only the standard library and shared logging configuration.
- Automated tests, real CLI end-to-end checks, formatting, lint, and unchanged coverage pass.

## Completion Summary
- Added `scripts/cards.py add`: JSON stdout, max-id allocation, box 1, next-day due date, explicit or local date, and repository-relative default store.
- Validates subject paths, card text, strict calendar dates, JSON shape, every stored field, and unique ids before changing storage; failures preserve existing bytes and do not disclose learner content.
- Writes cards atomically in id order and cleans up temporary files on write or replacement failure.
- Tests were written first and observed failing because the CLI was missing. Real subprocess tests cover successful addition, default-store resolution from another working directory, invalid-data preservation, and usage errors.
- `make test` and `make check` passed: 26 tests, formatting, lint, and 100% statement/branch coverage (unchanged). `make coverage` and `git diff --check` also passed.

## Next Slice Recommendation
- `US-04 List due cards`. Keep US-05 Review due cards in view; defer grading and the review skill until that story.
