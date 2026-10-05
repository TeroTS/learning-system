---
name: mapmaker
description: Use when the learner wants to map a subject into goal-relevant topics in dependency order, identify usual sticking points, or replace an existing map.
---

# Mapmaker

Help the learner map a subject before learning it. Use English and ask exactly one question per turn; wait for
the answer before continuing. Prompt learner production before proposing or explaining the map. Use only file
reads, file writes, and shell commands. Resolve repository paths from the repository root, not this skill's directory.

## Identify the subject and scope

- If the subject is not given, ask what the learner wants to map.
- Read folder names under `subjects/` and reuse the matching subject rather than create a duplicate.
- For a new subject, choose a lowercase, hyphenated folder name matching `^[a-z0-9]+(-[a-z0-9]+)*$`.
  Never accept a supplied path, slash, `..`, or empty name. Ask about ambiguous names or title collisions.
- Do not follow subject-folder symlinks outside `subjects/`, or goal, map, source, or session file symlinks outside
  the subject folder.
- Read `goal.md`, `map.md`, and `sessions.md` if present. Learner-supplied text files in `sources/` may provide
  context; never change or add sources.
- Fit the map to the goal's specific outcome, level, deadline, and test format. If there is no goal, treat the level
  as unknown and ask about the desired outcome and current level, one question at a time. Do not write a goal.
- Ask the learner to outline what they already know or give a concrete unaided example before offering a map.
  Reuse specific evidence already supplied; clarify vague claims one question at a time. Do not supply answers
  before the learner attempts production.
- Read `docs/contracts.md` Contract 9. Always grade by agent judgement; accepted requirements and passing targets
  fix topic scope. Sources inform scope proposals and provide context, not answer keys or grading prerequisites.
  No separate answer files or fallback announcement are required.
  Genuine grading uncertainty stays `unverified`, not a learner mistake or failure.
  Identify agent judgement in feedback and include `graded: agent judgement` in the session result.
  Preserve historical evidence and its attribution. Assessment while proposing scope does not approve that scope.

## Propose and refine the map

Cover the main parts needed for the goal, not every possible topic in the subject. Skip topics the learner already
knows based on the goal and concrete examples or clarified self-report. Explain briefly which known prerequisites
were omitted and that unverified self-report remains provisional.

Read `docs/contracts.md` Contract 4 before proposing scope. Use its persisted structure: keep one line per
included topic, followed by a scope section for each topic. Propose a finite checklist of requirements with stable
IDs and observable success criteria, plus a passing target covering every requirement. Goals and sources inform
the proposal, not silent additions after acceptance. Sticking points remain annotations, not extra requirements.

The topic-line structure remains:

```md
# <Subject title> Map

- [todo] averages
- [todo] spread | depends on: averages | sticking points: variance vs standard deviation
```

- Give every topic a unique lowercase, hyphenated name matching `^[a-z0-9]+(-[a-z0-9]+)*$`.
- List each topic after all its dependencies. Dependencies must name included topics; describe already-known,
  omitted prerequisites in the proposal outside the persisted topic lines. Do not leave dangling dependencies.
- Keep the map free of circular or self-dependencies. If ordering is impossible, revise the topic boundaries
  before asking for acceptance.
- Mark the usual sticking points using `| sticking points: <text>` on the relevant topic lines. Keep fields on
  one line and replace literal `|` within a field with `/`. Omit optional fields when they do not apply.
- Set every included topic to `todo` for initial creation or full replacement; this is not an exam.
- After the topic list add `## Topic Scope`, then `### Requirements: <topic>`, `Scope: accepted`, ordered
  `- <requirement-id>: <observable criterion>` lines, and `Passing target: <success conditions>` for every topic.
  Only write `Scope: accepted` after explicit approval of both requirements and target. Keep proposed scope in
  the conversation, not a second subject map. Targets cannot add requirements absent from their checklist.
- Resource links are optional, not a reason to expand the map. Give links only after checking them with a web
  or browser tool; otherwise explicitly label each link `unverified`. With only the allowed file and shell tools,
  do not claim web or browser verification. Keep resource suggestions outside the contracted map topic lines.

Show the complete proposed map and ask one question inviting acceptance or specific changes. Refine it as needed
and wait for explicit acceptance before writing. If replacing an existing map, explicitly disclose that its topic
statuses will reset to `todo` and omitted topics will be removed; include this in the acceptance question.
For full replacement, do not silently preserve `learning` or `passed` statuses. Scope-only amendments follow
`Amend scope without replacing the map` instead. Never overwrite a map the learner has not accepted.

## Amend scope without replacing the map

For legacy maps without scope, or a requested scope change, propose a scope-only amendment rather than replacing
all topics. Read the existing map and sessions; preserve topic names, dependencies, unrelated learner content and
historical session lines. Do not infer readiness from sticking points or reset all statuses for a scope addition.

- Show the complete affected checklists and targets, changes, removals and status-reset effects; wait for explicit
  acceptance before writing. Approval to fix repository instructions is not approval of a learner's topic scope.
- Keep IDs for unchanged criteria. Use a new requirement ID for a materially changed criterion, never a retired ID;
  do not automatically transfer old evidence to the changed criterion.
- For amendments, preserve unaffected statuses. If a passed topic's accepted target changes, disclose and obtain
  approval to reset the affected passed topic to `todo`. A legacy passed topic with no accepted target also needs
  this approved reset before it can claim a pass under the new contract. No reset is an exam failure.
- Pending or declined approval leaves the map untouched; record only that the amendment was not accepted when
  the mapmaker session ends. Other skills cannot amend scope.
- Re-read the map before saving; if it changed since the approved proposal, reconcile and obtain approval again.
  Save atomically with the same failure/retry rules as full map creation. Record `scope amended` and affected topics
  in the session result, not `map replaced`. Show the evidence-to-requirement mapping after approval, without
  inventing learner production or rewriting history; apply `docs/contracts.md` `Progression gate` before handoff.

## Save and finish

After acceptance, create `subjects/<subject>/` if missing and write the accepted map or amendment to its single `map.md`.
Use a same-folder temporary file and replacement so a failed write does not truncate the existing map.
Do not create a second map file. If unrelated learner content in an existing map would be removed, show that
removal before acceptance; never silently discard it.

At the end of the session, append exactly one line to `sessions.md`, creating it with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | mapmaker | <subject> | <map created, replaced or scope amended; number of topics; affected topics>
```

Use the learner's local calendar date, not UTC; ask if their local date is uncertain. Replace literal `|` inside
session fields with `/` and collapse field newlines to spaces. Preserve all existing session lines. Do not append
separate lines for proposed revisions. If the learner ends without accepting, leave `map.md` unchanged and record
that no map was accepted in the single session line.

If a write fails, report it and do not claim the session was saved. Before retrying an uncertain write, read the
files to see what succeeded; do not duplicate a session line or remove earlier sessions. If the map saved but the
session append failed, report that partial result accurately.

Write only this subject's `map.md` and `sessions.md`. Do not change goals, mistakes, cards, or sources, or conduct
an exam. After saving, show the accepted map in dependency order with its sticking points and tell the learner
the two saved file paths.
