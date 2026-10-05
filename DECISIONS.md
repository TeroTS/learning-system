# AI Learning System Decisions

Status: Draft v3

## Problem Summary

Most people use AI only as an explainer. That is passive consumption, and it feels like learning but does not stick.
The source (`transcript.txt`) argues that learning happens through active production: recall, prediction,
explanation and real attempts. It describes 10 AI roles and spaced repetition as ways to support that.
This repository turns those ideas into a set of repo-local, agent-agnostic skills plus a small local store, for one learner
working on many subjects.

## Goals and Success Criteria

- Each of the 10 transcript roles is available as one repo-local skill, plus a `review` skill.
- Skills push the learner to produce answers. They do not just hand answers over.
- Mistakes are captured automatically and can be turned into spaced-repetition cards.
- The diagnostician can find recurring misunderstandings across all subjects from stored data.
- Review scheduling gives the same result every time and is covered by automated tests (coverage of at least 80%).

## Primary Roles / Actors

- Learner: a single user who runs the skills from this repository in any coding agent that supports skills.
- Agent: any coding agent that supports skills and can read and write files and run shell commands.
  It runs a skill and reads and writes the local store.
- `scripts/cards.py`: a script that does the card scheduling with deterministic date maths.

## Non-Goals

- Supporting several learners.
- A standalone app, web UI or direct LLM API integration.
- Agent-built practice apps (deferred).
- SM-2 or adaptive scheduling, and Anki export.
- Saving full conversation transcripts.
- CI.
- Automated behavioral evaluation of skills through LLM APIs. Focused instruction-contract checks are allowed.
- Global skill installation.

## Locked Decisions

### Product / Scope

- Form: agent-agnostic skills that follow the open Agent Skills format, plus a small local store.
  No standalone app.
- Skills must not use features, tools or instructions specific to one agent. They rely only on reading and
  writing files and running shell commands.
- Skills live in the repository at `.agents/skills/<skill>/SKILL.md`, not globally.
- Version 1 has 11 skills: `interviewer`, `mapmaker`, `explainer`, `socratic-questioner`, `examiner`,
  `checker`, `listener`, `diagnostician`, `sparring-partner`, `clerk` and `review`.
- Placing questions at the learner's level is part of `interviewer` and `examiner`.
  Simulations and role play are part of `sparring-partner`.
- Practice apps are excluded from version 1.

### UX / Workflow

- All skills, stored files and sessions are in English.
- Skills ask one question at a time where the role involves questioning.
- At the end of a session, the skill suggests cards based on the session's mistakes. Cards are added only
  after the learner confirms.

### Data / State / Ownership

- One learner, several subjects. Each subject has its own folder, `subjects/<subject>/`.
- Files in each subject folder:
  - `goal.md`: goal, current level, deadline and how the learner will be tested (written by `interviewer`).
  - `map.md`: topics, dependencies, sticking points, learner-approved requirement checklists and passing targets;
    each topic has a status of `todo`, `learning` or `passed` (written by `mapmaker`; exam status updated by `examiner`).
  - `mistakes.md`: entries appended automatically. Each entry has the date, skill, mistake and correct idea.
  - `sessions.md`: one line per session with the date, skill, topic and result or score.
  - `cards.json`: flashcards. Only `scripts/cards.py` writes to this file.
  - `sources/`: source material supplied by the learner.
- Full conversation transcripts are not saved.

### Interfaces / Contracts

- `scripts/cards.py` uses Python 3.11 or newer and only the standard library. Subcommands: `add`, `due` and `grade`.
- Spaced repetition uses Leitner boxes with intervals of 1, 3, 7, 14 and 30 days. A correct answer moves the card
  up one box (the top box stays at 30 days). A wrong answer moves it back to box 1. The next due date is the
  grading date plus the interval of the card's new box.
- Skills call `scripts/cards.py` for all card operations.

### Operations / Deployment

- Everything runs locally. There is no CI.
- Tests use `unittest`. Coverage is measured with `coverage.py`, with an 80% minimum, run locally.
- `ruff` is used for both formatting and linting.
- Dev dependencies are `coverage` and `ruff` only, pinned in `requirements-dev.txt`.
- Logging uses the standard `logging` module, configured by `scripts/logging_setup.py`.
  Logs go to stderr so that stdout stays free for command output. The level is set by `LOG_LEVEL` (default `WARNING`),
  and an invalid value is an error. Secrets and learner content are never logged.

## Core Business Rules

- Learning comes from producing answers. Skills prompt the learner before explaining.
- `explainer` explains only the step the learner is stuck on, at the learner's level. It then requires
  the learner to redo the task from the start without help.
- `socratic-questioner` never gives the answer directly.
- `examiner` asks questions that get harder until the learner fails, then reports the learner's level.
- `checker` reviews the learner's process and intermediate steps against a rubric. It points out errors and
  shorter paths but does not rewrite the learner's work.
- `listener` grades the learner's spoken (transcribed), written and drawn explanations by agent judgement
  and lists what was missed.
- `diagnostician` reads `mistakes.md` and `sessions.md` across all subjects and names the root
  misunderstandings that keep coming up.
- `sparring-partner` runs a timed, tough simulation (interview, sales call, speaking). Difficulty can be
  adjusted, and a score is given at the end.
- `clerk` organises only the learner's own notes. It does not add content.
- `review` shows the front of each due card. The learner answers from memory before seeing the back.
  The agent judges the answer right or wrong and calls `grade`.
- Every skill that catches a mistake (`socratic-questioner`, `examiner`, `checker`, `listener`,
  `sparring-partner`, `review`) adds it to `mistakes.md` automatically.
- Every skill adds one line to `sessions.md` per session. `explainer` and `socratic-questioner` name the specific
  concepts attempted and their outcomes in the existing result field; historical lines are not rewritten.

## UX / Workflow Rules

- Typical flow: `interviewer` → `mapmaker` → study, with `explainer` as needed → `socratic-questioner` /
  `examiner` / `checker` / `listener` / `sparring-partner` → `review` on a schedule → `diagnostician` from time to time.
- Each topic has a finite learner-approved checklist of observable requirements and a passing target in `map.md`.
  Goals and sources inform scope proposals; the accepted map fixes requirements. They do not silently expand scope.
  Sticking points are annotations.
- Apply `docs/contracts.md` `Progression gate` before choosing a continuation role, offering an exam or moving topics.
  Missing accepted scope requires a mapmaker handoff; unmet dependencies require learning the earliest unmet dependency;
  unknown or unresolved requirements require continued learning in checklist order; complete coverage offers an exam;
  only a passed topic permits normal progression to the first unpassed, dependency-ready topic in map order.
- Coverage requires concrete learner production with a resolved outcome. Aided production establishes coverage,
  not unaided mastery. Missing, vague or unverified evidence is unknown; misconceptions without correction are unresolved.
  Use the latest substantive applicable outcome in append order and cite its session entry. Interrupted sessions without
  production do not erase earlier evidence. Legacy evidence must clearly match an accepted criterion.
- Scope changes require explicit approval through mapmaker. Unchanged criteria keep their IDs; materially changed criteria
  get new IDs. Scope amendments preserve unaffected statuses; changing a passed topic's target requires a disclosed,
  approved reset to `todo`. Full replacement keeps its existing disclosed reset rule.
- Scope and evidence use Contracts 4 and 6 in `docs/contracts.md`; no new store files or dependencies are added.
- The examiner independently applies the gate before the first question and uses only the accepted passing target.
  Readiness checks never change map status. Only an unaided completed target earns `passed`.
- Exams test transfer using fresh tasks within the same accepted requirements, not repeated learning examples or
  previous exam solutions. Renaming identifiers or swapping values alone is insufficient; vary the reasoning task
  and context/data without adding scope or difficulty beyond the target. Standard syntax may recur.
- Compare exam tasks against available conversation and concise session task summaries before scoring. If history
  is insufficient, choose a new scenario and report freshness as unverified, not proven. Store short task context
  in the existing session result field, not full questions, solutions or transcripts. Learning follow-ups and
  explainer redos may reuse the learning task; an exam handoff does not convert that redo into an exam question.
- Explicit skips and dependency overrides require disclosure and confirmation; they never mark topics passed or satisfy
  dependencies. Explicit topic selection alone is not approval to bypass the gate. Role changes require confirmation.
- An early diagnostic exam requires an accepted passing target, an explicit learner request and informed confirmation
  after disclosing gaps and the existing map-status effects (`learning` on failure, `passed` on target completion). A bare `ok` to a
  premature offer is insufficient. Diagnostic exams keep the whole-topic target and normal grading rules.
- Focused automated instruction-contract checks protect these rules; scenario review complements them but neither
  proves that every agent will follow the instructions.
- `interviewer` asks for specifics, including the goal, current level, deadline and test format, and pushes
  back on vague answers.
- `mapmaker` lists the main parts of the subject, how the topics depend on each other and where learners
  usually get stuck.

## Data / State / Ownership Decisions

- The learner owns all files under `subjects/`. Skills may write only to the files listed above.
- `cards.json` is changed only through `scripts/cards.py`.

## Interface / Contract Expectations

- Skill directory: `.agents/skills/<skill>/SKILL.md`, using portable frontmatter (`name`, `description`).
- Card CLI: `python3 scripts/cards.py add|due|grade` acting on `subjects/<subject>/cards.json`.
- The agent always generates questions and judges answers against the accepted requirements and passing targets.
  Agent judgement is the system-wide grading basis, not a fallback; source-first grading is replaced.
- Learner-supplied sources, including topic-only guides, inform scope proposals and provide context, not answer keys
  or a prerequisite for grading. Separate answer files are not required.
- Genuine grading uncertainty stays `unverified`, not a learner mistake or failure. Missing answer files do not
  by themselves make an assessment unverified.
- Feedback identifies agent judgement as the grading basis, and the `sessions.md` line records
  `graded: agent judgement`. Historical evidence and its attribution are not rewritten.
  `mistakes.md` entries keep their existing format with no basis tag.
- Agent-judgement grades have normal effects: mistakes are logged, cards are suggested subject to confirmation,
  `review` calls `grade`, and `examiner` updates map statuses (including `passed`).
- `clerk` is unchanged: it organises only the learner's own notes and never adds content from judgement.
- Resource links are suggested only when they have been checked with a web or browser tool.
  Links that were not checked are marked as unverified.

## Operational / Deployment Constraints

- The system runs locally with any coding agent that supports skills, plus Python 3.11 or newer.
- No network access is needed except for optional link checking.
- The repository must be initialised with `git init`.

## Assumptions

- The "C" answer to the testing question means: `unittest` plus `coverage.py` (80% minimum), run locally,
  with no CI.
- `interviewer` creates `subjects/<subject>/` and `goal.md` when the subject is new.
- Subject folder names are lowercase and hyphenated (kebab-case).
- Dates use the learner's local calendar date (ISO `YYYY-MM-DD`).
- Card fields: `id`, `front`, `back`, `box`, `due`, `created`.

## Open Questions

- None currently.

## Ready for Spec Generation

- Status: yes
- Reason: Scope, skills, store layout, scheduling rules, mistake and session logging, source handling,
  language and testing are decided, including system-wide agent-judgement grading. `$decision-to-spec` can proceed
  without inventing policy. SPEC.md, contracts, vocabulary and skills still need alignment with this decision.
  The remaining defaults are recorded under Assumptions.
