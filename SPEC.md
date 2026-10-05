# Product Specification

Source: `DECISIONS.md` (Draft v3)

## Summary
- An agent-agnostic learning system for one learner and many subjects. It has 11 repo-local skills in
  `.agents/skills/` (the 10 roles from `transcript.txt` plus `review`), a Markdown/JSON store in `subjects/<subject>/`,
  and a standard-library Python script, `scripts/cards.py`, that schedules Leitner-box spaced repetition. Every skill pushes the
  learner to produce answers rather than just consume explanations.

- The skill lives at `.agents/skills/<skill>/SKILL.md` with portable frontmatter (`name`, `description`), and uses only
  file reads and writes and shell commands.
- Everything is in English. Skills ask one question at a time when the role involves questioning.
- The skill prompts the learner to produce an answer before it explains anything.
- The skill writes only to the subject files listed in `DECISIONS.md`. `cards.json` is changed only through `scripts/cards.py`.
- Each session adds exactly one line to `subjects/<subject>/sessions.md`: date, skill, topic and result or score.
- Skills that catch mistakes (`socratic-questioner`, `examiner`, `checker`, `listener`, `sparring-partner`, `review`)
  add each mistake to `subjects/<subject>/mistakes.md` with the date, skill, mistake and correct idea. At the end of the session
  they suggest cards based on those mistakes and add only the ones the learner confirms, using `scripts/cards.py add`.
- The agent generates questions and always judges answers against accepted requirements and passing targets by
  agent judgement (US-14). Sources, including topic-only guides, inform scope proposals and provide context;
  they are not answer keys or prerequisites for grading. Separate answer files are not required.
- Genuine grading uncertainty stays `unverified`, not a learner mistake or failure. Missing answer files alone
  do not make an assessment unverified. Feedback and session results identify `graded: agent judgement`;
  historical evidence and its attribution are preserved.
- Resource links are given only after they have been checked with a web or browser tool. Otherwise they are
  marked as unverified.
- Dates are the learner's local calendar date in ISO `YYYY-MM-DD` format.
- Before choosing a continuation role, offering an exam or moving topics, apply `docs/contracts.md` `Progression gate`.
  Topic scope is a finite learner-approved checklist and passing target in `map.md`; goals, sources and sticking points
  cannot silently expand it. Scope amendments and progression overrides require explicit approval. Role changes require
  confirmation; readiness never changes map status.
- Evidence states are resolved, unresolved or unknown. Use requirement-specific learner production, citing the latest
  substantive applicable outcome in append order. Aided production establishes coverage, not unaided mastery; missing,
  vague or unverified evidence is unknown. Interruptions without production do not erase earlier evidence. Preserve history.

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

## User Stories

### US-14: Get assessed by agent judgement
Primary actor: Learner

Trigger: The learner submits an answer for assessment by a grading skill (`interviewer`, `mapmaker`, `explainer`,
`socratic-questioner`, `examiner`, `checker`, `listener`, `review` or `sparring-partner`).

Happy-path action: The skill assesses the learner's answer by agent judgement against the accepted requirements
and passing target.

Visible outcome: The learner receives an assessment identified as based on agent judgement, not source verification.

Authoritative state transition: The skill appends its session result with `graded: agent judgement` to `sessions.md`.

Slice boundary: Shared grading instructions, affected skills, session attribution and instruction-contract tests.
No card-scheduling changes.

Acceptance criteria:
- Agent judgement is always the grading basis, whether sources are absent, topic-only or substantive.
  No source-first branch, fallback announcement, answer-file requirement or grading-permission prompt remains.
- Sources inform scope proposals and provide context; only the accepted map fixes topic requirements and targets.
  The agent generates questions within that scope rather than requiring supplied questions or answers.
- Genuine grading uncertainty remains `unverified`, not a learner mistake or failure. Missing answer files alone
  do not make an assessment unverified.
- Grading retains normal role-specific effects: established mistakes are logged in the existing format, cards are
  suggested and added only after confirmation, review calls `grade`, and completed unaided exams can earn `passed`.
- Historical evidence and its attribution are not rewritten. `clerk` still uses only the learner's own content;
  `diagnostician` still bases findings on stored evidence, not invented learner mistakes.
- A focused instruction-contract check covers the universal grading rule and its uncertainty and attribution safeguards;
  it does not claim to establish the correctness of every agent assessment.

Deferred follow-ups:
- None.

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

Authoritative state transition: `subjects/<subject>/map.md` is written. Initial creation and full replacement set
included topics to `todo`; approved scope amendments preserve unaffected statuses and disclose affected resets.

Slice boundary: `mapmaker` skill, `map.md`, `sessions.md` line.

Acceptance criteria:
- `map.md` lists the main parts of the subject, dependencies and sticking points. Each topic has a status, a finite
  learner-approved requirement checklist with observable success criteria, and a passing target, per Contract 4.
- Require approval before writing scope; unchanged criteria retain IDs, materially changed criteria get new IDs.
- Scope-only amendments preserve unaffected statuses and history. Changing a passed topic's target requires a disclosed,
  approved reset of that topic to `todo`; full map replacement retains the disclosed reset of included topics.
- Legacy maps without accepted requirements and targets need scope approval before readiness can be claimed.
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
- The session result names concepts, accepted requirement IDs when available, coverage states (resolved, unresolved or
  unknown), aided/unaided attribution and concise production evidence per Contract 6; history is not rewritten.
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
- The session result names concepts, accepted requirement IDs when available, coverage states (resolved, unresolved or
  unknown), aided/unaided attribution and concise production evidence per Contract 6; history is not rewritten.
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
- Before proposing or starting an exam, independently apply `docs/contracts.md` `Progression gate`, using the accepted
  requirement checklist, passing target and cited production evidence. Do not infer extra requirements at runtime.
- Missing accepted scope blocks the exam; unmet dependencies block normal progression; unknown or unresolved requirements
  require continued learning. All requirements resolved permits an exam offer, not a pass or automatic topic advancement.
- Use the accepted passing target to build the finite difficulty ladder. Questions may vary but requirements and passing
  criteria cannot change during the exam. Completing the entire accepted target unaided earns `passed`.
- Scored exam tasks use fresh applications of accepted concepts, not learning examples or previous exam solutions.
  Changing only identifiers or values is insufficient; vary the reasoning task and context/data within accepted scope.
  Standard syntax may recur. Compare tasks with available conversation and session summaries before presenting them.
- If task history is insufficient, choose new scenarios and report freshness unverified. A duplicate discovered during
  an exam is withdrawn unscored and replaced at the same level before feedback; it is not a learner failure.
  Repeated examples do not count as transfer evidence. Log short task context without full questions or solutions.
- Learning follow-ups and required explainer redos may reuse the original task; exam handoffs preserve concept evidence,
  not a pre-solved question. Do not retroactively rewrite historical grades when updating these instructions.
- After a pass, offer the first unpassed, dependency-ready topic in map order; all topics passed with valid accepted
  scope and resolved coverage means map completion. Requested re-exams use the same accepted target and gate.
  Explicit skips never mark topics passed or satisfy dependencies and require disclosed, confirmed overrides.
- An early diagnostic exam requires an accepted passing target, an explicit learner request and informed confirmation
  after disclosing gaps and the normal map-status effects. A bare `ok` to a premature offer is insufficient. Do not shrink the target to
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

Happy-path action: The listener grades the learner's explanation by agent judgement against accepted requirements.

Visible outcome: The learner sees what they missed or got wrong, for each format.

Authoritative state transition: Missed points are added to `mistakes.md`, and one line with the grade is added to `sessions.md`.

Slice boundary: `listener` skill, `mistakes.md`, `sessions.md`, card suggestions and instruction-contract tests.

Acceptance criteria:
- For each supplied format, feedback identifies omissions and mistakes by agent judgement (US-14).
- Genuine grading uncertainty remains `unverified` and is not logged as a learner mistake.
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

Happy-path action: The clerk organises the learner's notes into the requested outline or proposed-card format.

Visible outcome: The learner sees their own content organised in the requested format.

Authoritative state transition: One line is added to `sessions.md`. Saving confirmed cards is handled by US-03.

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

### US-15: Resume learning with fixed progression
Primary actor: Learner

Trigger: The learner asks to continue a subject, select another topic, or move on.

Happy-path action: Before choosing a role, the agent reads accepted scope and cited production evidence and applies
`docs/contracts.md` `Progression gate` in its specified order.

Visible outcome: The learner sees the next required action and the evidence supporting it, not an improvised scope.

Authoritative state transition: None from routing. Scope amendments require mapmaker approval; exam results retain
US-08 status rules. Role handoffs and disclosed progression overrides require confirmation.

Slice boundary: `AGENTS.md`, the shared progression contract, affected skills and instruction-contract tests.

Acceptance criteria:
- Explicit topic selection is respected but cannot silently bypass unmet dependencies or missing accepted scope.
- Missing accepted scope offers mapmaker approval; unknown/unresolved evidence offers the first gap in checklist order.
- Complete coverage offers an exam, not a pass; passing offers the first unpassed, dependency-ready topic in map order.
- No selection means the first unpassed topic in map order; all topics passed requires valid scope and coverage before
  reporting completion. A requested re-exam uses the same accepted target and readiness rules.
- Same accepted map and evidence imply the same prescribed action. Question wording and grading may involve judgement.
- Skips, dependency overrides and diagnostics follow the disclosed confirmation rules and do not invent passes.
- Repository maintenance does not create learning-session entries or approve scope for the learner.

Deferred follow-ups:
- An executable progression engine or live agent-evaluation runner; instruction checks do not prove agent compliance.

## Open Questions
- None.
