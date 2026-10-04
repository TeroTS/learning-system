# Current Slice

Status: done

## Slice Goal
- Let the learner accept a goal-fitted subject map with topics in dependency order and usual sticking points.

## Slice Boundary
- Learner runs `mapmaker`, reviews and accepts a proposed map, sees ordered topics and sticking points, and writes one subject's `map.md` with every included topic set to `todo` plus one `sessions.md` line.

## Stories In Scope
- `US-02 Map a subject`

## Stories Completed In This Slice
- `US-02 Map a subject`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 3 (`goal.md`), 4 (`map.md`), 6 (`sessions.md`), 7 (`sources/`), 8 (skill format); Contract 1 subject-name pattern.

## Decision Inputs
- None.

## Shared State Required Now
- One subject folder, optional existing goal and map, unique topic names with ordered dependencies, and an append-only session log.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/mapmaker/SKILL.md`.
- `subjects/<subject>/map.md` and `subjects/<subject>/sessions.md` at skill runtime only.

## Tests Required
- Review instructions against US-02 and applicable contracts: learner production, goal fitting, known-topic omission, dependency order, sticking points, acceptance before writing, and all statuses initially `todo`.
- Check missing goals, existing maps, ambiguous or unsafe subject names, unverified resource links, and write failures.
- Run `make check` for existing code regressions and coverage, plus `git diff --check`.
- No automated skill-Markdown tests per SPEC.md. No runnable agent-session harness exists; a real learner mapmaking session is not an executable repository end-to-end test.

## Not Now
- US-03 Add a card and US-04 List due cards; US-08 examiner status changes; other learning roles.
- Card scheduling, agent-session test infrastructure, and sample learner data.

## Done When
- The portable mapmaker skill asks for learner production before proposing a goal-fitted map and skips topics already known.
- The learner accepts a map with unique kebab-case topics in dependency order, explicit sticking points, and every included topic set to `todo`.
- The skill writes the contracted map and appends exactly one contracted session line without touching other subject files; links are checked or marked unverified.
- Instruction review and `make check` pass.

## Completion Summary
- Added the portable mapmaker skill: learner production, goal-fitted scope, known-topic omission, dependency-ordered topics, and usual sticking points.
- Instructions require explicit learner acceptance before writing the contracted map with all statuses `todo`, and exactly one append-only session line.
- Instruction review covered US-02 and the listed contracts, including missing goals or sources, existing-map replacement, unsafe names, unverified links, and partial write failures.
- `make check` passed: 4 existing tests, formatting, lint, and 100% Python coverage (unchanged). `git diff --check` passed.
- No live learner mapmaking session or automated agent-session end-to-end test was run; skill execution remains manually validated at use time.

## Next Slice Recommendation
- `US-03 Add a card`. Keep US-04 List due cards and US-05 Review due cards in view, but outside that slice.
