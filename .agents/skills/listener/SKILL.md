---
name: listener
description: Use when the learner explains a topic through transcribed speech, writing, and/or a drawing description and wants grades by agent judgement and feedback on what each format missed or got wrong.
---

# Listener

Listen to the learner's explanation before giving feedback. Grade what they produced, not an explanation you
supply. Use English and ask exactly one question per turn when clarification is needed; wait for the answer.
Use only file reads, file writes, and shell commands. Resolve repository paths from the repository root, not this
skill's directory.

## Establish the subject and explanation

- Ask which subject and topic the learner means if either is missing, one question at a time. Reuse the existing
  subject folder under `subjects/`; if it is missing, direct the learner to `interviewer` without creating a folder.
- Require a subject name matching `^[a-z0-9]+(-[a-z0-9]+)*$`; reject paths, slashes, `..`, and empty names. Ask about
  ambiguous names. Do not follow a subject-folder symlink outside `subjects/`, or goal, map, source, or log file
  symlinks outside the subject folder.
- Read `goal.md`, `map.md`, `mistakes.md`, and `sessions.md` if present. Use accepted map scope and the goal
  for feedback depth.
  Treat a missing level as unknown and ask when necessary; do not assess or rewrite the goal.
- If no explanation has been supplied, ask the learner to explain the topic in their own words before giving
  hints, a model explanation, or source excerpts. Already supplied explanations satisfy the production requirement.
- Accept any one or more of transcribed speech, writing, and a drawing description. Identify the format of each
  explanation, asking if unclear. Do not require all three or penalize an absent format.
- For audio without a transcript, ask for transcribed speech. For a drawing without a text description, ask the
  learner to describe its labels, components, and relationships. Do not add transcription or image-recognition
  tools, invent speech content, or claim to have inspected a drawing from its description alone.
- Keep explanations in the conversation or read learner-authorized text files without copying or modifying them.
  Do not save explanations, transcripts, or drawing descriptions in the subject store.

## Grade by agent judgement

Read learner-supplied text files in `subjects/<subject>/sources/` for context; never add to or change them.
Read `docs/contracts.md` Contract 9. Always grade by agent judgement; accepted requirements and passing targets
fix topic scope. Sources provide context, not answer keys or grading prerequisites. No separate answer files or
fallback announcement are required. Genuine grading uncertainty stays `unverified`, not a learner mistake or failure.
Identify agent judgement in feedback and include `graded: agent judgement` in the session result.
Preserve historical evidence and its attribution.

Use the agreed rubric when available. Otherwise, derive a concise checklist of key ideas and relationships from
accepted requirements within the agreed topic scope. Make the criteria explicit, not an arbitrary letter grade or
unexplained global scale. Apply the same relevant criteria across formats, respecting agreed format requirements.

For **each supplied explanation separately**:

- Mark each applicable criterion as correctly conveyed, missing, or incorrect. Accept accurate paraphrases and
  described relationships rather than demanding exact wording.
- Report a grade as correctly conveyed criteria out of applicable criteria, or use the agreed rubric.
  An idea stated incorrectly does not count as correctly conveyed merely because it was mentioned.
- Show the specific omissions and wrong ideas, explaining the reasoning supporting each finding by agent judgement.
  Locate wrong claims in the learner's explanation; identify where a missing relationship belonged.
- For transcribed speech, judge the available conceptual content, not unheard tone, pronunciation, or delivery.
  For a drawing description, distinguish `missing from the description` from claims about an unseen drawing.
- Ask one focused clarification for genuinely ambiguous wording or relationships, without supplying the missing
  answer. Do not silently fill in a gap and award credit for your own interpretation.
- If grading a criterion or extra claim is genuinely uncertain, mark that portion `unverified` and explain the
  limitation. Identify excluded criteria so a partial assessment cannot be mistaken for full validation.

Do not merge formats into a single score that hides their differences or let a correct written explanation erase
an incorrect spoken explanation. If nothing was missed or wrong in a supported explanation, say so without
claiming mastery beyond the checked criteria. Provide concise corrections after production, not a replacement
explanation, lesson, or mandatory exam/redo.

## Record mistakes and suggest cards

Automatically append every distinct omission or wrong idea established by agent judgement to `mistakes.md`,
creating it with `# Mistakes` if missing:

```md
- <YYYY-MM-DD> | listener | <topic, affected format(s), and concise missed or wrong idea> | <correct idea>
```

Do not ask permission to capture mistakes. Preserve earlier lines. If the same mistake occurs in multiple
formats, record it once with all affected formats while retaining separate format-specific feedback. Different
mistakes get separate lines. Do not save full explanations, count an optional unsupplied format as a mistake, or
record an unverified concern as fact. If no supported mistakes were found, do not create an empty mistake log.

At the end, suggest focused cards based on this session's recorded mistakes. Show each proposed front and back
and ask one confirmation question at a time. Add only explicitly confirmed cards:

```bash
python3 scripts/cards.py add <subject> --front '<confirmed front>' --back '<confirmed back>' --today <YYYY-MM-DD>
```

Use safely quoted arguments or a subprocess argument list, never unescaped shell interpolation. Check the exit
code and returned JSON before claiming an addition. Declined suggestions or silence create no cards. All card
access uses `scripts/cards.py`; never read or edit `cards.json` directly or change existing card grades. Do not
manufacture suggestions when there were no supported mistakes.

## Finish the session

Show the grade and key findings for each supplied format, including any unverified portions. Append exactly one
line to `sessions.md`, creating it with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | listener | <topic or -> | <per-format grades; grading limitations or incomplete session>
```

Include all supplied-format grades in that single line; for ungraded portions, say why instead of inventing a
score. Use the learner's local calendar date in ISO `YYYY-MM-DD`, asking if uncertain. Date mistakes when caught,
cards when added, and the session line at session end. Replace literal `|` inside log fields with `/` and collapse
field newlines to spaces. Preserve earlier lines; do not add session entries for individual formats or cards.
If the learner ends early, record what was actually evaluated and mark the rest incomplete, not passed.

If a write or CLI call fails, report what did and did not save and include the failure in the session result when
possible. Before retrying an uncertain log append, read the file to see whether the intended entry was written;
do not duplicate entries or remove earlier lines. Card addition is non-idempotent: stop for reconciliation after
an uncertain add rather than blindly repeating it and creating a duplicate card.

Write only this subject's `mistakes.md` and `sessions.md` directly; confirmed cards use only the CLI. Never change
goals, maps, sources, or submitted explanations, and do not suggest resource links. Finish with format-specific
results and paths of files actually changed.
