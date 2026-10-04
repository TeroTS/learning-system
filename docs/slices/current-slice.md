# Current Slice

Status: done

## Slice Goal
- Let the learner get graded by agent judgement when no source applies, instead of getting no grade.

## Slice Boundary
- Learner runs a grading skill on a topic or card that no source covers; the skill announces "no applicable source;
  grading by agent judgement", grades by agent judgement, and appends one session line recording
  `graded: agent judgement`.

## Stories In Scope
- `US-14 Get graded without a source`

## Stories Completed In This Slice
- `US-14 Get graded without a source`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contract 7 (`sources/`) failure expectation changes from "does not grade" to the judgement
  fallback; Contract 6 session line format is unchanged.

## Decision Inputs
- `DECISIONS.md` Interface / Contract Expectations: fallback trigger, announcement, labeling, and full side effects.

## Shared State Required Now
- None new. The session line result field carries `graded: agent judgement`; mistake line format is unchanged.

## Operations / Endpoints / Surfaces In This Slice
- `SKILL.md` of `interviewer`, `mapmaker`, `explainer`, `socratic-questioner`, `examiner`, `checker`, `listener`,
  `review`, `sparring-partner`.
- `docs/contracts.md` Contract 7.

## Tests Required
- Instruction review of each affected skill against US-14 acceptance criteria.
- Grep confirms no remaining `not graded: no source` or "do not grade" no-source rule in skills or contracts.
- `make check` and `git diff --check` pass. No automated skill-Markdown tests per SPEC.md.

## Not Now
- `clerk` and `diagnostician` changes; basis tags in `mistakes.md`; Python changes.

## Done When
- Every affected skill grades by agent judgement when no source applies, announces it, labels it, and applies the
  same side effects as source-based grading, while applicable sources still take precedence and in-source gaps
  stay `unverified`.

## Completion Summary
- Nine grading skills now announce `no applicable source; grading by agent judgement` and grade by judgement when
  `sources/` is missing, empty, or does not cover the topic or card, recording `graded: agent judgement`.
- Judgement grades have full effects: mistakes, card suggestions, `review` scheduling, `examiner` map statuses.
- Applicable sources still take precedence; in-source gaps or conflicts stay `unverified`. Contract 7 updated.
- `sparring-partner` also had the no-source block; added to US-14 in `SPEC.md`.
- `make check` (100% coverage) and `git diff --check` pass. No live agent-session test was run.

## Next Slice Recommendation
- No explicit next story remains in `SPEC.md`.
