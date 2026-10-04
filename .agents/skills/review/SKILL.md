---
name: review
description: Use when the learner wants to recall a subject's due cards from memory, receive source-supported feedback, and update their Leitner schedule.
---

# Review

Review due cards through learner production, not passive reading. Use English and ask exactly one question per
turn; wait for the answer before continuing. Use only file reads, file writes, and shell commands. Resolve
repository paths from the repository root, not this skill's directory.

## Prepare the session

- Ask which subject to review if it is not given. Reuse its existing folder under `subjects/`; never create a
  subject during review. If the subject is missing, direct the learner to `interviewer` and do not write elsewhere.
- Require a subject name matching `^[a-z0-9]+(-[a-z0-9]+)*$`; reject paths, slashes, `..`, and empty names.
  Ask about ambiguous names. Do not follow a subject-folder symlink outside `subjects/`, or source and log file
  symlinks outside the subject folder.
- Read existing `mistakes.md` and `sessions.md` if present. Read learner-supplied text files in `sources/` for
  correctness judgments; never add or change sources. A missing goal means level unknown, not a blocked review.
- Establish the learner's local calendar date in `YYYY-MM-DD`, asking if uncertain. Pass it explicitly as
  `--today` so the script's system date cannot silently substitute a different local date.
- All card access goes through `scripts/cards.py`; never read or edit `cards.json` directly.

Get the due cards using:

```bash
python3 scripts/cards.py due <subject> --today <YYYY-MM-DD>
```

**Capture stdout rather than displaying this command's raw output.** It contains backs. Use shell commands and
Python's standard-library `subprocess` and `json` to capture it and project only each card's `id` and `front` before
any learner-visible output. Check the command's exit code before parsing. Preserve the returned due/id order.
Never show the raw due JSON, a list of backs, source excerpts, hints, or explanations before attempts.

If the command fails, report the failure without exposing card content and do not treat it as an empty queue.
If no cards are due, say so and finish with one session line recording `no cards due`; do not create card storage.
An applicable source always takes precedence. If `sources/` is missing or empty, or no source covers a card,
announce `no applicable source; grading by agent judgement` without asking, then grade that card by agent judgement.
For such cards, read `source-supported` below as `supported by agent judgement`. Judgement-based grades have the same
effects as source-based grades: run `grade`, record mistakes, and suggest cards. Include `graded: agent judgement`
in the session line when any card was graded this way.

## Recall and grade one card at a time

For each card in the initial due queue:

1. Show only its front and ask the learner to answer from memory. Wait for an unaided attempt; do not reveal the
   back even if the learner asks for a hint first. An explicit `I don't know` counts as an attempt, not a right answer.
2. After the attempt, retrieve the current card through `due` with stdout captured, selecting only that card's id
   before displaying anything. Do not expose the other cards' backs. If it is no longer due or is missing, report
   that its state changed and do not grade the stale queue entry.
3. Judge correctness against applicable files in `sources/`, or by agent judgement when none cover the card. The
   stored back is the recall target, not a substitute for a source. Accept supported paraphrases; do not require a
   verbatim answer. If an answer is ambiguous, ask one clarification before revealing the back.
4. If the back conflicts with an applicable source, explain this after the attempt and leave
   the card ungraded. Show the stored back only as conflicting content; do not silently repair it,
   claim correctness, or record an unsupported mistake.
5. Otherwise, show whether the attempt was right or wrong, the back, and a concise source-supported
   correction when needed. For every wrong answer, append the mistake as described below without asking permission.
6. Run exactly one grade command for this attempted card, using the learner's local date at grading time:

   ```bash
   python3 scripts/cards.py grade <subject> <id> --result right --today <YYYY-MM-DD>
   python3 scripts/cards.py grade <subject> <id> --result wrong --today <YYYY-MM-DD>
   ```

   Choose **one** of these commands, not both. Check the exit code. On success, show the next due date from the
   returned card, not a date calculated by the skill. Right moves up one box, capped at 5; wrong resets to box 1.
   The new-box intervals are 1, 3, 7, 14, and 30 days, measured from the grading date.

Do not grade unanswered cards or repeat a card merely because it was wrong. Stop if the learner ends the session;
leave the remaining cards unchanged and record partial completion accurately.

## Record mistakes and suggest cards

Create `mistakes.md` with `# Mistakes` if missing and append one line per caught mistake:

```md
- <YYYY-MM-DD> | review | <card id and concise mistaken idea or failed recall> | <source-supported correct idea>
```

Use the date the mistake was caught. Preserve all earlier lines. Store concise mistakes, not full answers or a
conversation transcript. If the mistake append fails, report it and pause before grading that card.

At the end, suggest focused cards based on this session's recorded mistakes. Avoid duplicating a card just
reviewed; suggest a narrower card only when it addresses the mistake usefully. Show each proposed front and back
and ask one confirmation question at a time. Add only the cards explicitly confirmed by the learner:

```bash
python3 scripts/cards.py add <subject> --front '<confirmed front>' --back '<confirmed back>' --today <YYYY-MM-DD>
```

Pass text as safely quoted arguments or a subprocess argument list, never unescaped shell interpolation. Check
success before claiming a card was added. A declined suggestion changes nothing; no confirmation means no addition.

## Finish and handle failures

Append exactly one line at the end of the session, creating `sessions.md` with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | review | <subject> | <number graded; right/wrong counts; ungraded or remaining cards and any failures>
```

Use the learner's local date at session end. Replace literal `|` inside all log fields with `/` and collapse field
newlines to spaces. Preserve existing lines; do not append separate session lines for cards or suggestions.

If a write or CLI call fails, report what did and did not save. Do not claim a new due date without a successful
grade result. Both `grade` and `add` are non-idempotent: **never blindly repeat an uncertain command**. For uncertain
grade outcomes, inspect the selected card through captured `due --today 9999-12-31` output and compare its box and
due date with the pre-grade state and intended transition. Do not display other backs or apply another transition
if the intended state is already present. If the outcome remains ambiguous, stop and report it rather than retry.
For an uncertain add, stop for reconciliation rather than risk creating a duplicate card.

Before retrying an uncertain log append, read the log to determine whether this session's entry was written.
Do not duplicate it or remove previous entries. If grading failed after a mistake was recorded, preserve that
mistake and record the scheduling failure in the session result.

Write only this subject's `mistakes.md` and `sessions.md` directly; card changes use only the CLI. Never change
`goal.md`, `map.md`, or sources. Do not suggest resource links during review. Finish with a concise result and the
paths of the files actually changed, without revealing any unanswered card's back.
