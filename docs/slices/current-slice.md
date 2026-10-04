# Current Slice

Status: done

## Slice Goal
- Let the learner face a tough simulated counterpart at their chosen difficulty and per-answer time limit, then see their score and weak answers.

## Slice Boundary
- Learner runs `sparring-partner` with a scenario, difficulty, and time limit per answer; they answer one simulated prompt at a time, receive pushback during the session and a source-supported score at the end, with supported weak answers appended to `mistakes.md` and one scored session line.

## Stories In Scope
- `US-11 Spar in a timed simulation`

## Stories Completed In This Slice
- `US-11 Spar in a timed simulation`

## Stories Remaining In This Slice
- None.

## Contract Inputs
- `docs/contracts.md`: Contracts 1 (confirmed-card add CLI), 3 (goal context), 5 (mistake log), 6 (scored session line), 7 (source-only grading), and 8 (portable skill).

## Decision Inputs
- None.

## Shared State Required Now
- Existing subject, scenario and counterpart, learner-selected difficulty and positive per-answer time limit, applicable sources, and append-only mistake/session logs.
- Agreed session endpoint, source-backed scoring criteria, answers, and measured or learner-reported timing stay in the conversation; no timer service, transcript, or new persistent simulation model.

## Operations / Endpoints / Surfaces In This Slice
- `.agents/skills/sparring-partner/SKILL.md`.
- Skill-owned appends to `mistakes.md` and `sessions.md`; existing `scripts/cards.py add` only for confirmed suggestions.
- Learner-operated timer or reliable visible message timing for per-answer elapsed time, with provenance and limitations stated explicitly.

## Tests Required
- Review instructions against US-11: required scenario/difficulty/time limit, tough counterpart, one prompt per turn, learner production before feedback, in-session pushback on vague answers, and final score basis.
- Check exact supplied difficulty and limit are preserved, units and non-positive limits are clarified, timing starts at prompt availability, each new prompt has its own timer, and on-limit/late/partial answers are handled explicitly without invented elapsed times.
- Check unavailable or self-reported timing, missing/conflicting sources, scenario adaptation without role drift, session endpoint and interruption, automatic supported mistake capture, confirmed-only cards, safe paths, local dates, and one session line.
- Check failed/uncertain writes or additions preserve prior data and do not produce false save claims or duplicate cards.
- Run `make test`, `make coverage`, `make check`, and `git diff --check`; maintain 100% Python coverage.
- No automated skill-Markdown tests per SPEC.md. No agent-session/timing harness exists; live simulation, answer timing, scoring, confirmations, and logs cannot be exercised by repository end-to-end tests. Existing CLI tests cover card addition, not skill confirmation.

## Not Now
- US-12 clerk and US-13 diagnostician; other learning roles.
- Automated message interception or hard timeout enforcement, audio/video analysis, fixed global scoring scales, goal/map updates, stored transcripts, new Python behavior, and agent-session test infrastructure.

## Done When
- The portable skill applies the supplied scenario, difficulty, and time limit to each prompt, challenges vague answers during the simulation, and does not supply model answers before attempts.
- Timing uses an agreed real measurement method; learner-reported or unavailable timing is identified rather than fabricated or silently treated as compliant.
- Final scoring uses applicable sources, supported weak answers are captured automatically, and exactly one session line records score and timing limitations; no sources means explicitly ungraded rather than invented scores.
- Cards require explicit confirmation through the existing CLI; instruction review and existing automated checks pass.

## Completion Summary
- Added the portable sparring-partner skill: agreed scenario, counterpart, difficulty, finite endpoint, and per-answer time limit, with one prompt at a time and in-character pushback on vague answers.
- Timing uses a learner-operated timer or reliable message timestamps; exact-limit, late, partial, and unavailable-timing cases are explicit, without fabricated elapsed times or false hard-timeout claims.
- Final score uses applicable sources and separates timing compliance and provenance; missing sources produce an explicitly ungraded simulation rather than invented correctness scores.
- Supported weak answers are captured automatically, confirmed cards use the existing CLI, and exactly one session line records score, difficulty, time limit, timing provenance, and limitations.
- Instruction review covered US-11 and the listed contracts, including invalid limits/elapsed reports, unverified timing, source gaps, endpoint/interruption behavior, safe paths, and failed or uncertain persistence.
- `make test`, `make coverage`, and `make check` passed: 48 existing tests, formatting, lint, and 100% Python statement/branch coverage (unchanged). `git diff --check` passed.
- No live timed learner simulation or automated agent-session end-to-end test was run; timing, pushback, scoring, confirmation, and log behavior were reviewed as instructions.

## Next Slice Recommendation
- `US-12 Organise notes with the clerk`. Keep US-13 Diagnose recurring mistakes in view for stored session/mistake handling, but outside that slice.
