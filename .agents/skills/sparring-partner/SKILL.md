---
name: sparring-partner
description: Use when the learner wants a tough interview, sales-call, or speaking simulation at a chosen difficulty and time limit per answer, with pushback during the session and a score afterward.
---

# Sparring Partner

Play a tough simulated counterpart, not an explainer. Use English and give exactly one prompt or question per
turn; wait for the learner's answer before continuing. Require production before feedback. Use only file reads,
file writes, and shell commands. Resolve repository paths from the repository root, not this skill's directory.

## Agree the simulation

- Ask which subject the scenario belongs to if it is not given. Reuse its existing folder under `subjects/`; if
  missing, direct the learner to `interviewer` without creating a folder or writing elsewhere.
- Require a subject name matching `^[a-z0-9]+(-[a-z0-9]+)*$`; reject paths, slashes, `..`, and empty names. Ask about
  ambiguous names. Do not follow a subject-folder symlink outside `subjects/`, or goal, source, or log file symlinks
  outside the subject folder.
- Read `goal.md`, `mistakes.md`, and `sessions.md` if present. Use the goal for context, not to silently replace
  the learner's chosen difficulty. Treat a missing level as unknown and ask if needed; do not update the goal.
- Collect the scenario, counterpart role, difficulty, and time limit per answer, one question at a time, reusing
  details already supplied. Clarify what an ambiguous difficulty means in terms of objections or reasoning demands.
- Require a positive, finite, unambiguous time limit. Clarify missing units or invalid values rather than inventing
  a limit or clamping it. Preserve the supplied limit; do not secretly extend it for weak answers.
- Agree a finite session endpoint, such as a number of prompts, before starting. Summarize the scenario, difficulty,
  per-answer limit, endpoint, and scoring basis; resolve ambiguities before the first timed prompt.
- Read applicable text files in `sources/` for scoring and supported corrections; never add or change sources.
  Use their rubric if available, otherwise derive a small set of source-backed criteria relevant to the scenario.
  Explain the basis without supplying model answers. Do not invent a global score scale.

If no applicable source exists, say so and do not grade correctness, invent a score, or record unsupported mistakes
or correct ideas. A simulation may still proceed as explicitly ungraded production with in-character requests
for specifics; record `not graded: no source` at the end. Fictional scenario details are simulation context, not
new grading sources or real-world facts.

## Establish real per-answer timing

Agree a measurement method before claiming the simulation is timed. Prefer the learner's timer, started when the
prompt is visible and stopped when their answer is complete; ask them to include elapsed time or `time expired`
with each answer. Label this timing **learner-reported**, not independently verified. Reliable visible message
timestamps may be used only when they represent the same prompt-available-to-answer-complete interval.

Do not estimate elapsed time from answer length, turn count, or how long a shell command ran. A timestamp taken
before generating a prompt or after your later analysis includes agent latency and is not an exact answer timer.
Do not claim automatic interruption or a hard timeout that the current agent cannot enforce.

- Each new prompt, including a pushback question, starts a fresh interval with the same supplied limit.
- An answer at or below the limit is on time; an answer above it is late. At expiry, the learner should submit the
  partial answer or report timeout, not reset the timer to polish that same answer.
- Require reported elapsed times to be finite, non-negative durations with clear units. If timing is missing or
  invalid, ask for clarification without giving content feedback first. If no reliable timing can be supplied,
  mark it unverified and exclude it from any claim of verified timing compliance.
- If the learner cannot use a timer and usable timestamps are unavailable, say the time limit cannot be verified.
  Ask whether they want to continue with unverified timing; never silently present that as an enforced timed run.

## Run the simulation

Adopt the agreed counterpart and keep the supplied difficulty throughout the session. For an interview, press
for reasoning and concrete evidence; for a sales call, act as a skeptical prospective customer; for speaking,
challenge the claim or explanation as the agreed audience. Keep demands within the scenario and difficulty;
being tough does not mean personal insults or arbitrarily changing the task.

Give one timed prompt, wait for the answer, and then respond in character:

- Push back on vague claims, unsupported assertions, or evasions by asking for a specific example, decision,
  justification, or response to an objection. Tie the pushback to what the learner actually said.
- Do not provide a model answer, script their response, or turn the simulation into a lesson before they attempt.
- After a late or timed-out answer, note its timing status and assess only the content actually submitted where
  sources support it. Do not award a complete response for an unfinished one or treat lateness as a factual error.
- Count every new pushback prompt toward the agreed endpoint and apply the same per-answer limit to it. Do not
  quietly add unlimited rounds, repeat a timed answer to erase its result, or raise/lower difficulty mid-session.
- If the learner explicitly changes difficulty, limit, or endpoint, clarify and acknowledge the change before the
  next prompt, applying it prospectively rather than rescoring earlier answers under new conditions.

When the endpoint is reached, stop the simulation and give the result. If the learner stops early, respect that
choice and report the completed portion as partial. Keep responses and timing in the conversation; do not store
a simulation transcript, audio, or video, or invent delivery details unavailable from text.

## Score, capture mistakes, and suggest cards

With applicable sources, report the source-rubric score or satisfied criteria out of applicable assessed criteria,
and explain the strongest and weakest answers using specific prompt locations and source evidence. Mark any
unsupported or conflicting criteria ungraded rather than substituting general knowledge. Do not claim an overall
score if nothing was gradable. State which rounds were assessed and which were incomplete or unverified.

Report timing separately as on-time, late, timeout, or unverified for each answer and a compliance count with its
measurement provenance. If the source rubric includes timing, apply the supplied limit using the agreed timing
method and state its limitations; do not silently omit timing from that score. Content success does not erase a
late response, and learner-reported elapsed time is not independently verified timing.

Automatically append each distinct source-supported weak answer or mistake to `mistakes.md`, creating it with
`# Mistakes` if missing:

```md
- <YYYY-MM-DD> | sparring-partner | <scenario, prompt number, and concise weakness or mistake> | <source-supported correct idea>
```

Do not ask permission to capture mistakes. Preserve earlier entries and avoid duplicate lines for repeated
pushback on the same mistake. Do not log lateness alone, personal preferences, or unsupported judgments as factual
mistakes; timing belongs in the session result. Do not save full answers or a transcript.

Suggest focused cards based on this session's captured mistakes. Show each proposed front and back and ask one
confirmation question at a time. Add only cards explicitly confirmed by the learner:

```bash
python3 scripts/cards.py add <subject> --front '<confirmed front>' --back '<confirmed back>' --today <YYYY-MM-DD>
```

Use safely quoted arguments or a subprocess argument list, never unescaped shell interpolation. Check the exit
code and returned JSON before claiming an addition. Declined suggestions or silence create no cards. All card
access uses `scripts/cards.py`; never read or edit `cards.json` directly or change existing card grades. If there
were no supported mistakes, do not manufacture cards.

## Save the session

Append exactly one line to `sessions.md`, creating it with `# Sessions` if missing:

```md
- <YYYY-MM-DD> | sparring-partner | <scenario/topic or -> | <difficulty; per-answer limit; score or not graded; timing provenance/compliance; partial or persistence limitations>
```

Use the learner's local calendar date in ISO `YYYY-MM-DD`, asking if uncertain. Date mistakes when caught, cards
when added, and the session line at session end. Replace literal `|` inside log fields with `/` and collapse field
newlines to spaces. Preserve earlier lines; do not add session entries for individual prompts or card suggestions.

If a write or CLI call fails, report what did and did not save and include the failure in the session result when
possible. Before retrying an uncertain log append, read the file to see whether the intended entry was written;
do not duplicate entries or remove earlier lines. Card addition is non-idempotent: stop for reconciliation after
an uncertain add rather than blindly repeating it and creating a duplicate card.

Write only this subject's `mistakes.md` and `sessions.md` directly; confirmed cards use only the CLI. Do not change
goals, maps, sources, or suggest resource links. Finish with the score or grading limitation, timing result, key
weaknesses, and paths of files actually changed.
