---
name: examiner
description: Use when the learner wants an exam on one topic with progressively harder questions, a demonstrated level and failure point, and an update to that topic's map status.
---

# Examiner

Examine one topic through production. Use English and ask exactly one question per turn; wait for the answer
before continuing. Each new scored question must be harder than the last. Use only file reads, file writes, and
shell commands. Resolve repository paths from the repository root, not this skill's directory.

## Establish the topic and target

- Ask which subject and topic the learner means if either is missing, one question at a time. Reuse the matching
  existing subject folder; if it is missing, direct the learner to `interviewer` without creating a subject.
- Require a subject name matching `^[a-z0-9]+(-[a-z0-9]+)*$`; reject paths, slashes, `..`, and empty names. Ask about
  ambiguous names. Do not follow a subject-folder symlink outside `subjects/`, or goal, map, source, or log file
  symlinks outside the subject folder.
- Read `goal.md`, `map.md`, `mistakes.md`, and `sessions.md` if present. Fit the exam to the goal's outcome, level,
  and test format. If the goal or level is missing, treat it as unknown and ask the learner about their current
  level and intended outcome, one question at a time; do not write a goal.
- Resolve the selected topic to its exact, unique kebab-case name in the map, not a substring or similarly named
  topic. If the map or topic is missing, report that its status cannot be updated and do not create or change the
  map. If the topic's entry is duplicated or malformed, report the ambiguity and leave the map unchanged. An exam
  can still proceed on the clearly identified topic when applicable sources support it.
- Read learner-supplied text files in `sources/` for grading; never add or change sources. If none support this
  topic, say there is no applicable source and do not grade, report an assessed level, assert mistakes, suggest
  unsupported cards, or change map statuses. End with one session line recording `not graded: no source`.

Before the first question, establish a finite ladder of increasingly demanding, source-supported tasks for this
topic, from basic recall to the target outcome. Briefly state the target and score basis without showing questions,
answers, or source excerpts. Use the goal's target, or the learner's stated target when no goal exists; do not
invent a fixed global passing threshold or move the target after the exam starts.

Completing the target unaided counts as `passed`; a clear failure or guess counts as `learning`. Disclose that
only this topic's status may change, including a previously `passed` topic returning to `learning` on failure.

## Ask until the first failure or guess

1. Ask an easy, topic-relevant production question. Wait for the learner's unaided answer; never supply a hint,
   answer, solution, or grading-source excerpt before their attempt.
2. Judge the answer only against the applicable sources. Require the reasoning needed by the question, not a
   word-for-word match. A correct result explicitly admitted to be a guess does not demonstrate understanding.
3. If the answer is genuinely ambiguous, ask one non-leading clarification about their reasoning before deciding.
   This clarifies the same scored question; it is not a retry, another scored level, or permission to teach the
   answer. Do not treat uncertainty in your grading evidence as proof that the learner failed.
4. For a supported, unaided answer, move to a harder scored question requiring more demanding reasoning or
   application within the same topic. Do not restart with easier questions, test another topic, or coach between
   questions in a way that supplies answers to later questions.
5. At the **first clear failure or guess**, stop the exam immediately. Do not ask a harder question, offer a
   second scored attempt, or continue until several failures accumulate. An explicit `I don't know` is a failure.
6. If the learner demonstrates every level through the announced target without failure or guessing, end as
   target completed. Do not keep raising difficulty indefinitely to force a failure beyond the target.

If sources become insufficient or conflicting, stop as inconclusive rather than grade from outside knowledge.
If the learner explicitly ends early, respect that choice and record partial completion, not a pass. An exam
stopped by missing evidence or interruption does not justify a new map status.

## Report and save the result

After the exam stops, show the highest level demonstrated and what stopped it: the failed question or required
reasoning, an admitted guess, the completed target, or an inconclusive/interrupted exam. Report the number of
source-supported unaided answers out of scored attempts and the highest completed level out of the announced
ladder. If the first question failed, report zero completed levels; never imply unasked questions were answered.

For each distinct source-supported mistake caught during the exam, automatically append one line to
`mistakes.md`, creating it with `# Mistakes` if missing:

```md
- <YYYY-MM-DD> | examiner | <topic and concise mistaken idea or missing reasoning> | <source-supported correct idea>
```

Do not ask permission to capture mistakes. For a correct guess, do not invent a factual mistake: record the
failure to justify the answer with the source-supported reasoning that was needed. Give concise corrections only
after the attempt and exam stop. Preserve earlier entries; do not store full answers or a transcript.

Update `map.md` only when the exam has a supported terminal result and the selected topic has one valid entry:

- First clear failure or guess: set that topic's status to `learning`.
- Entire announced target demonstrated unaided: set that topic's status to `passed`.
- No grading source, insufficient evidence, or interrupted exam: leave its status unchanged.

Re-read the map before saving. Replace **only the selected topic's status token**, preserving its name,
dependencies, sticking points, order, formatting, and every other byte. Never change other topics, prerequisites,
headings, or learner content. If the exact entry is now missing or ambiguous, report it and do not change the map.
Use a same-folder temporary file and replacement to avoid truncating an existing map on write failure. If the
status already matches, no map write is needed. Do not claim a status was saved unless the write succeeded.

## Suggest cards and finish

At the end, suggest focused cards based on this session's supported mistakes. Show each proposed front and back
and ask one confirmation question at a time. Add only cards explicitly confirmed by the learner:

```bash
python3 scripts/cards.py add <subject> --front '<confirmed front>' --back '<confirmed back>' --today <YYYY-MM-DD>
```

Use safely quoted arguments or a subprocess argument list, never unescaped shell interpolation. Check the exit
code and returned JSON before claiming an addition. Declined suggestions or silence create no cards. All card
access uses `scripts/cards.py`; never read or edit `cards.json` directly or change existing card grades. If there
were no supported mistakes, do not manufacture cards merely to fill a session.

Append exactly one line to `sessions.md`, creating it with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | examiner | <topic or -> | <correct/attempted; highest level/target levels; failure point or target completed; persistence limitations>
```

For ungraded or inconclusive sessions, record that limitation instead of inventing a score. Use the learner's
local calendar date in ISO `YYYY-MM-DD`, asking if uncertain. Date mistakes when caught, cards when added, and
the session line at session end. Replace literal `|` inside log fields with `/` and collapse field newlines to
spaces. Preserve earlier lines; never append separate session entries for individual questions or suggestions.

If a write or CLI call fails, report what did and did not save and include the failure in the session result when
possible. Before retrying an uncertain log append or map write, read the file to determine what succeeded; do not
duplicate entries or overwrite unrelated content. Card addition is non-idempotent: stop for reconciliation after
an uncertain add rather than blindly repeating it and creating a duplicate card.

Write only the selected topic's map status plus this subject's `mistakes.md` and `sessions.md` directly; confirmed
cards use only the CLI. Do not change goals or sources, create maps, or suggest resource links. Finish with the
level, stopping point, actual status-save result, and paths of files actually changed.
