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
- Grade correctness against applicable files in `sources/`; they always take precedence. If `sources/` is missing
  or empty, or no source covers the learner's examples, announce `no applicable source; grading by agent judgement`
  without asking, grade by agent judgement, and record `graded: agent judgement` in the session line.

## Propose and refine the map

Cover the main parts needed for the goal, not every possible topic in the subject. Skip topics the learner already
knows based on the goal and concrete examples or clarified self-report. Explain briefly which known prerequisites
were omitted and that unverified self-report remains provisional.

Use this exact persisted structure, with one line per included topic:

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
- Set every included topic to `todo`; this is a new accepted map, not an exam or a status update.
- Resource links are optional, not a reason to expand the map. Give links only after checking them with a web
  or browser tool; otherwise explicitly label each link `unverified`. With only the allowed file and shell tools,
  do not claim web or browser verification. Keep resource suggestions outside the contracted map topic lines.

Show the complete proposed map and ask one question inviting acceptance or specific changes. Refine it as needed
and wait for explicit acceptance before writing. If replacing an existing map, explicitly disclose that its topic
statuses will reset to `todo` and omitted topics will be removed; include this in the acceptance question.
Do not silently preserve `learning` or `passed` statuses or overwrite a map the learner has not accepted.

## Save and finish

After acceptance, create `subjects/<subject>/` if missing and write the accepted map to its single `map.md`.
Use a same-folder temporary file and replacement so a failed write does not truncate the existing map.
Do not create a second map file. If unrelated learner content in an existing map would be removed, show that
removal before acceptance; never silently discard it.

At the end of the session, append exactly one line to `sessions.md`, creating it with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | mapmaker | <subject> | <map created or replaced; number of topics>
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
