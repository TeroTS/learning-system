"""Instruction-contract checks, not behavioral tests of an agent following the skills."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


class ExamReadinessTest(unittest.TestCase):
    def test_all_exam_entry_points_use_the_same_fixed_gate(self) -> None:
        for skill in ("explainer", "socratic-questioner", "examiner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                for requirement in (
                    "## Check exam readiness",
                    "Read `docs/contracts.md` Contracts 4 and 6 and `Progression gate`",
                    "before offering continuation, an exam or the next topic",
                    "Do not infer additional required concepts from goals, sources or sticking points.",
                    "Readiness checks never change map status.",
                ):
                    self.assertIn(requirement, text)
                self.assertNotIn("minimum checklist", text)
                self.assertNotIn("Use the goal and applicable sources to establish the goal-relevant scope", text)

    def test_fixed_scope_and_evidence_contract(self) -> None:
        text = " ".join((ROOT / "docs/contracts.md").read_text(encoding="utf-8").split())
        for requirement in (
            "### Requirements: <topic>",
            "Scope: accepted",
            "Passing target:",
            "new requirement ID",
            "resolved, unresolved or unknown",
            "latest substantive applicable outcome in append order",
            "An interruption without production does not erase earlier evidence.",
            "Cite the session path and line number",
            "aided production establishes coverage, not unaided mastery",
            "Legacy evidence counts only when",
            "readiness checks never write",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_progression_covers_every_state_and_override(self) -> None:
        text = " ".join((ROOT / "docs/contracts.md").read_text(encoding="utf-8").split())
        for requirement in (
            "## Progression gate",
            "Missing, malformed or unaccepted scope/target",
            "Required dependency not passed",
            "Unknown or unresolved requirement",
            "Every requirement resolved; topic not passed or re-exam requested",
            "Topic passed",
            "Every topic passed",
            "first such requirement in accepted checklist order",
            "first unpassed, dependency-ready topic in map order",
            "A skip never marks a topic passed or satisfies a dependency.",
            "Explicit topic selection does not itself authorize bypassing the gate.",
            "No accepted target means no diagnostic exam.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_progression_table_order_is_fixed(self) -> None:
        text = (ROOT / "docs/contracts.md").read_text(encoding="utf-8").split("## Progression gate", maxsplit=1)[1]
        states = (
            "| Missing, malformed or unaccepted scope/target |",
            "| Required dependency not passed |",
            "| Unknown or unresolved requirement |",
            "| Every requirement resolved; topic not passed or re-exam requested |",
            "| Topic passed; unpassed topics remain |",
            "| Every topic passed |",
        )
        positions = [text.index(state) for state in states]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("take the first", text)
        self.assertIn("matching row below", text)

    def test_general_continuation_is_gated_before_role_selection(self) -> None:
        text = " ".join((ROOT / "AGENTS.md").read_text(encoding="utf-8").split())
        self.assertIn("## Learning progression", text)
        self.assertIn("before choosing a role or offering the next topic", text)
        self.assertIn("Read `docs/contracts.md`", text)
        self.assertIn("Do not silently switch roles", text)

    def test_diagnostic_exception_requires_informed_request(self) -> None:
        for skill in ("explainer", "socratic-questioner", "examiner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                for requirement in (
                    "An early diagnostic exam is allowed only when explicitly requested by the learner.",
                    "Disclose the uncovered or unknown concepts and that this exam can set the topic to",
                    "A bare `ok` to a premature exam offer is not an informed diagnostic request.",
                    "Do not silently shrink the exam target to the concepts already covered.",
                    "No accepted target means no diagnostic exam.",
                ):
                    self.assertIn(requirement, text)

    def test_learning_sessions_record_requirement_evidence(self) -> None:
        for skill in ("explainer", "socratic-questioner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                self.assertIn("Name the specific concepts attempted and their outcomes", text)
                self.assertIn("requirement IDs", text)
                self.assertIn("resolved, unresolved or unknown", text)
                self.assertIn("Do not rewrite historical session lines", text)

    def test_handoffs_and_exam_start_use_the_readiness_gate(self) -> None:
        for skill in ("explainer", "socratic-questioner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                handoff = text.split("## Offer an exam handoff", maxsplit=1)[1]
                self.assertIn("Apply `Check exam readiness` before offering an `examiner` session", handoff)
                self.assertNotIn("then offer an", handoff)
        examiner = " ".join((SKILLS / "examiner" / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn("Apply `Check exam readiness` independently before the first question", examiner)
        self.assertIn("Use the accepted passing target in `map.md`", examiner)
        self.assertIn("Do not add requirements or change passing criteria during the exam.", examiner)
        self.assertNotIn("can still proceed on the clearly identified topic", examiner)

    def test_mapmaker_supports_approved_scope_amendments(self) -> None:
        text = " ".join((SKILLS / "mapmaker" / "SKILL.md").read_text(encoding="utf-8").split())
        for requirement in (
            "## Amend scope without replacing the map",
            "finite checklist",
            "observable success criteria",
            "passing target",
            "wait for explicit acceptance before writing",
            "preserve unaffected statuses",
            "new requirement ID",
            "reset the affected passed topic to `todo`",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_exam_questions_require_transfer_not_repetition(self) -> None:
        text = " ".join((SKILLS / "examiner" / "SKILL.md").read_text(encoding="utf-8").split())
        for requirement in (
            "## Choose fresh exam tasks",
            "Compare proposed tasks with learning and previous exam examples",
            "current conversation and `sessions.md` task summaries",
            "Do not reuse learning examples as scored exam questions.",
            "Renaming identifiers or swapping values alone is not sufficient.",
            "Change the reasoning task",
            "Standard syntax intrinsic to the concept may recur",
            "freshness unverified",
            "Repeated examples do not count as transfer evidence.",
            "withdraw it unscored",
            "Do not retroactively rewrite historical grades",
            "without adding requirements, unlearned concepts or difficulty beyond the accepted target.",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)
        self.assertIn("## Choose fresh exam tasks", text)
        self.assertLess(text.index("## Choose fresh exam tasks"), text.index("## Ask until the first failure or guess"))

    def test_learning_handoffs_preserve_evidence_not_exam_examples(self) -> None:
        for skill in ("explainer", "socratic-questioner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                handoff = text.split("## Offer an exam handoff", maxsplit=1)[1]
                self.assertIn("Do not reuse learning examples as scored exam questions.", handoff)
                self.assertIn("short task context", text)
                self.assertIn("not full questions, solutions or transcripts", text)
        explainer = (SKILLS / "explainer" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("redo the **entire task from the beginning**", explainer)

    def test_authoritative_docs_do_not_expand_scope_at_runtime(self) -> None:
        for path in ("DECISIONS.md", "SPEC.md", "docs/contracts.md"):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertNotIn("minimum checklist", text)
                self.assertIn("learner-approved", text)
                self.assertIn("docs/contracts.md", text)


if __name__ == "__main__":
    unittest.main()
