import contextlib
import importlib
import io
import json
import logging
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "cards.py"


class AddCardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.subjects = Path(self.temp.name) / "subjects"
        self.subject = self.subjects / "statistics"
        self.subject.mkdir(parents=True)
        self.path = self.subject / "cards.json"
        self.original_card = {
            "id": 3,
            "front": "Original front",
            "back": "Original back",
            "box": 4,
            "due": "2025-10-01",
            "created": "2025-09-01",
        }
        self.addCleanup(logging.basicConfig, force=True)

    def arguments(self, **overrides: str) -> list[str]:
        options = {"front": "What is the mean?", "back": "Sum divided by count", "today": "2025-10-04"}
        options.update(overrides)
        return [
            "add",
            "statistics",
            "--subjects-dir",
            str(self.subjects),
            *[argument for name, value in options.items() for argument in (f"--{name}", value)],
        ]

    def invoke(self, arguments: list[str]) -> tuple[int, str, str]:
        self.assertTrue(SCRIPT.is_file(), "The add CLI has not been implemented")
        cards = importlib.import_module("scripts.cards")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cards.main(arguments)
        return code, stdout.getvalue(), stderr.getvalue()

    def assert_rejected(self, arguments: list[str]) -> None:
        before = self.path.read_bytes() if self.path.exists() else None
        code, stdout, stderr = self.invoke(arguments)
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertTrue(stderr.strip())
        self.assertNotIn("Original front", stderr)
        self.assertNotIn("Original back", stderr)
        self.assertNotIn("What is the mean?", stderr)
        self.assertEqual(self.path.read_bytes() if self.path.exists() else None, before)
        self.assertEqual(list(self.subject.glob("*.tmp")), [])

    def test_end_to_end_add_creates_file_and_reports_card(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *self.arguments()], capture_output=True, text=True, cwd=self.temp.name
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        card = json.loads(result.stdout)
        self.assertEqual(
            card,
            {
                "id": 1,
                "front": "What is the mean?",
                "back": "Sum divided by count",
                "box": 1,
                "due": "2025-10-05",
                "created": "2025-10-04",
            },
        )
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [card])
        self.assertEqual(list(self.subject.iterdir()), [self.path])

    def test_end_to_end_default_store_is_relative_to_script(self) -> None:
        copied_script = Path(self.temp.name) / "scripts" / "cards.py"
        copied_script.parent.mkdir()
        for name in ("cards.py", "logging_setup.py"):
            (copied_script.parent / name).write_text(
                (SCRIPT.parent / name).read_text(encoding="utf-8"), encoding="utf-8"
            )
        arguments = self.arguments()
        del arguments[2:4]
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        result = subprocess.run(
            [sys.executable, str(copied_script), *arguments], capture_output=True, text=True, cwd=elsewhere
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [json.loads(result.stdout)])
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_end_to_end_data_error_preserves_bytes_and_does_not_log_content(self) -> None:
        original = b"not JSON: private learner content"
        self.path.write_bytes(original)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *self.arguments()],
            capture_output=True,
            text=True,
            env={**os.environ, "LOG_LEVEL": "DEBUG"},
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("cards.json", result.stderr)
        self.assertNotIn("private learner content", result.stderr)
        self.assertEqual(self.path.read_bytes(), original)

    def test_add_uses_max_id_and_sorts_without_changing_existing_cards(self) -> None:
        other = {**self.original_card, "id": 1}
        self.path.write_text(json.dumps([self.original_card, other]), encoding="utf-8")
        code, stdout, stderr = self.invoke(self.arguments())
        self.assertEqual((code, stderr), (0, ""))
        created = json.loads(stdout)
        self.assertEqual(created["id"], 4)
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [other, self.original_card, created])

    def test_add_trims_text_and_preserves_unicode(self) -> None:
        code, stdout, stderr = self.invoke(self.arguments(front="  平均値?\n", back="  Keskiarvo: ää \t"))
        self.assertEqual((code, stderr), (0, ""))
        card = json.loads(stdout)
        self.assertEqual(card["front"], "平均値?")
        self.assertEqual(card["back"], "Keskiarvo: ää")
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [card])

    def test_dates_cross_leap_day_month_and_year_boundaries(self) -> None:
        for today, due in [("2024-02-28", "2024-02-29"), ("2024-02-29", "2024-03-01"), ("2025-12-31", "2026-01-01")]:
            with self.subTest(today=today):
                code, stdout, stderr = self.invoke(self.arguments(today=today))
                self.assertEqual((code, stderr), (0, ""))
                self.assertEqual(json.loads(stdout)["due"], due)
                self.assertEqual(json.loads(stdout)["created"], today)

    def test_default_date_is_local_today(self) -> None:
        arguments = self.arguments()
        arguments = arguments[:-2]
        before = date.today()
        code, stdout, stderr = self.invoke(arguments)
        after = date.today()
        self.assertEqual((code, stderr), (0, ""))
        card = json.loads(stdout)
        created = date.fromisoformat(card["created"])
        self.assertIn(created, (before, after))
        self.assertEqual(card["due"], (created + timedelta(days=1)).isoformat())

    def test_rejects_empty_text_without_creating_or_changing_storage(self) -> None:
        for existing in (False, True):
            if existing:
                self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
            for field in ("front", "back"):
                for value in ("", " \n\t"):
                    with self.subTest(existing=existing, field=field, value=value):
                        self.assert_rejected(self.arguments(**{field: value}))

    def test_rejects_invalid_subject_names(self) -> None:
        for subject in ("", "../statistics", "/tmp/statistics", "Statistics", "a_b", "-a", "a-", "a--b", "a\n"):
            with self.subTest(subject=subject):
                arguments = self.arguments()
                arguments.pop(1)
                arguments.extend(["--", subject])
                self.assert_rejected(arguments)

    def test_rejects_unknown_subject_or_file_in_place_of_folder(self) -> None:
        for subject in ("missing", "not-a-folder"):
            (self.subjects / "not-a-folder").write_text("not a folder", encoding="utf-8")
            arguments = self.arguments()
            arguments[1] = subject
            self.assert_rejected(arguments)
        self.assertFalse((self.subjects / "missing").exists())

    def test_rejects_subject_symlink_outside_store(self) -> None:
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.subjects / "escape").symlink_to(outside, target_is_directory=True)
        arguments = self.arguments()
        arguments[1] = "escape"
        self.assert_rejected(arguments)
        self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_card_storage_symlink(self) -> None:
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text("[]", encoding="utf-8")
        self.path.symlink_to(outside)
        self.assert_rejected(self.arguments())
        self.assertEqual(outside.read_text(encoding="utf-8"), "[]")

    def test_rejects_invalid_dates_and_date_overflow(self) -> None:
        for today in ("20251004", "2025-1-04", "2025-02-29", "2025-W40-6", "2025-10-04\n", "no-date", "9999-12-31"):
            with self.subTest(today=today):
                self.assert_rejected(self.arguments(today=today))

    def test_rejects_invalid_json_and_utf8_without_repair(self) -> None:
        for content in (b"not JSON Original front", b"[", b"\xff"):
            with self.subTest(content=content):
                self.path.write_bytes(content)
                self.assert_rejected(self.arguments())

    def test_rejects_invalid_card_shapes(self) -> None:
        invalid = [None, {}, "cards", [None], [[self.original_card]], [{"id": 1}]]
        for field in self.original_card:
            incomplete = dict(self.original_card)
            del incomplete[field]
            invalid.append([incomplete])
        for field, values in {
            "id": [0, -1, True, 1.5, "1"],
            "front": ["", " \t", 1, None],
            "back": ["", " \t", 1, None],
            "box": [0, 6, True, 1.5, "1"],
            "due": ["20251004", "2025-02-29", None, 1],
            "created": ["2025-W40-6", "2025-02-29", None, 1],
        }.items():
            invalid.extend([[{**self.original_card, field: value}] for value in values])
        invalid.extend([[self.original_card, self.original_card], [{**self.original_card, "extra": "unexpected"}]])
        for data in invalid:
            with self.subTest(data=data):
                self.path.write_text(json.dumps(data), encoding="utf-8")
                self.assert_rejected(self.arguments())

    def test_read_failure_does_not_change_storage(self) -> None:
        self.path.mkdir()
        code, stdout, stderr = self.invoke(self.arguments())
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertTrue(stderr.strip())
        self.assertTrue(self.path.is_dir())

    def test_atomic_replace_failure_preserves_original_and_cleans_temp(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        with mock.patch("os.replace", side_effect=OSError("simulated replacement failure")):
            self.assert_rejected(self.arguments())

    def test_temporary_write_failure_preserves_original_and_cleans_temp(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        with mock.patch("json.dump", side_effect=OSError("simulated write failure")):
            self.assert_rejected(self.arguments())

    def test_temporary_file_creation_failure_preserves_original(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        with mock.patch("tempfile.NamedTemporaryFile", side_effect=OSError("simulated creation failure")):
            self.assert_rejected(self.arguments())

    def test_bad_usage_exits_two_without_writing(self) -> None:
        for arguments in ([], ["add", "statistics"], ["due", "statistics"], [*self.arguments(), "--unexpected"]):
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.strip())
        self.assertFalse(self.path.exists())

    def test_invalid_logging_configuration_does_not_write(self) -> None:
        with mock.patch.dict(os.environ, {"LOG_LEVEL": "invalid"}):
            self.assert_rejected(self.arguments())

    def test_script_entry_point(self) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(sys, "argv", [str(SCRIPT), *self.arguments()]),
            mock.patch.object(sys, "path", [str(REPO_ROOT / "scripts"), *sys.path]),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit) as raised,
        ):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(raised.exception.code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [json.loads(stdout.getvalue())])


if __name__ == "__main__":
    unittest.main()
