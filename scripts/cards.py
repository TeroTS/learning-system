# Add, list due, and grade cards in an existing subject's UTF-8 JSON store using Leitner scheduling.
# CLI output is JSON on stdout; invalid input or storage failures leave existing cards unchanged.

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

if __package__:
    from .logging_setup import configure_logging
else:
    from logging_setup import configure_logging

SUBJECT_PATTERN = r"[a-z0-9]+(-[a-z0-9]+)*"
CARD_FIELDS = {"id", "front", "back", "box", "due", "created"}
BOX_INTERVALS = (1, 3, 7, 14, 30)


# Parse a strict ISO calendar date from CLI or stored data; invalid input raises a content-free ValueError.
def parse_date(value: str) -> date:
    if not isinstance(value, str) or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
        raise ValueError("Dates must use YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Invalid calendar date.") from exc


# Read and validate all card fields and unique ids; a missing file returns [], invalid data raises ValueError.
# Never repairs stored data or includes learner content in failure messages.
def load_cards(path: Path) -> list[dict[str, str | int]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("Invalid cards.json encoding or JSON.") from exc
    if not isinstance(data, list):
        raise ValueError("cards.json must contain an array of cards.")
    ids = set()
    for card in data:
        if not isinstance(card, dict) or set(card) != CARD_FIELDS:
            raise ValueError("Invalid card fields in cards.json.")
        if type(card["id"]) is not int or card["id"] < 1 or card["id"] in ids:
            raise ValueError("Card ids must be unique positive integers.")
        ids.add(card["id"])
        if type(card["box"]) is not int or not 1 <= card["box"] <= 5:
            raise ValueError("Card boxes must be integers from 1 to 5.")
        for field in ("front", "back"):
            if not isinstance(card[field], str) or not card[field].strip():
                raise ValueError("Card fronts and backs must be non-empty strings.")
        parse_date(card["due"])
        parse_date(card["created"])
    return data


# Write cards through a same-folder temporary file and atomic replacement; propagate filesystem errors.
# Remove the temporary file on success or failure, leaving the original untouched if replacement fails.
def write_cards(path: Path, cards: list[dict[str, str | int]]) -> None:
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=".cards-", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(cards, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


# Resolve card storage inside an existing subject folder; reject invalid names, escaped paths and symlinked files.
# Return the validated path without creating or changing files; invalid paths raise ValueError.
def cards_path(subjects_dir: Path, subject: str) -> Path:
    if re.fullmatch(SUBJECT_PATTERN, subject) is None:
        raise ValueError("Invalid subject name; use lowercase hyphenated names.")
    subject_dir = subjects_dir / subject
    if not subject_dir.is_dir() or subject_dir.resolve().parent != subjects_dir.resolve():
        raise ValueError("Subject folder must already exist inside the subjects directory.")
    path = subject_dir / "cards.json"
    if path.is_symlink():
        raise ValueError("cards.json must not be a symlink.")
    return path


# Validate subject and card text, then append a box-1 card due tomorrow and return it.
# Read all existing cards before writing, preserving existing data on input or storage failures.
# ponytail: single-writer local store; add per-subject locking if concurrent writers are required.
def add_card(subjects_dir: Path, subject: str, front: str, back: str, today: date) -> dict[str, str | int]:
    path = cards_path(subjects_dir, subject)
    front, back = front.strip(), back.strip()
    if not front or not back:
        raise ValueError("Card front and back must not be empty.")
    cards = load_cards(path)
    card = {
        "id": max((existing["id"] for existing in cards), default=0) + 1,
        "front": front,
        "back": back,
        "box": 1,
        "due": (today + timedelta(days=1)).isoformat(),
        "created": today.isoformat(),
    }
    cards.append(card)
    write_cards(path, sorted(cards, key=lambda item: item["id"]))
    return card


# Return validated cards due on or before today, sorted by due date then id; missing storage returns [].
# Read-only: never creates or changes files; propagate validation and read failures.
def due_cards(subjects_dir: Path, subject: str, today: date) -> list[dict[str, str | int]]:
    cards = load_cards(cards_path(subjects_dir, subject))
    return sorted(
        (card for card in cards if card["due"] <= today.isoformat()), key=lambda card: (card["due"], card["id"])
    )


# Apply a validated right/wrong result to one card: promote with a box-5 cap or reset to box 1.
# Schedule from today using the new box's interval, write atomically in id order, and return the updated card.
# Unknown ids raise ValueError; validation, date overflow and storage failures leave the persisted cards unchanged.
def grade_card(subjects_dir: Path, subject: str, card_id: int, result: str, today: date) -> dict[str, str | int]:
    path = cards_path(subjects_dir, subject)
    cards = load_cards(path)
    for card in cards:
        if card["id"] == card_id:
            card["box"] = min(card["box"] + 1, 5) if result == "right" else 1
            card["due"] = (today + timedelta(days=BOX_INTERVALS[card["box"] - 1])).isoformat()
            write_cards(path, sorted(cards, key=lambda item: item["id"]))
            return card
    raise ValueError("Unknown card id.")


# Parse add/due/grade CLI arguments, configure stderr logging once, and print the result as JSON.
# Return 0 on success or 1 for input/data/storage failures; argparse exits 2 for bad usage.
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage subject cards.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    add = subcommands.add_parser("add", help="Add a confirmed card.")
    add.add_argument("--front", required=True)
    add.add_argument("--back", required=True)
    due = subcommands.add_parser("due", help="List due cards without changing storage.")
    grade = subcommands.add_parser("grade", help="Record a right or wrong recall result.")
    grade.add_argument("--result", choices=("right", "wrong"), required=True)
    for command in (add, due, grade):
        command.add_argument("subject")
        command.add_argument("--today", help="Local calendar date (YYYY-MM-DD).")
        command.add_argument("--subjects-dir", type=Path, default=Path(__file__).resolve().parents[1] / "subjects")
    grade.add_argument("id", type=int)
    args = parser.parse_args(argv)
    try:
        configure_logging()
        today = parse_date(args.today) if args.today is not None else date.today()
        if args.command == "add":
            result = add_card(args.subjects_dir, args.subject, args.front, args.back, today)
        elif args.command == "due":
            result = due_cards(args.subjects_dir, args.subject, today)
        else:
            result = grade_card(args.subjects_dir, args.subject, args.id, args.result, today)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, OverflowError):
        print("Cannot manage cards: storage failure or date outside the supported range.", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
