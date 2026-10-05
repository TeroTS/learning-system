# Current Slice

Status: implementation complete; TypeScript scope approval pending

## Slice Goal

Fix accepted topic scope and make continuation, exam readiness and next-topic routing use one ordered decision rule.

## Stories In Scope

- US-02: approved finite topic requirements, targets and scope amendments.
- US-06 and US-07: requirement-specific production evidence and gated handoffs.
- US-08: independent readiness checks and exams against fixed accepted targets.
- US-15: general continuation applies the same gate before choosing a role.

## Contract and Decision Inputs

- `DECISIONS.md`: fixed scope, evidence rules, progression, approval and diagnostic exceptions.
- `docs/contracts.md`: Contracts 4 and 6 and `Progression gate`.
- `docs/plans/deterministic-learning-progression.md`: accepted implementation plan.

## Surfaces Changed

- `AGENTS.md`, mapmaker, explainer, socratic-questioner and examiner instructions.
- Decisions, specification, contracts, README and regression scenario documentation.
- `tests/test_exam_readiness.py`: instruction-contract checks, not a live behavioral runner.

## State and Ownership

- No new subject files, CLI changes, dependencies or card-format changes.
- Mapmaker owns approved scope amendments; examiner changes only the examined topic's status.
- History remains append-only; coverage is derived and cited, not stored in a second mutable ledger.
- Learner files are unchanged. The pre-existing AWS session modification is outside this slice.

## Tests Required

```bash
.venv/bin/python -m unittest tests.test_exam_readiness
make test
make coverage
make check
git diff --check
```

## Verification

- Baseline: 52 passing tests, 100% script coverage.
- New instruction checks observed failing before changes: 43 assertion failures across 9 tests.
- Final results: 58 tests pass; 100% script coverage unchanged; `make check` and `git diff --check` pass.
  Details: `docs/plans/deterministic-learning-progression.md` implementation record.
- Synthetic rule review: documented in `docs/testing/exam-readiness.md`; independent live agent replay not run.

## Deferred / Pending

- `docs/plans/typescript-scope-proposal.md` proposes criteria and evidence mapping, not accepted learner scope.
- Obtain explicit approval before amending `subjects/typescript/map.md` or resuming learning under that scope.
- Other subjects remain legacy maps until individually approved; do not automatically migrate them.
- Executable routing, LLM behavioral evaluation and CI remain outside this change.
