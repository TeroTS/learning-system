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
- Producers / Owners: `mapmaker` writes approved maps and scope amendments. `examiner` changes only the status of
  the examined topic. Scope amendments preserve unaffected statuses; changing a passed topic's target requires an
  explicitly approved reset of that topic to `todo`. A legacy passed topic without an accepted target also requires
  that disclosed, approved reset. Full replacement resets included statuses after disclosure.
- Consumers: `mapmaker`, `examiner`, `socratic-questioner`, `explainer`, `diagnostician` and general continuation routing.
- Trigger / Direction: Written when the learner accepts a map or scope amendment. The status is updated after an exam.
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
  - Keep topic lines compatible. After them, include exactly one `### Requirements: <topic>` scope section per topic:

    ```md
    ## Topic Scope

    ### Requirements: spread
    Scope: accepted
    - spread-compare: Explain how variance and standard deviation differ, including their units.
    - spread-calculate: Calculate both for a supplied small population and explain each step.
    Passing target: Complete both requirements unaided, including calculation and interpretation.
    ```

  - Requirements form the complete finite learner-approved scope, not a set of examples. Each ID is a unique
    kebab-case name within the subject; each criterion describes observable production and success conditions.
    List requirements in learning order. The passing target covers every requirement and names required forms of
    production and success conditions; it must not introduce unnamed extra concepts.
  - Only mapmaker writes `Scope: accepted`, after explicit approval of the checklist and target. Proposed scope
    stays outside the subject store until accepted. Empty, duplicate, malformed or unaccepted sections are unknown scope.
  - Goals and sources inform scope proposals and provide context; the accepted map fixes requirements and passing
    targets. Sources do not silently change scope or become answer-file prerequisites. Sticking points are
    annotations only. Extras cannot become blockers without approval.
  - Preserve IDs for unchanged criteria. A materially changed criterion gets a new requirement ID, never a reused
    retired ID. Changed criteria cannot automatically inherit evidence for their previous criteria. Show affected
    targets, resets and removals before approval. Preserve unaffected statuses and unrelated learner content.
  - Legacy maps remain readable, but missing accepted checklists or targets block readiness. Add sections through
    an approved scope amendment, not a destructive full replacement. Existing topic names remain unchanged.
- Ordering / Idempotency expectations: Each topic appears after the topics it depends on.
- Visibility / Security: Learner-owned.
- Failure / Retry expectations: If the topic being examined isn't in the map, `examiner` reports this and doesn't change the map.

### Contract 5: `mistakes.md`

- Kind: Append-only Markdown log.
- Producers / Owners: `socratic-questioner`, `examiner`, `checker`, `listener`, `sparring-partner`, `review`.
- Consumers: `diagnostician`, and skills that suggest cards.
- Trigger / Direction: Appended when agent judgement establishes a learner mistake during a session (Contract 9).
  Genuine grading uncertainty is not a learner mistake and is not appended here.
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
- Consumers: `diagnostician`, the learner, and `explainer`, `socratic-questioner` and `examiner` for exam readiness.
- Trigger / Direction: Exactly one line is appended at the end of each session. `diagnostician` appends to each subject it reports on.
- Payload / Shape: created with a `# Sessions` heading if missing:

  ```md
  - 2025-10-04 | examiner | spread | level 3 of 5; failed on standard error
  ```

  - Line pattern: `- <YYYY-MM-DD> | <skill> | <topic or "-"> | <result or score>`. A literal `|` inside a field is written as `/`.
  - Learning sessions name accepted requirement IDs when available, coverage state, aided/unaided attribution,
    and a concise description of concrete learner production in the existing result field, for example:
    `spread-compare: resolved, aided, explained units correctly; spread-calculate: unresolved, unaided, omitted division`.
    Use resolved, unresolved or unknown: resolved requires correct learner production matching the criterion;
    unresolved means a demonstrated misconception without correction; unknown means missing, vague, incomplete
    or unverified evidence. Mere explanation, agreement, self-report or a topic status is not coverage evidence.
  - Derive coverage from the latest substantive applicable outcome in append order, then any current-session
    production. A later demonstrated misconception supersedes earlier success. An interruption without production
    does not erase earlier evidence. A resolved outcome can include correction within the same session.
  - Cite the session path and line number (or specific current-session attempt) for each reported requirement state.
    Missing evidence is reported as `none`; aided production establishes coverage, not unaided mastery.
  - Legacy evidence counts only when its specific production and resolved outcome clearly match an accepted
    criterion. Ambiguous mappings remain unknown. Criterion changes do not automatically inherit old evidence.
  - Historical lines stay unchanged. No new fields or tracking files are required; readiness checks never write
    derived coverage or fabricate session outcomes. Log interruptions and verification limits explicitly.
  - Learning and exam results include short task context (scenario, relevant data shape and reasoning demanded)
    sufficient to compare future exam tasks with prior examples, not full questions, solutions or transcripts.
    No new field or tracking file is needed; vague legacy summaries cannot establish proven task freshness.
  - Results from grading skills identify `graded: agent judgement` in the existing result field, whether sources
    are absent, topic-only or substantive. Record genuine grading uncertainty as `unverified`, not a learner failure;
    unverified evidence remains unknown for coverage. Preserve historical evidence and its original attribution.
  - Exam results cite tested requirement IDs, outcomes, score, terminal result and task-freshness limitations.
    Exams use fresh applications of accepted requirements, not repeated learning examples or prior exam solutions;
    changing only names/values is insufficient. Unavailable history means freshness unverified, not proven novelty.
    Only completion of the whole accepted target unaided yields a pass; unasked requirements are never reported
    as demonstrated. Learning follow-ups and explainer redos may reuse the original task.
- Ordering / Idempotency expectations: Append only, in chronological order.
- Visibility / Security: Learner-owned.
- Failure / Retry expectations: A missing file is created on the first append.

### Contract 7: `sources/`

- Kind: A folder of learner-supplied files.
- Producers / Owners: the learner.
- Consumers: Skills proposing scope or reading subject context; sources are not grading authorities.
- Trigger / Direction: Read-only for skills.
- Payload / Shape: any text-readable files in `subjects/<subject>/sources/`, including topic-only guides.
  These inform scope proposals and provide context, not answer keys. The accepted map fixes requirements and targets.
- Ordering / Idempotency expectations: None.
- Visibility / Security: Skills never change or add to sources.
- Failure / Retry expectations: Missing, empty, topic-only, incomplete or conflicting sources do not create an
  answer-file requirement or a source-first grading branch. Agent judgement always supplies the grading basis
  (Contract 9); missing answer files alone do not make an assessment unverified. Genuine grading uncertainty is
  reported as `unverified`, not a learner mistake or failure.

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

### Contract 9: Agent-judgement assessment

- Kind: Shared assessment and evidence contract (US-14).
- Producers / Owners: The agent running `interviewer`, `mapmaker`, `explainer`, `socratic-questioner`, `examiner`,
  `checker`, `listener`, `review` or `sparring-partner`.
- Consumers: The learner, mistake/session logs, card review and topic progression.
- Trigger / Direction: The learner supplies production for assessment; the skill assesses it before recording outcomes.
- Payload / Shape:
  - The agent generates questions within accepted scope and judges answers against accepted requirements and passing
    targets. Agent judgement is always the grading basis, whether sources are absent, topic-only or substantive.
  - Feedback identifies agent judgement, not source verification. Session results include `graded: agent judgement`
    in the existing Contract 6 result field; no new store fields or files are introduced.
  - Established mistakes use Contract 5. Cards are suggested and added only after confirmation through Contract 1.
    Review judges recall before calling `grade`; examiner retains accepted-target and unaided-pass rules.
- Ordering / Idempotency expectations: Learner production precedes assessment and feedback. Preserve historical
  evidence and its attribution; do not retroactively relabel earlier assessments. Exactly one session line is appended
  per session under Contract 6, not one per assessed answer. Card transitions retain Contracts 1 and 2.
- Visibility / Security: No grading-permission prompt, fallback announcement or separate answer files are required.
  Clerk still organises only learner content; diagnostician cites stored evidence rather than inventing learner mistakes.
- Failure / Retry expectations: Genuine grading uncertainty remains `unverified`, not a learner mistake or failure.
  Do not record it as a wrong-card transition or a failed exam; unverified evidence cannot establish coverage or a pass.
  Missing answer files alone do not make an assessment unverified. Existing role-specific interruption and persistence
  rules remain in force. Instruction-contract tests check these rules, not the correctness of every agent judgement.

## Progression gate

This is the shared decision rule for general continuation requests and skill handoffs. Read Contracts 4 and 6
before using it; all consumers of `docs/contracts.md` apply the same order rather than inventing additional scope.

1. Validate the subject name as `^[a-z0-9]+(-[a-z0-9]+)*$`; reject paths, slashes, `..` and empty names.
   Do not follow subject-folder symlinks outside `subjects/` or goal/map/session symlinks outside the subject folder.
   Read the selected subject's goal, map and sessions. Use an explicitly selected topic if given. Otherwise choose
   the first unpassed topic in map order; this resumes the earliest unfinished topic rather than skipping it.
   If all topics are passed, validate accepted scope and coverage for every topic before reporting completion;
   the first invalid scope or unknown/unresolved requirement in map order determines the action instead.
   Missing subject or ambiguous topic selection requires clarification, not creation or guessed progress.
2. Validate accepted scope/targets, unique topic names and dependency ordering for the selected topic and its
   dependencies. Missing, duplicate, dangling or cyclic dependencies block routing and require mapmaker repair.
   A passed status without accepted scope is legacy state, not proof of completion under the new contract.
3. Derive requirement coverage using Contract 6. Report IDs, states and evidence citations, then take the first
   matching row below. Selection/coverage are read-only; a gate refusal is not an exam failure.

| State | Required next action |
| --- | --- |
| Missing, malformed or unaccepted scope/target | Offer a mapmaker scope-approval handoff; do not invent completeness or begin an exam. |
| Required dependency not passed | Offer the earliest unmet dependency in map order before the selected topic. |
| Unknown or unresolved requirement | Offer the first such requirement in accepted checklist order; cite its evidence state. |
| Every requirement resolved; topic not passed or re-exam requested | Offer the accepted topic exam; wait for confirmation, not automatic advancement. |
| Topic passed; unpassed topics remain | Offer the first unpassed, dependency-ready topic in map order, applying this gate again before starting it. |
| Every topic passed | Report map completion; do not automatically expand scope. |

- A request to re-examine an already passed topic uses the same accepted target and readiness/diagnostic rules;
  it does not automatically redirect to the next topic. Otherwise a pass offers normal progression.
- Scope changes require explicit approval through mapmaker. Readiness never writes map status or log entries on its own.
- Before bypassing an unmet dependency or choosing to skip a requirement/topic, disclose what remains incomplete and
  obtain explicit confirmation. Explicit topic selection does not itself authorize bypassing the gate.
  A skip never marks a topic passed or satisfies a dependency. An approved bypass applies only to the disclosed
  request, not future sessions; never silently shrink the exam target.
- An early diagnostic requires an explicit request, an accepted target, disclosure of coverage/dependency gaps and
  normal status effects (`learning` on failure, `passed` on completion), then informed confirmation. No accepted target
  means no diagnostic exam. A bare `ok` to a premature offer is insufficient.
- Do not silently switch roles. Wait for confirmation for a handoff; respect an explicitly requested role, but still
  apply its gate. A role request cannot be reinterpreted as a diagnostic or an override.
- Same accepted map and evidence imply the same prescribed next action. Grading and question wording may involve
  judgement; instruction-contract tests do not prove that every agent follows the rule.

## Slice Handoff

- Contract artifacts implementers must read:
  - `docs/contracts.md` (Contracts 4–9 and the Progression gate for US-14 alignment).
- Next step: `$lean-story-delivery`. List `docs/contracts.md` under `## Contract Inputs` in
  `docs/slices/current-slice.md` when slice planning starts. No HTTP surface or OpenAPI artifact is required.
