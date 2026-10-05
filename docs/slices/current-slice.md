# Current Slice

Status: done

## Slice Goal
- Assess learner production by agent judgement without requiring answer files.

## Slice Boundary
- Learner submits an answer to a grading skill; the skill assesses it against accepted requirements and targets,
  shows feedback identified as agent judgement, and appends the session result with `graded: agent judgement`.

## Stories In Scope
- `US-14 Get assessed by agent judgement`

## Stories Completed In This Slice
- `US-14 Get assessed by agent judgement`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 4–9 and Progression gate; Contracts 1–2 for unchanged card transitions.

## Decision Inputs
- None.

## Shared State Required Now
- Existing accepted map requirements/targets, append-only mistakes/sessions and CLI-managed cards.
- Agent judgement is universal; genuine uncertainty remains unverified, not a learner failure.
- Historical evidence and attribution remain unchanged.

## Operations / Endpoints / Surfaces In This Slice
- Nine grading skills, README and CONTEXT.md; focused instruction-contract tests.
- Reconcile the completed legacy progression slice note into this single-story brief; learner scope approval remains
  separate and is not granted by repository maintenance.

## Tests Required
- Add regression checks covering universal grading, accepted scope, attribution, uncertainty and removal of source-first rules.
- Preserve review's ungraded-card safeguard and examiner's inconclusive-result safeguard; preserve clerk/diagnostician boundaries.
- Run `.venv/bin/python -m unittest tests.test_agent_judgement`, `make test`, `make coverage`, `make check`
  and `git diff --check`.
- Baseline: `make check` passed, 60 tests and 100% script coverage. New regression checks failed as expected
  with 12 assertion failures before skill and public-guidance changes.
- No live agent end-to-end harness exists; instruction checks do not establish agent compliance or answer correctness.

## Not Now
- US-02 learner map approval/amendments and US-15 progression changes; existing routing is preserved.
- Script/CLI/schema changes, dependencies, LLM evaluation, CI and learner-store edits.
- Historical plan documents are not retroactively rewritten.

## Done When
- All grading skills use agent judgement regardless of source availability, without fallback announcements or answer-file prerequisites.
- Feedback/session attribution and uncertainty safeguards match Contract 9; normal card/exam effects remain intact.
- Vocabulary and README agree; automated checks pass without decreasing script coverage.

## Completion Summary
- Nine grading skills now use agent judgement without source-first branches or answer-file prerequisites.
- Genuine uncertainty stays unverified; uncertain/incorrect-back cards stay ungraded and inconclusive exams leave
  status unchanged. Normal confirmed card additions, established mistakes and unaided exam passes remain supported.
- README and source vocabulary align; learner files, historical evidence and scheduling code are unchanged.
- Four new instruction-contract tests; 64 total tests pass, script coverage remains 100%, and format/lint/diff checks pass.
- No live agent replay was run: instruction checks cannot prove assessment correctness or agent compliance.

## Next Slice Recommendation
- No explicit next story remains in `SPEC.md` to implement; existing skills and CLI provide the other story surfaces.
- Pending learner scope approval remains a separate US-02 learning workflow, not repository-maintenance authorization.
