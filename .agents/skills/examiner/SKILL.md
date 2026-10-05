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
  topic. If the map, topic or accepted scope/target is missing, report the gate limitation and offer a mapmaker
  handoff; do not create or change scope or begin an exam. If an entry is duplicated or malformed, report the
  ambiguity and leave the map unchanged. A clearly named topic alone is not an accepted exam target.
- Read learner-supplied text files in `sources/` for grading; never add or change sources. An applicable source
  always takes precedence. If `sources/` is missing or empty, or no source covers this topic, announce
  `no applicable source; grading by agent judgement` without asking, then grade by agent judgement. For that exam,
  read `source-supported` below as `supported by agent judgement` and record `graded: agent judgement` in the
  session line. Judgement-based results have the same effects as source-based ones: level report, mistakes, card
  suggestions, and map status updates, including `passed`.

## Check exam readiness

Apply `Check exam readiness` independently before the first question, including after a handoff from another skill.

- Read `docs/contracts.md` Contracts 4 and 6 and `Progression gate` before offering continuation, an exam or the next topic.
  Apply its ordered decision table using the accepted checklist and passing target in `map.md` and cited production
  evidence. Do not infer additional required concepts from goals, sources or sticking points.
- Missing accepted scope requires a mapmaker handoff, not an invented checklist. Unmet dependencies require the
  disclosed dependency action; unknown or unresolved requirements require continued learning in checklist order.
  All requirements resolved permits an exam offer, not a pass. Readiness checks never change map status.
- Wait for confirmation before switching roles or applying a disclosed progression override. Readiness alone does
  not justify moving topics; do not offer the next topic merely because one redo or correction succeeded.
- An early diagnostic exam is allowed only when explicitly requested by the learner. Disclose the uncovered or
  unknown concepts and that this exam can set the topic to `learning` on failure or `passed` on target completion,
  and any unmet dependencies, then obtain informed confirmation before starting or handing off. A bare `ok` to a
  premature exam offer is not an informed diagnostic request. Do not silently shrink the exam target to the concepts
  already covered. No accepted target means no diagnostic exam.

If readiness is blocked and the learner ends or chooses continued learning before the exam starts, record
`not started: coverage incomplete or unknown` in the single session line, with the specific gaps and no invented
score. Leave the map unchanged.

## Announce the exam target

Only after readiness or an informed diagnostic request is established, create a finite ladder of increasingly
demanding, source-supported tasks for this topic, from basic recall to the target outcome. Use the accepted passing target in `map.md`
and cover every accepted requirement. Do not add requirements or change passing criteria during the exam.
Question wording may vary, not required concepts or success conditions. Briefly state the accepted target and score
basis without showing questions, answers, or source excerpts. Do not invent a global passing threshold. If the target
cannot support a clear ladder, offer a mapmaker clarification rather than silently revising it.

Completing the target unaided counts as `passed`; a clear failure or guess counts as `learning`. Disclose that
only this topic's status may change, including a previously `passed` topic returning to `learning` on failure.

## Choose fresh exam tasks

Compare proposed tasks with learning and previous exam examples in the current conversation and `sessions.md` task summaries
before presenting each scored question. Do not reuse learning examples as scored exam questions.
Do not repeat previous exam solutions either. Renaming identifiers or swapping values alone is not sufficient.
Change the reasoning task and context/data so the learner must apply the same accepted concepts independently,
without adding requirements, unlearned concepts or difficulty beyond the accepted target. Standard syntax intrinsic
to the concept may recur; a previously solved task and its solution chain must not.

If prior task history is insufficient, choose a new scenario and report `freshness unverified`, not proven novelty.
Replace a duplicate before asking. If duplication is discovered after presentation, withdraw it unscored and replace
it at the same level before giving feedback; it is not a learner failure or a scored retry.
Repeated examples do not count as transfer evidence. Do not retroactively rewrite historical grades or force a
re-exam when the learner declines one.

## Ask until the first failure or guess

1. Ask an easy, topic-relevant production question. Wait for the learner's unaided answer; never supply a hint,
   answer, solution, or grading-source excerpt before their attempt.
2. Judge the answer against the applicable sources, or by agent judgement when none apply. Require the reasoning
   needed by the question, not a word-for-word match. A correct result explicitly admitted to be a guess does not
   demonstrate understanding.
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

If applicable sources become insufficient or conflicting, stop as inconclusive rather than fill gaps from judgement.
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
- Insufficient evidence within an applicable source, or interrupted exam: leave its status unchanged.

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

Record tested requirement IDs, resolved/unresolved/unknown states, unaided attribution and concise evidence per
`docs/contracts.md` Contract 6. Include short task context and any freshness-comparison limits, not full questions,
solutions or transcripts. Never claim unasked requirements were demonstrated.
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
