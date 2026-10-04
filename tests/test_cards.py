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


class CardsTestCase(unittest.TestCase):
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
            try:
                code = cards.main(arguments)
            except SystemExit as exc:
                code = exc.code
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


class AddCardTest(CardsTestCase):
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
        for arguments in ([], ["add", "statistics"], ["unknown", "statistics"], [*self.arguments(), "--unexpected"]):
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


class DueCardTest(CardsTestCase):
    def arguments(self, **overrides: str) -> list[str]:
        options = {"today": "2025-10-04"}
        options.update(overrides)
        return [
            "due",
            "statistics",
            "--subjects-dir",
            str(self.subjects),
            *[argument for name, value in options.items() for argument in (f"--{name}", value)],
        ]

    def test_lists_overdue_and_today_cards_sorted_by_due_then_numeric_id(self) -> None:
        stored = [
            {**self.original_card, "id": 10, "due": "2025-10-04"},
            {**self.original_card, "id": 4, "due": "2025-10-05"},
            {**self.original_card, "id": 2, "due": "2025-10-04"},
            self.original_card,
        ]
        self.path.write_text(json.dumps(stored), encoding="utf-8")
        before = self.path.read_bytes()
        first = self.invoke(self.arguments())
        second = self.invoke(self.arguments())
        self.assertEqual(first, second)
        code, stdout, stderr = first
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout), [stored[3], stored[2], stored[0]])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.subject.iterdir()), [self.path])

    def test_missing_empty_and_future_only_storage_list_no_cards(self) -> None:
        for stored in (None, [], [{**self.original_card, "due": "2025-10-05"}]):
            with self.subTest(stored=stored):
                if stored is not None:
                    self.path.write_text(json.dumps(stored), encoding="utf-8")
                before = self.path.read_bytes() if self.path.exists() else None
                code, stdout, stderr = self.invoke(self.arguments())
                self.assertEqual((code, stdout, stderr), (0, "[]\n", ""))
                self.assertEqual(self.path.read_bytes() if self.path.exists() else None, before)
                self.assertEqual(list(self.subject.iterdir()), [] if stored is None else [self.path])

    def test_default_date_is_local_today(self) -> None:
        yesterday = date.today() - timedelta(days=1)
        stored = [{**self.original_card, "due": yesterday.isoformat()}]
        self.path.write_text(json.dumps(stored), encoding="utf-8")
        code, stdout, stderr = self.invoke(self.arguments()[:-2])
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout), stored)

    def test_maximum_date_is_valid_for_read_only_listing(self) -> None:
        stored = [{**self.original_card, "due": "9999-12-31"}]
        self.path.write_text(json.dumps(stored), encoding="utf-8")
        code, stdout, stderr = self.invoke(self.arguments(today="9999-12-31"))
        self.assertEqual((code, stderr), (0, ""))
        self.assertEqual(json.loads(stdout), stored)

    def test_invalid_subject_or_date_is_rejected_without_creating_storage(self) -> None:
        for subject in ("../statistics", "Statistics", "missing"):
            with self.subTest(subject=subject):
                arguments = self.arguments()
                arguments[1] = subject
                self.assert_rejected(arguments)
        for today in ("20251004", "2025-02-29", "2025-W40-6"):
            with self.subTest(today=today):
                self.assert_rejected(self.arguments(today=today))
        self.assertFalse(self.path.exists())

    def test_invalid_storage_and_invalid_future_cards_are_rejected_without_repair(self) -> None:
        invalid = [
            b"not JSON Original front",
            b"\xff",
            b"{}",
            json.dumps([{**self.original_card, "due": "2025-10-05", "box": 6}]).encode(),
            json.dumps([self.original_card, {**self.original_card, "due": "2025-10-05"}]).encode(),
        ]
        for content in invalid:
            with self.subTest(content=content):
                self.path.write_bytes(content)
                self.assert_rejected(self.arguments())

    def test_subject_escape_and_storage_symlink_are_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.subjects / "escape").symlink_to(outside, target_is_directory=True)
        arguments = self.arguments()
        arguments[1] = "escape"
        self.assert_rejected(arguments)
        outside_cards = outside / "cards.json"
        outside_cards.write_text("[]", encoding="utf-8")
        self.path.symlink_to(outside_cards)
        self.assert_rejected(self.arguments())
        self.assertEqual(outside_cards.read_text(encoding="utf-8"), "[]")

    def test_end_to_end_listing_is_deterministic_and_read_only(self) -> None:
        stored = [
            {**self.original_card, "id": 2, "due": "2025-10-04"},
            {**self.original_card, "id": 1, "due": "2025-10-05"},
            self.original_card,
        ]
        self.path.write_text(json.dumps(stored), encoding="utf-8")
        before = self.path.read_bytes()
        command = [sys.executable, str(SCRIPT), *self.arguments()]
        first = subprocess.run(command, capture_output=True, text=True, cwd=self.temp.name)
        second = subprocess.run(command, capture_output=True, text=True, cwd=self.temp.name)
        self.assertEqual((first.returncode, first.stderr), (0, ""))
        self.assertEqual((second.returncode, second.stderr), (0, ""))
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout), [stored[2], stored[0]])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.subject.iterdir()), [self.path])

    def test_end_to_end_missing_file_and_invalid_data(self) -> None:
        command = [sys.executable, str(SCRIPT), *self.arguments()]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "[]\n", ""))
        self.assertFalse(self.path.exists())
        original = b"not JSON: private learner content"
        self.path.write_bytes(original)
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("private learner content", result.stderr)
        self.assertEqual(self.path.read_bytes(), original)

    def test_bad_usage_exits_two(self) -> None:
        for arguments in (["due"], [*self.arguments(), "--front", "not accepted"]):
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.strip())
        self.assertFalse(self.path.exists())


class GradeCardTest(CardsTestCase):
    def arguments(self, **overrides: str) -> list[str]:
        options = {"result": "right", "today": "2025-10-04"}
        options.update(overrides)
        return [
            "grade",
            "statistics",
            "3",
            "--subjects-dir",
            str(self.subjects),
            *[argument for name, value in options.items() for argument in (f"--{name}", value)],
        ]

    def test_every_right_and_wrong_transition_uses_new_box_interval(self) -> None:
        for result, transitions in {
            "right": [(1, 2, 3), (2, 3, 7), (3, 4, 14), (4, 5, 30), (5, 5, 30)],
            "wrong": [(box, 1, 1) for box in range(1, 6)],
        }.items():
            for old_box, new_box, interval in transitions:
                with self.subTest(result=result, old_box=old_box):
                    original = {**self.original_card, "box": old_box}
                    unrelated = {**self.original_card, "id": 1}
                    self.path.write_text(json.dumps([original, unrelated]), encoding="utf-8")
                    code, stdout, stderr = self.invoke(self.arguments(result=result))
                    self.assertEqual((code, stderr), (0, ""))
                    expected = {
                        **original,
                        "box": new_box,
                        "due": (date(2025, 10, 4) + timedelta(days=interval)).isoformat(),
                    }
                    self.assertEqual(json.loads(stdout), expected)
                    self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [unrelated, expected])
                    self.assertEqual(list(self.subject.iterdir()), [self.path])

    def test_scheduling_uses_grading_date_not_old_due_date(self) -> None:
        for old_due in ("2020-01-01", "2030-01-01"):
            with self.subTest(old_due=old_due):
                self.path.write_text(json.dumps([{**self.original_card, "due": old_due}]), encoding="utf-8")
                code, stdout, stderr = self.invoke(self.arguments())
                self.assertEqual((code, stderr), (0, ""))
                self.assertEqual(json.loads(stdout)["due"], "2025-11-03")

    def test_scheduling_crosses_calendar_boundaries(self) -> None:
        for today, due in [("2024-02-28", "2024-02-29"), ("2024-02-29", "2024-03-01"), ("2025-12-31", "2026-01-01")]:
            with self.subTest(today=today):
                self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
                code, stdout, stderr = self.invoke(self.arguments(result="wrong", today=today))
                self.assertEqual((code, stderr), (0, ""))
                self.assertEqual(json.loads(stdout)["due"], due)

    def test_default_date_is_local_today(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        before = date.today()
        code, stdout, stderr = self.invoke(self.arguments()[:-2])
        after = date.today()
        self.assertEqual((code, stderr), (0, ""))
        self.assertIn(json.loads(stdout)["due"], ((day + timedelta(days=30)).isoformat() for day in (before, after)))

    def test_unknown_ids_preserve_storage_including_missing_file(self) -> None:
        self.assert_rejected(self.arguments())
        for stored in ([], [self.original_card]):
            self.path.write_text(json.dumps(stored), encoding="utf-8")
            for card_id in ("1", "0", "-1", "99"):
                with self.subTest(stored=stored, card_id=card_id):
                    arguments = self.arguments()
                    arguments[2] = card_id
                    self.assert_rejected(arguments)

    def test_invalid_subject_date_or_data_preserves_storage(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        for subject in ("../statistics", "Statistics", "missing"):
            with self.subTest(subject=subject):
                arguments = self.arguments()
                arguments[1] = subject
                self.assert_rejected(arguments)
        for today in ("20251004", "2025-02-29", "2025-W40-6", "9999-12-31"):
            with self.subTest(today=today):
                self.assert_rejected(self.arguments(today=today))
        for content in (
            b"not JSON Original front",
            b"\xff",
            b"{}",
            json.dumps([self.original_card, {**self.original_card, "id": 1, "box": 6}]).encode(),
        ):
            with self.subTest(content=content):
                self.path.write_bytes(content)
                self.assert_rejected(self.arguments())

    def test_grade_rejects_storage_symlink(self) -> None:
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text(json.dumps([self.original_card]), encoding="utf-8")
        before = outside.read_bytes()
        self.path.symlink_to(outside)
        self.assert_rejected(self.arguments())
        self.assertEqual(outside.read_bytes(), before)

    def test_atomic_write_failure_preserves_cards_and_cleans_temporary_file(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        with mock.patch("os.replace", side_effect=OSError("simulated replacement failure")):
            self.assert_rejected(self.arguments())

    def test_grade_is_not_idempotent(self) -> None:
        self.path.write_text(json.dumps([{**self.original_card, "box": 1}]), encoding="utf-8")
        first = self.invoke(self.arguments())
        second = self.invoke(self.arguments())
        self.assertEqual((first[0], first[2], second[0], second[2]), (0, "", 0, ""))
        self.assertEqual((json.loads(first[1])["box"], json.loads(second[1])["box"]), (2, 3))
        self.assertEqual(json.loads(second[1])["due"], "2025-10-11")

    def test_bad_usage_exits_two_without_writing(self) -> None:
        invalid_id = self.arguments()
        invalid_id[2] = "not-an-id"
        for arguments in (["grade", "statistics"], invalid_id, self.arguments(result="maybe")):
            with self.subTest(arguments=arguments):
                result = subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.strip())
        self.assertFalse(self.path.exists())

    def test_end_to_end_due_grade_and_rescheduled_due_list(self) -> None:
        stored = [self.original_card, {**self.original_card, "id": 1, "box": 1}]
        self.path.write_text(json.dumps(stored), encoding="utf-8")
        due_command = [
            sys.executable,
            str(SCRIPT),
            "due",
            "statistics",
            "--subjects-dir",
            str(self.subjects),
            "--today",
            "2025-10-04",
        ]
        initial = subprocess.run(due_command, capture_output=True, text=True, cwd=self.temp.name)
        self.assertEqual((initial.returncode, initial.stderr), (0, ""))
        self.assertEqual([card["id"] for card in json.loads(initial.stdout)], [1, 3])
        for card_id, result, box, due in [("1", "right", 2, "2025-10-07"), ("3", "wrong", 1, "2025-10-05")]:
            arguments = self.arguments(result=result)
            arguments[2] = card_id
            graded = subprocess.run(
                [sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True, cwd=self.temp.name
            )
            self.assertEqual((graded.returncode, graded.stderr), (0, ""))
            card = json.loads(graded.stdout)
            self.assertEqual((card["id"], card["box"], card["due"]), (int(card_id), box, due))
        after = subprocess.run(due_command, capture_output=True, text=True, cwd=self.temp.name)
        self.assertEqual((after.returncode, after.stdout, after.stderr), (0, "[]\n", ""))
        due_command[-1] = "2025-10-05"
        next_day = subprocess.run(due_command, capture_output=True, text=True, cwd=self.temp.name)
        self.assertEqual((next_day.returncode, next_day.stderr), (0, ""))
        self.assertEqual([card["id"] for card in json.loads(next_day.stdout)], [3])
        self.assertEqual(list(self.subject.iterdir()), [self.path])

    def test_end_to_end_unknown_card_preserves_bytes(self) -> None:
        self.path.write_text(json.dumps([self.original_card]), encoding="utf-8")
        before = self.path.read_bytes()
        arguments = self.arguments()
        arguments[2] = "99"
        result = subprocess.run([sys.executable, str(SCRIPT), *arguments], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())
        self.assertNotIn("Original front", result.stderr)
        self.assertNotIn("Original back", result.stderr)
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
