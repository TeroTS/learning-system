"""Instruction-contract checks; these do not prove agent compliance or answer correctness."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
GRADING_SKILLS = (
    "interviewer",
    "mapmaker",
    "explainer",
    "socratic-questioner",
    "examiner",
    "checker",
    "listener",
    "review",
    "sparring-partner",
)


class AgentJudgementTest(unittest.TestCase):
    def test_every_grading_skill_uses_universal_judgement_with_safeguards(self) -> None:
        for skill in GRADING_SKILLS:
            with self.subTest(skill=skill):
                text = " ".join((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").split())
                for required in (
                    "Read `docs/contracts.md` Contract 9.",
                    "Always grade by agent judgement",
                    "accepted requirements and passing targets",
                    "Genuine grading uncertainty stays `unverified`, not a learner mistake or failure.",
                    "Identify agent judgement in feedback",
                    "`graded: agent judgement` in the session result",
                    "Preserve historical evidence and its attribution.",
                ):
                    self.assertIn(required, text)
                for obsolete in (
                    r"sources?.{0,25}(?:take|takes|always takes) precedence",
                    r"no applicable source",
                    r"(?:when|if) no source applies",
                    r"source-(?:supported|backed|based)",
                    r"(?:against|by|from) (?:the )?applicable sources?",
                    r"supported by a source",
                ):
                    self.assertNotRegex(text.lower(), obsolete)

    def test_uncertainty_does_not_change_card_schedule_or_exam_status(self) -> None:
        review = " ".join((SKILLS / "review" / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn("If grading is uncertain or the stored back is incorrect, leave the card ungraded.", review)
        self.assertIn("Do not call `grade` or log a learner mistake for that card.", review)
        examiner = " ".join((SKILLS / "examiner" / "SKILL.md").read_text(encoding="utf-8").split())
        self.assertIn("If grading is genuinely uncertain, stop as inconclusive", examiner)
        self.assertIn("Grading uncertainty or interrupted exam: leave its status unchanged.", examiner)

    def test_non_grading_roles_keep_their_evidence_boundaries(self) -> None:
        clerk = (SKILLS / "clerk" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not label the learner's notes correct, grade them, or create mistake records.", clerk)
        diagnostician = (SKILLS / "diagnostician" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("not permission to independently regrade unseen", diagnostician)
        self.assertIn("unverified entries into verified facts", diagnostician)

    def test_public_guidance_matches_the_assessment_contract(self) -> None:
        for path in ("README.md", "CONTEXT.md", "docs/contracts.md"):
            with self.subTest(path=path):
                text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
                self.assertIn("agent judgement", text)
                self.assertNotRegex(
                    text,
                    re.compile(
                        r"(?:only basis for grading|take precedence for correctness grading|no applicable source)", re.I
                    ),
                )


if __name__ == "__main__":
    unittest.main()
