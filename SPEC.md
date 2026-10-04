# Product Specification

Source: `DECISIONS.md`

## Summary
- An agent-agnostic learning system for one learner and many subjects. It has 11 repo-local skills in
  `.agents/skills/` (the 10 roles from `transcript.txt` plus `review`), a Markdown/JSON store in `subjects/<subject>/`,
  and a standard-library Python script, `scripts/cards.py`, that schedules Leitner-box spaced repetition. Every skill pushes the
  learner to produce answers rather than just consume explanations.

## Goals
- Each of the 10 transcript roles is available as one repo-local skill, plus a `review` skill.
- Skills push the learner to produce answers. They do not just hand answers over.
- Mistakes are captured automatically and can be turned into cards once the learner confirms.
- The diagnostician finds root misunderstandings across all subjects from stored data.
- Card scheduling gives the same result every time and is covered by automated tests (coverage of at least 80%).

## Non-Goals
- Supporting several learners.
- A standalone app, web UI or direct LLM API integration.
- Agent-built practice apps.
- SM-2 or adaptive scheduling, and Anki export.
- Saving full conversation transcripts.
- CI.
- Automated behavioral evaluation of skills through LLM APIs. Focused instruction-contract checks are allowed.
- Global skill installation.
- Features specific to one agent.

## Rules That Apply to Every Skill
- The skill lives at `.agents/skills/<skill>/SKILL.md` with portable frontmatter (`name`, `description`), and uses only
  file reads and writes and shell commands.
- Everything is in English. Skills ask one question at a time when the role involves questioning.
- The skill prompts the learner to produce an answer before it explains anything.
- The skill writes only to the subject files listed in `DECISIONS.md`. `cards.json` is changed only through `scripts/cards.py`.
- Each session adds exactly one line to `subjects/<subject>/sessions.md`: date, skill, topic and result or score.
- Skills that catch mistakes (`socratic-questioner`, `examiner`, `checker`, `listener`, `sparring-partner`, `review`)
  add each mistake to `subjects/<subject>/mistakes.md` with the date, skill, mistake and correct idea. At the end of the session
  they suggest cards based on those mistakes and add only the ones the learner confirms, using `scripts/cards.py add`.
- Grading uses applicable files in `subjects/<subject>/sources/` whenever they exist, and sources always take precedence.
  If no source applies (folder missing or empty, or no source covers the topic or card), the skill grades by agent
  judgement as described in US-14. Gaps or conflicts within an applicable source stay marked `unverified`.
- Resource links are given only after they have been checked with a web or browser tool. Otherwise they are
  marked as unverified.
- Dates are the learner's local calendar date in ISO `YYYY-MM-DD` format.

## User Stories

### US-01: Start a subject with the interviewer
Primary actor: Learner

Trigger: The learner runs `interviewer` for a new subject.

Happy-path action: The learner answers questions about goal, current level, deadline and test format, asked one at a time.

Visible outcome: The learner sees a summary of the goal and their assessed level.

Authoritative state transition: `subjects/<subject>/goal.md` is created. Its folder is created if it does not already exist.

Slice boundary: `interviewer` skill, `goal.md`, `sessions.md` line.

Acceptance criteria:
- A new subject gets a lowercase, hyphenated (kebab-case) folder and a `goal.md` with the goal, level, deadline and test format.
- Vague answers get a follow-up asking for specifics before `goal.md` is written.
- Questions go from easy to hard to place the learner's level.
- If the subject already exists, `goal.md` is updated, not duplicated.
- One line is added to `sessions.md`.

Deferred follow-ups:
- None.

### US-02: Map a subject
Primary actor: Learner

Trigger: The learner runs `mapmaker` for a subject.

Happy-path action: The learner reviews and accepts the proposed map.

Visible outcome: The learner sees the topics in dependency order, with the usual sticking points marked.

Authoritative state transition: `subjects/<subject>/map.md` is written, with every topic set to `todo`.

Slice boundary: `mapmaker` skill, `map.md`, `sessions.md` line.

Acceptance criteria:
- `map.md` lists the main parts of the subject, how the topics depend on each other and where learners usually get stuck. Each topic has a status.
- The map is fitted to `goal.md` when it exists, and topics the learner already knows are skipped.
- Resource links follow the link-checking rule.
- One line is added to `sessions.md`.

Deferred follow-ups:
- None.

### US-03: Add a card
Primary actor: Learner

Trigger: The learner confirms a suggested card. The agent runs `python3 scripts/cards.py add`.

Happy-path action: A card with a front and back is added to the subject.

Visible outcome: The command prints the new card's id and due date.

Authoritative state transition: A card with `box` 1, `due` = today + 1 day and `created` = today is added to `subjects/<subject>/cards.json`,
which is created if missing.

Slice boundary: `scripts/cards.py add`, `cards.json`, `unittest` tests.

Acceptance criteria:
- The card stores `id`, `front`, `back`, `box`, `due` and `created`.
- An empty front or back, an unknown subject folder or an invalid `cards.json` stops the command with a non-zero exit and a
  message on stderr, and `cards.json` is left unchanged.
- Today's date can be supplied so tests are deterministic.

Deferred follow-ups:
- None.

### US-04: List due cards
Primary actor: Learner

Trigger: The agent runs `python3 scripts/cards.py due` for a subject.

Happy-path action: The script selects every card whose due date is on or before today.

Visible outcome: The due cards are printed on stdout.

Authoritative state transition: None (read-only).

Slice boundary: `scripts/cards.py due`, `unittest` tests.

Acceptance criteria:
- Only cards due on or before today are listed, and the output is the same every time for the same input and date.
- A missing `cards.json` lists no cards. An invalid file stops the command with a non-zero exit.

Deferred follow-ups:
- None.

### US-05: Review due cards
Primary actor: Learner

Trigger: The learner runs `review` for a subject.

Happy-path action: For each due card, the learner answers the front from memory before seeing the back.

Visible outcome: The learner sees whether each answer was right and the card's next due date.

Authoritative state transition: `scripts/cards.py grade` moves the card up one box (capped at box 5) if right, or back to box 1 if wrong,
and sets `due` = grading date + the interval for the card's new box (1, 3, 7, 14 or 30 days).

Slice boundary: `review` skill, `scripts/cards.py grade`, `mistakes.md`, `sessions.md`, `unittest` tests.

Acceptance criteria:
- The back of the card is never shown before the learner answers.
- Box changes and due dates match the Leitner rules exactly, including a correct answer in box 5.
- An unknown card id stops the command with a non-zero exit and leaves `cards.json` unchanged.
- Wrong answers are added to `mistakes.md`. One line is added to `sessions.md`.

Deferred follow-ups:
- None.

### US-06: Get unstuck with the explainer
Primary actor: Learner

Trigger: The learner runs `explainer` and names the task and the step they are stuck on.

Happy-path action: The learner gets an explanation of only that step, then redoes the task from the start without help.

Visible outcome: The learner shows a complete, unaided redo of the task.

Authoritative state transition: One line is added to `sessions.md` recording whether the redo succeeded without help.

Slice boundary: `explainer` skill, `sessions.md` line.

Acceptance criteria:
- The explanation covers only the stuck step, at the level recorded in `goal.md` or stated by the learner.
- The skill requires the redo from the start and does not count the session as complete until the redo is attempted.
- The session result names the specific concepts attempted and their outcomes (unaided, aided, unresolved or
  incomplete); historical lines are not rewritten.
- A successful redo does not automatically trigger a whole-topic exam offer. Apply the exam-readiness rule in US-08
  before offering a handoff, and wait for explicit confirmation before switching roles.

Deferred follow-ups:
- None.

### US-07: Find gaps with the Socratic questioner
Primary actor: Learner

Trigger: The learner runs `socratic-questioner` on a topic.

Happy-path action: The learner answers questions, asked one at a time, until they find the gap themselves.

Visible outcome: The learner states the gap they found in their own words.

Authoritative state transition: The gaps are added to `mistakes.md`, and one line is added to `sessions.md`.

Slice boundary: `socratic-questioner` skill, `mistakes.md`, `sessions.md`, card suggestions.

Acceptance criteria:
- The skill never gives the answer directly. It responds with follow-up questions.
- The session result names the specific concepts attempted and their outcomes (unaided, aided, unresolved or
  incomplete); historical lines are not rewritten.
- A demonstrated correction does not automatically trigger a whole-topic exam offer. Apply the exam-readiness rule
  in US-08 before offering a handoff, and wait for explicit confirmation before switching roles.
- Card suggestions follow the shared rule.

Deferred follow-ups:
- None.

### US-08: Get examined on a topic
Primary actor: Learner

Trigger: The learner runs `examiner` on a topic.

Happy-path action: The learner answers questions that get harder, one at a time, until they fail.

Visible outcome: The learner sees their level and the point where they failed.

Authoritative state transition: The topic's status in `map.md` is updated (`learning` or `passed`), and mistakes and a session line with the score are added.

Slice boundary: `examiner` skill, `map.md`, `mistakes.md`, `sessions.md`, card suggestions.

Acceptance criteria:
- Before proposing or starting an exam, compare the selected topic's sticking points in `map.md` with concrete
  learner production in `sessions.md` and the current conversation. Sticking points are a minimum checklist,
  not an exhaustive topic specification; establish the goal-relevant scope using the goal and applicable sources.
- Coverage requires concrete learner production with a resolved outcome. Aided production establishes coverage,
  not unaided mastery. Passive exposure, self-report, missing or vague evidence, and unresolved attempts do not
  establish readiness. One correction or redo is not evidence of whole-topic readiness.
- The examiner independently checks readiness before the first question. If coverage is incomplete or unknown,
  name the gaps and offer continued learning without silently switching roles or changing map status.
- An early diagnostic exam requires an explicit learner request and informed confirmation after disclosing gaps
  and the normal map-status effects. A bare `ok` to a premature offer is insufficient. Do not shrink the target to
  covered concepts; diagnostic exams keep the normal grading and status rules.
- Each question is harder than the last, and the exam stops at the first clear failure or guess.
- Only the examined topic's status changes in `map.md`; interrupted or unstarted exams leave it unchanged.
- Card suggestions follow the shared rule.

Deferred follow-ups:
- None.

### US-09: Check work with the checker
Primary actor: Learner

Trigger: The learner runs `checker` and provides their work (summary, proof, code or solution).

Happy-path action: The checker reviews each intermediate step against a rubric.

Visible outcome: The learner sees each error or missing step and any shorter path.

Authoritative state transition: Errors are added to `mistakes.md`, and one line is added to `sessions.md`.

Slice boundary: `checker` skill, `mistakes.md`, `sessions.md`, card suggestions.

Acceptance criteria:
- The learner's work is never rewritten. Findings point to specific steps.
- Card suggestions follow the shared rule.

Deferred follow-ups:
- None.

### US-10: Explain back to the listener
Primary actor: Learner

Trigger: The learner runs `listener` and gives their explanation (transcribed speech, writing and/or a drawing description).

Happy-path action: The listener grades each explanation against the subject's sources.

Visible outcome: The learner sees what they missed or got wrong, for each format.

Authoritative state transition: Missed points are added to `mistakes.md`, and one line with the grade is added to `sessions.md`.

Slice boundary: `listener` skill, `sources/`, `mistakes.md`, `sessions.md`, card suggestions.

Acceptance criteria:
- Grading uses `sources/` when an applicable source exists. Otherwise it falls back to agent judgement (US-14).
- Card suggestions follow the shared rule.

Deferred follow-ups:
- None.

### US-11: Spar in a timed simulation
Primary actor: Learner

Trigger: The learner runs `sparring-partner` with a scenario (interview, sales call or speaking), a difficulty and a time limit per answer.

Happy-path action: The learner answers a tough simulated counterpart, one prompt at a time.

Visible outcome: The learner gets pushback during the session and a score at the end.

Authoritative state transition: Weak answers are added to `mistakes.md`, and one line with the score is added to `sessions.md`.

Slice boundary: `sparring-partner` skill, `mistakes.md`, `sessions.md`, card suggestions.

Acceptance criteria:
- Vague answers get pushback, and the difficulty and time limit are applied as given.
- Card suggestions follow the shared rule.

Deferred follow-ups:
- None.

### US-12: Organise notes with the clerk
Primary actor: Learner

Trigger: The learner runs `clerk` with messy notes.

Happy-path action: The clerk turns the notes into a clean outline, or into proposed cards.

Visible outcome: The learner sees the outline or the proposed cards.

Authoritative state transition: One line is added to `sessions.md`. Proposed cards are added through `scripts/cards.py add` only after the learner confirms.

Slice boundary: `clerk` skill, `sessions.md`, `scripts/cards.py add`.

Acceptance criteria:
- The output contains only the learner's own content. Nothing is added.

Deferred follow-ups:
- None.

### US-13: Diagnose recurring mistakes
Primary actor: Learner

Trigger: The learner runs `diagnostician`.

Happy-path action: The diagnostician reads `mistakes.md` and `sessions.md` across all subjects.

Visible outcome: The learner sees the root misunderstandings, each with the mistakes that show it.

Authoritative state transition: One line is added to `sessions.md` of each subject that has related findings.

Slice boundary: `diagnostician` skill, all `subjects/*/mistakes.md` and `subjects/*/sessions.md`.

Acceptance criteria:
- Every root misunderstanding cites the specific mistakes behind it, which may come from different subjects.
- If there are no mistakes, the skill says so and diagnoses nothing.

Deferred follow-ups:
- None.

### US-14: Get graded without a source
Primary actor: Learner

Trigger: The learner runs a grading skill (`interviewer`, `mapmaker`, `explainer`, `socratic-questioner`, `examiner`,
`checker`, `listener`, `review` or `sparring-partner`) on a topic or card that no file in `subjects/<subject>/sources/` covers.

Happy-path action: The skill announces "no applicable source; grading by agent judgement" without asking the learner,
then grades the learner's answers by agent judgement.

Visible outcome: The learner sees grades and feedback marked as based on agent judgement.

Authoritative state transition: One line is added to `sessions.md` that records `graded: agent judgement` instead of
`not graded: no source`.

Slice boundary: The source rules in the affected `SKILL.md` files, plus `sessions.md`. No script changes.

Acceptance criteria:
- The fallback applies only when `sources/` is missing or empty, or no source covers the topic or card. An applicable
  source is always used instead of judgement.
- Gaps or conflicts within an applicable source stay marked `unverified` and are not filled by judgement.
- Judgement-based grades have the same effects as source-based grades: mistakes are logged to `mistakes.md` in the
  existing format (no basis tag), cards are suggested, `review` calls `scripts/cards.py grade`, and `examiner` updates
  `map.md` statuses, including `passed`.
- `clerk` is unchanged and never adds content from judgement.

Deferred follow-ups:
- None.

## Open Questions
- None. Card ids, CLI arguments and output, and where the diagnostician's session line goes are settled in `docs/contracts.md`.
