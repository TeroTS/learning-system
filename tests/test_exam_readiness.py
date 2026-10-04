"""Instruction-contract checks, not behavioral tests of an agent following the skills."""

import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / ".agents" / "skills"


class ExamReadinessTest(unittest.TestCase):
    def test_all_exam_entry_points_require_coverage_evidence(self) -> None:
        for skill in ("explainer", "socratic-questioner", "examiner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                for requirement in (
                    "## Check exam readiness",
                    "Compare the selected topic's sticking points in `map.md` with concrete learner production",
                    "Sticking points are a minimum checklist, not an exhaustive topic specification.",
                    "Missing or vague evidence means coverage is unknown, not complete.",
                    "A single correction or successful redo does not establish whole-topic readiness.",
                    "If any required concept is uncovered, unresolved, or unknown, do not propose or start",
                ):
                    self.assertIn(requirement, text)

    def test_diagnostic_exception_requires_informed_request(self) -> None:
        for skill in ("explainer", "socratic-questioner", "examiner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                for requirement in (
                    "An early diagnostic exam is allowed only when explicitly requested by the learner.",
                    "Disclose the uncovered or unknown concepts and that this exam can set the topic to",
                    "A bare `ok` to a premature exam offer is not an informed diagnostic request.",
                    "Do not silently shrink the exam target to the concepts already covered.",
                ):
                    self.assertIn(requirement, text)

    def test_learning_sessions_record_specific_concepts_and_outcomes(self) -> None:
        for skill in ("explainer", "socratic-questioner"):
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                self.assertIn("Name the specific concepts attempted and their outcomes", text)
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


if __name__ == "__main__":
    unittest.main()
