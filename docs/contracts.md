# Contracts

## Purpose

Defines the interfaces between the skills, `scripts/cards.py` and the learner's store under `subjects/`, so that
every skill reads and writes the same formats. Source: `SPEC.md`, with `DECISIONS.md` as fallback.

## HTTP Contract Source

- None.

## Non-HTTP Contract Inventory

### Contract 1: `scripts/cards.py` CLI

- Kind: Command-line interface.
- Producers / Owners: `scripts/cards.py`.
- Consumers: `review`, plus every skill that adds cards (`socratic-questioner`, `examiner`, `checker`, `listener`,
  `sparring-partner`, `clerk`), and tests.
- Trigger / Direction: The agent runs it from the repository root. It reads and writes `subjects/<subject>/cards.json`.
- Payload / Shape:
  - Common options:
    - `<subject>`: the subject folder name. It must match `^[a-z0-9]+(-[a-z0-9]+)*$`, and `<subjects-dir>/<subject>/` must
      already exist.
    - `--today YYYY-MM-DD`: optional, defaults to the local calendar date. Used for deterministic tests.
    - `--subjects-dir PATH`: optional, defaults to `<repo-root>/subjects`.
  - `python3 scripts/cards.py add <subject> --front TEXT --back TEXT`
    - stdout: the created card as one JSON object (Contract 2).
  - `python3 scripts/cards.py due <subject>`
    - stdout: a JSON array of the due cards (`due <= today`), sorted by `due` and then `id`. `[]` if there are none.
  - `python3 scripts/cards.py grade <subject> <id> --result right|wrong`
    - stdout: the updated card as one JSON object.
  - Exit codes: `0` success. `1` validation or data error (message on stderr). `2` bad usage (argparse).
- Ordering / Idempotency expectations:
  - `add` is not idempotent: each call creates a new card.
  - `due` is read-only, and its output is the same for the same file and `--today`.
  - `grade` is not idempotent: each call applies one transition.
- Visibility / Security: Local only. Logs follow `scripts/logging_setup.py` (stderr, `LOG_LEVEL`). Card text is never logged.
- Failure / Retry expectations: Each of these exits with `1` and leaves `cards.json` unchanged:
  - an invalid subject name or a subject folder that doesn't exist
  - an empty `--front` or `--back` after trimming whitespace
  - an unknown `id`
  - an invalid date
  - `cards.json` that isn't valid JSON or doesn't match Contract 2

  `cards.json` is written atomically: to a temporary file in the same folder, then replaced. A missing `cards.json`
  counts as `[]`.

### Contract 2: `cards.json` and Leitner scheduling

- Kind: File format plus scheduling rules.
- Producers / Owners: `scripts/cards.py` only.
- Consumers: `scripts/cards.py`. Skills see cards only through CLI output.
- Trigger / Direction: Written by `add` and `grade`. Read by all subcommands.
- Payload / Shape: a UTF-8 JSON array of cards:

  ```json
  [
    {
      "id": 1,
      "front": "What are the four strokes of a car engine?",
      "back": "Intake, compression, power, exhaust",
      "box": 1,
      "due": "2025-10-05",
      "created": "2025-10-04"
    }
  ]
  ```

  - `id`: a positive integer, unique within the subject. A new card's id is the highest existing id + 1, or 1 for the first card.
  - `front`, `back`: non-empty strings.
  - `box`: an integer from 1 to 5.
  - `due`, `created`: ISO `YYYY-MM-DD` dates.
  - Intervals: box 1 → 1 day, 2 → 3, 3 → 7, 4 → 14, 5 → 30.
  - `add`: `box = 1`, `due = today + 1`, `created = today`.
  - `grade right`: `box = min(box + 1, 5)`. `grade wrong`: `box = 1`. Then `due = today + interval(box)`.
- Ordering / Idempotency expectations: Cards are kept in `id` order.
- Visibility / Security: Learner-owned data, edited by hand only at the learner's own risk.
- Failure / Retry expectations: If the file doesn't match this shape, the CLI exits with `1`. It never repairs the file silently.

### Contract 3: `goal.md`

- Kind: Markdown file format.
- Producers / Owners: `interviewer`.
- Consumers: `mapmaker`, `explainer`, `examiner` and the other skills, for the learner's level and context.
- Trigger / Direction: Created or updated at the end of an `interviewer` session.
- Payload / Shape:

  ```md
  # <Subject title>

  ## Goal
  <specific target outcome>

  ## Level
  <assessed current level>

  ## Deadline
  <YYYY-MM-DD or "None">

  ## Test Format
  <how the learner will be tested>
  ```
- Ordering / Idempotency expectations: Exactly one `goal.md` per subject. Updates replace the sections in place.
- Visibility / Security: Learner-owned.
- Failure / Retry expectations: Skills treat a missing `goal.md` as "level unknown" and ask the learner.

### Contract 4: `map.md`

- Kind: Markdown file format.
- Producers / Owners: `mapmaker` writes it. `examiner` changes only the status of the examined topic.
- Consumers: `examiner`, `socratic-questioner`, `explainer`, `diagnostician`.
- Trigger / Direction: Written when the learner accepts a map. The status is updated after an exam.
- Payload / Shape: topics in dependency order, one line each:

  ```md
  # <Subject title> Map

  - [todo] averages
  - [todo] spread | depends on: averages | sticking points: variance vs standard deviation
  - [learning] probability | depends on: averages
  ```

  - Line pattern: `- [<status>] <topic> [| depends on: <topic>, ...] [| sticking points: <text>]`.
  - `<status>`: `todo`, `learning` or `passed`.
  - `<topic>`: a lowercase, hyphenated (kebab-case) name, unique within the map.
- Ordering / Idempotency expectations: Each topic appears after the topics it depends on.
- Visibility / Security: Learner-owned.
- Failure / Retry expectations: If the topic being examined isn't in the map, `examiner` reports this and doesn't change the map.

### Contract 5: `mistakes.md`

- Kind: Append-only Markdown log.
- Producers / Owners: `socratic-questioner`, `examiner`, `checker`, `listener`, `sparring-partner`, `review`.
- Consumers: `diagnostician`, and skills that suggest cards.
- Trigger / Direction: Appended when a mistake is caught during a session.
- Payload / Shape: one line per mistake, created with a `# Mistakes` heading if missing:

  ```md
  - 2025-10-04 | examiner | confused variance with standard deviation | standard deviation is the square root of variance
  ```

  - Line pattern: `- <YYYY-MM-DD> | <skill> | <mistake> | <correct idea>`. A literal `|` inside a field is written as `/`.
- Ordering / Idempotency expectations: Append only, in chronological order. Existing lines are never edited.
- Visibility / Security: Learner-owned. Never logged by scripts.
- Failure / Retry expectations: A missing file is created on the first append.

### Contract 6: `sessions.md`

- Kind: Append-only Markdown log.
- Producers / Owners: every skill.
- Consumers: `diagnostician`, and the learner.
- Trigger / Direction: Exactly one line is appended at the end of each session. `diagnostician` appends to each subject it reports on.
- Payload / Shape: created with a `# Sessions` heading if missing:

  ```md
  - 2025-10-04 | examiner | spread | level 3 of 5; failed on standard error
  ```

  - Line pattern: `- <YYYY-MM-DD> | <skill> | <topic or "-"> | <result or score>`. A literal `|` inside a field is written as `/`.
- Ordering / Idempotency expectations: Append only, in chronological order.
- Visibility / Security: Learner-owned.
- Failure / Retry expectations: A missing file is created on the first append.

### Contract 7: `sources/`

- Kind: A folder of learner-supplied files.
- Producers / Owners: the learner.
- Consumers: `listener` and `checker` (grading). Other skills may read it for context.
- Trigger / Direction: Read-only for skills.
- Payload / Shape: any text-readable files in `subjects/<subject>/sources/`.
- Ordering / Idempotency expectations: None.
- Visibility / Security: Skills never change or add to sources.
- Failure / Retry expectations: If the folder is missing or empty, the skill says there is no source and does not grade.

### Contract 8: Skill file

- Kind: Agent Skills format.
- Producers / Owners: the repository.
- Consumers: any coding agent that supports skills.
- Trigger / Direction: The agent finds skills at `.agents/skills/<skill>/SKILL.md`.
- Payload / Shape: YAML frontmatter with `name` (equal to the folder name) and `description` (when to use it), followed by
  Markdown instructions. The 11 names are: `interviewer`, `mapmaker`, `explainer`, `socratic-questioner`, `examiner`,
  `checker`, `listener`, `diagnostician`, `sparring-partner`, `clerk`, `review`.
- Ordering / Idempotency expectations: None.
- Visibility / Security: No tools, syntax or instructions specific to one agent. Only file reads and writes and shell commands.
- Failure / Retry expectations: Not applicable.

## Slice Handoff

- Contract artifacts implementers must read:
  - `docs/contracts.md`
