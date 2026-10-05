# AGENTS.md

## Project

An agent-agnostic learning system based on `transcript.txt`. It is a set of skills, one for each learning role, plus a
local store for each subject, with spaced repetition handled by a Python script.
The accepted decisions are in `DECISIONS.md`.

## Repo Layout

- `.agents/skills/<skill>/SKILL.md`: the skills, one per role, plus `review`.
- `subjects/<subject>/`: the learner's store (`goal.md`, `map.md`, `mistakes.md`, `sessions.md`, `cards.json`, `sources/`).
- `scripts/`: Python scripts, standard library only (`cards.py`, `logging_setup.py`).
- `tests/`: `unittest` tests, one `test_<module>.py` per script module.
- `.python-version`: pinned Python version (3.11, the minimum supported).

## Commands

- `make install`: create `.venv` and install pinned dev dependencies.
- `make fmt` / `make fmt-check`: format with ruff, or check formatting only.
- `make lint`: run ruff lint.
- `make test`: run the unittest suite.
- `make coverage`: run tests under coverage (fails below 80%).
- `make check`: run the format check, lint and coverage; run this before committing.

## Run a Single Test

```bash
.venv/bin/python -m unittest tests.test_logging_setup                                       # one file
.venv/bin/python -m unittest tests.test_logging_setup.ConfigureLoggingTest.test_defaults_to_warning  # one case
```

## Learning progression

- For general requests such as “continue TypeScript,” read the subject's goal, map and sessions before choosing a role
  or offering the next topic. Read `docs/contracts.md` Contracts 4 and 6 and apply its `Progression gate` in order.
- Use only accepted requirement checklists and passing targets. Missing legacy scope requires a mapmaker approval
  handoff; do not invent additional blockers or treat sticking points as the whole scope.
- Report requirement states with evidence citations. Unknown/unresolved requirements mean continued learning;
  complete coverage means an exam offer, not a pass; only a pass permits normal next-topic progression.
- Scope changes and disclosed progression overrides require explicit confirmation. Do not silently switch roles
  or rewrite historical learner evidence. Repository maintenance is not a learning session and must not create
  learner session entries or approve learner scope on their behalf.

## Logging

- Scripts call `configure_logging()` from `scripts/logging_setup.py` once at the entry point.
- Use `logging.getLogger(__name__)`. Logs go to stderr; stdout is for command output only.
- Set the level with `LOG_LEVEL` (default `WARNING`), for example `LOG_LEVEL=DEBUG`.
- Never log secrets or learner content.

## Domain Vocabulary

- Read `CONTEXT.md` before naming domain concepts.
- Use its canonical terms consistently in code, tests, documentation, and
  user-facing output.
- Resolve terminology conflicts before adding or renaming terms.
- Treat the accepted specification as authoritative for behavior and
  `CONTEXT.md` as authoritative for naming.
- Preserve public-interface compatibility; do not silently rename established
  CLI, JSON, or API fields.

## Commenting Convention

- Every production module and function must have comment directly above it.
- The comment must state its purpose, key inputs/output, and externally visible effects or
failure handling where applicable.
- Docstrings do not satisfy this rule.

Exemptions:

- generated files
