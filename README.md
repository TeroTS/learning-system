# Learning System

A local, agent-agnostic learning system for one learner and many subjects. Eleven skills guide active learning:
answering, explaining, attempting, and recalling—not just reading explanations. A Python script handles
Leitner-box spaced repetition.

There is no standalone app or web server. Use the skills through your existing coding agent.

## Requirements

- Python 3.11 or newer for card scheduling; no runtime dependencies beyond the standard library.
- An agent that can read/write local files and run shell commands. Automatic discovery of `.agents/skills/`
  is convenient but not required.
- Git for cloning; `make` for the optional development commands.

```bash
git clone https://github.com/TeroTS/learning-system.git
cd learning-system
python3 --version
```

Open this repository as your agent's working directory. If it discovers repo-local skills, request a skill by
name. Otherwise, tell it to read and follow the corresponding `.agents/skills/<name>/SKILL.md` file. Skill names
are agent instructions, **not shell commands**; no particular slash-command syntax is required.

## Start learning

### 1. Establish a subject and goal

Send your agent:

```text
Read and follow .agents/skills/interviewer/SKILL.md to start statistics.
My goal is to interpret descriptive statistics in research papers.
```

Answer its questions one at a time. It collects a specific goal, current level, deadline, and test format, asks
progressively harder production questions, and saves the confirmed result in `subjects/statistics/goal.md`.
Running it again updates the same goal rather than creating another subject.

Start new subjects with `interviewer`; most other skills require an existing subject folder. Names use lowercase
letters/digits separated by hyphens, such as `statistics` or `technical-interviews`.

### 2. Supply material for grading

After the subject exists:

```bash
mkdir -p subjects/statistics/sources
```

Put your own text-readable study material, explanations, or grading rubrics in that folder. Markdown and plain
text are straightforward choices. The skills read these files but never add to or change them.

**Correctness grading uses only applicable files in `sources/`.** Without them, skills report that grading is
unavailable or correctness is unverified; they do not substitute general knowledge. In particular, `review`
needs source support even when a card already has a back. Organising notes with `clerk` does not require sources.

### 3. Accept a map

```text
Use mapmaker for statistics. Fit the map to my goal and skip topics I already know.
```

Review the proposed topics, dependencies, and sticking points. Only after acceptance does the skill write
`map.md`, with included topics initially marked `todo`. Replacing a map resets its included statuses, so check
the proposal before accepting.

### 4. Produce answers and get feedback

Choose a skill for the task rather than asking for a complete lesson or solution. For example:

```text
Use explainer for statistics. I am stuck on the variance calculation in this task.
Here is my attempt: ...
```

```text
Use examiner on the spread topic in statistics. Assess me against my sources.
```

```text
Use checker for statistics. Here is my solution and rubric: ...
```

Replace `...` with your own work. The explainer requires a fresh redo from the start; the examiner stops at the
first clear failure or guess; the checker points to specific problems without rewriting your work.

Skills that capture mistakes append them automatically to `mistakes.md`. At session end, they suggest cards;
**only explicitly confirmed cards are added**. You may decline suggestions.

### 5. Review and diagnose

```text
Use review for statistics. Ask each due card's front and wait for my answer before showing its back.
```

Review regularly: there is no background scheduler or reminder service. New cards are first due tomorrow.
Correct answers promote a card one box, capped at box 5; wrong answers reset it to box 1. The next due date is
measured from the grading date using the interval for the new box:

| Box | Interval |
| --- | --- |
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5 | 30 days |

After several sessions, ask:

```text
Use diagnostician to find recurring root misunderstandings across all my subjects.
```

It cites the recorded mistakes supporting each finding and logs the diagnosis only in affected subjects.
With no mistakes or insufficient recurring evidence, it does not invent a diagnosis.

## Choose a skill

Each name links to its full instructions.

| Skill | Use it to |
| --- | --- |
| [interviewer](.agents/skills/interviewer/SKILL.md) | Establish or update a goal and assess the current level. |
| [mapmaker](.agents/skills/mapmaker/SKILL.md) | Build a goal-fitted map in dependency order. |
| [explainer](.agents/skills/explainer/SKILL.md) | Explain one stuck step, then redo the task unaided. |
| [socratic-questioner](.agents/skills/socratic-questioner/SKILL.md) | Discover a gap through questions, not supplied answers. |
| [examiner](.agents/skills/examiner/SKILL.md) | Answer increasingly hard questions and update one topic's status. |
| [checker](.agents/skills/checker/SKILL.md) | Check intermediate steps against a rubric without rewriting work. |
| [listener](.agents/skills/listener/SKILL.md) | Grade transcribed speech, writing, or a drawing description against sources. |
| [sparring-partner](.agents/skills/sparring-partner/SKILL.md) | Simulate an interview, sales call, or speaking scenario with pushback. |
| [clerk](.agents/skills/clerk/SKILL.md) | Organise only your own notes into an outline or proposed cards. |
| [review](.agents/skills/review/SKILL.md) | Recall due cards before seeing their backs and update their schedule. |
| [diagnostician](.agents/skills/diagnostician/SKILL.md) | Find evidence-backed root misunderstandings across subjects. |

For `listener`, supply a transcript or drawing description; automatic audio transcription and image recognition
are not provided. For `sparring-partner`, supply the scenario, difficulty, and a positive time limit per answer.
Agree a session endpoint and use a timer, reporting elapsed time with each answer. Learner-reported timing is
not independently verified, and the skill does not promise automatic hard timeouts.

## Your subject store

Files are created as needed, not all at once:

```text
subjects/statistics/
├── goal.md       # Specific goal, assessed level, deadline, test format
├── map.md        # Topics, dependencies, sticking points; todo/learning/passed
├── mistakes.md   # Append-only dated mistakes and correct ideas
├── sessions.md   # Append-only session outcomes or scores
├── cards.json    # Card storage managed only by scripts/cards.py
└── sources/      # Learner-supplied grading material; read-only for skills
```

Ordinary skill sessions append one session line. `diagnostician` appends one per subject with related findings,
and none when there are no findings. Dates use your local calendar date; tell the agent if its date differs.
Outlines and full explanations/transcripts are not saved by the skills; `clerk` shows outlines in the conversation.

Back up your subject folders. They are **not ignored by Git by default**: check what you stage and push, especially
private notes or copyrighted source material. The store is local, but your agent may send its contents to its model
provider; use your agent's privacy settings accordingly. Avoid simultaneous writers to the same subject.

## Card CLI: optional manual use

Run commands from the repository root. These examples assume `interviewer` already created `statistics`.
The agent normally runs them for you.

```bash
python3 scripts/cards.py add statistics \
  --front 'How is the arithmetic mean calculated?' \
  --back 'Sum the values and divide by their count.'

python3 scripts/cards.py due statistics

python3 scripts/cards.py grade statistics 1 --result right
```

`add` prints the created card as JSON, including its id and due date. Replace `1` with the actual card id when
grading, and grade only after an answer has been judged against your sources. Use `--result wrong` for a wrong answer.

`due` prints a JSON array sorted by due date, then id; `[]` means no cards are due. **Its raw output includes
backs**, so use the review skill rather than reading it before a recall attempt. A newly added card is not due
on its creation date.

All subcommands accept `--today YYYY-MM-DD` to supply the local date explicitly and `--subjects-dir PATH` to use
another subject store. The default store is this repository's `subjects/`, not a folder relative to your shell.
For example, this pins the date for a reproducible listing:

```bash
python3 scripts/cards.py due statistics --today 2026-01-02
```

Exit codes: `0` success, `1` invalid input/data or storage failure, `2` bad command usage. Errors go to stderr;
JSON results go to stdout. Card writes use atomic replacement. Invalid existing storage is rejected, not repaired.
Do not edit `cards.json` manually or blindly repeat an uncertain `add` or `grade`: another successful `add` creates
another card, and `grade` reapplies the box/schedule transition. Inspect/reconcile the result before retrying.

## Development and checks

Learning and card scheduling do not require installing development packages. To work on this repository:

```bash
make install
make test
make coverage
make check
```

`make install` uses Python 3.11 from `.python-version` and recreates `.venv`. If your supported Python is available
only as `python3`, use `make install PYTHON=python3` instead. It installs pinned Ruff and coverage dependencies.

- `make fmt`: format Python.
- `make lint`: lint Python.
- `make check`: check formatting, lint, and run tests with coverage.
- `make coverage`: run tests and print the coverage report; the configured minimum is 80%.

Optional HTML coverage report:

```bash
.venv/bin/coverage html
```

Open `htmlcov/index.html`. CLI behavior has automated tests; live agent-driven skill sessions do not have an
end-to-end test harness. There is no CI configuration. Script logging uses stderr and `LOG_LEVEL`, defaulting
to `WARNING`; an invalid level is an error. Learner content is not logged by the card script.

For authoritative details, see [SPEC.md](SPEC.md), [file and CLI contracts](docs/contracts.md),
[domain vocabulary](CONTEXT.md), and [repository guidance](AGENTS.md).
