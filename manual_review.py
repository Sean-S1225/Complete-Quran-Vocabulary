import json
import os
import sys
from pathlib import Path

import pandas as pd


CSV_PATH = Path("manual_lexeme_review.csv")

MANUAL_FIELDS = [
    "Manual Headword",
    "Manual Plural",
    "Manual Definition",
    "Manual Notes",
]

DISPLAY_FIELDS = [
    ("QAC Lemma", "QAC lemma"),
    ("QuranMorphLemmaAlternatives", "QuranMorph lemmas"),
    ("QuranMorphMatchForms", "QuranMorph match forms"),
    ("CAMeL Headwords", "CAMeL headwords"),
    ("POS", "QAC POS"),
    ("QuranMorphPOS", "QuranMorph POS"),
    ("Root", "Root"),
    ("IsParticiple", "Participle"),
    ("ParticipleType", "Participle type"),
    ("Frequency", "Frequency"),
    ("ObservedForms", "Observed forms"),
    ("English Glosses", "Quran Foundation glosses"),
    ("Definition Evidence", "Definition evidence"),
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def is_blank(value):
    if pd.isna(value):
        return True

    if isinstance(value, str):
        return value.strip() == ""

    return False


def is_reviewed(value):
    if isinstance(value, bool):
        return value

    if pd.isna(value):
        return False

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def pretty_value(value):
    """
    Pretty-print values that were JSON-serialized when the
    manual-review CSV was created.
    """
    if is_blank(value):
        return "—"

    if not isinstance(value, str):
        return str(value)

    text = value.strip()

    # Try to decode list/dict fields from JSON.
    if text.startswith("[") or text.startswith("{"):
        try:
            parsed = json.loads(text)

            if isinstance(parsed, list):
                if not parsed:
                    return "—"

                return " | ".join(
                    str(item)
                    for item in parsed
                )

            if isinstance(parsed, dict):
                if not parsed:
                    return "—"

                # Sort Counter-like dictionaries by frequency.
                try:
                    items = sorted(
                        parsed.items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                except TypeError:
                    items = parsed.items()

                return "\n".join(
                    f"    {key}: {value}"
                    for key, value in items
                )

        except json.JSONDecodeError:
            pass

    return text


def save_csv(df):
    """
    Save after every completed lexeme.

    Write to a temporary file first so an interrupted write
    is less likely to damage the working CSV.
    """
    temporary_path = CSV_PATH.with_suffix(".tmp.csv")

    df.to_csv(
        temporary_path,
        index=False,
        encoding="utf-8-sig",
    )

    temporary_path.replace(CSV_PATH)


def show_row(row, position, total):
    clear_screen()

    print("=" * 72)
    print(f"QUR'AN VOCABULARY MANUAL REVIEW    {position}/{total}")
    print("=" * 72)
    print()

    print(f"Vocabulary ID: {row['Vocabulary ID']}")
    print()

    for column, label in DISPLAY_FIELDS:
        if column not in row.index:
            continue

        value = pretty_value(row[column])

        print(f"{label}:")
        print(f"  {value}")
        print()

    print("-" * 72)
    print("MANUAL ENTRY")
    print("-" * 72)
    print()


def prompt_field(label, current_value):
    """
    Blank Enter keeps an existing value.

    If the field is currently empty, blank Enter leaves it empty.
    """
    existing = (
        ""
        if is_blank(current_value)
        else str(current_value)
    )

    if existing:
        prompt = f"{label} [{existing}]: "
    else:
        prompt = f"{label}: "

    entered = input(prompt).strip()

    if not entered:
        return existing

    return entered


def main():
    if not CSV_PATH.exists():
        print(
            f"Could not find {CSV_PATH.resolve()}"
        )
        sys.exit(1)

    df = pd.read_csv(
        CSV_PATH,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    required_columns = {
        "Vocabulary ID",
        "Reviewed",
        *MANUAL_FIELDS,
    }

    missing = required_columns - set(df.columns)

    if missing:
        print(
            "CSV is missing required columns:"
        )

        for column in sorted(missing):
            print(f"  - {column}")

        sys.exit(1)

    remaining_indices = [
        index
        for index, row in df.iterrows()
        if not is_reviewed(row["Reviewed"])
    ]

    total_remaining = len(remaining_indices)

    if total_remaining == 0:
        print("Everything has already been reviewed.")
        return

    completed_this_session = 0

    for number, index in enumerate(
        remaining_indices,
        start=1,
    ):
        row = df.loc[index]

        show_row(
            row,
            number,
            total_remaining,
        )

        print(
            "Commands: "
            "[Enter values normally]  "
            ":skip  :quit"
        )
        print()

        # Allow a command before beginning entry.
        command = input(
            "Press Enter to edit this lexeme: "
        ).strip().lower()

        if command == ":quit":
            break

        if command == ":skip":
            continue

        print()

        headword = prompt_field(
            "Headword",
            row["Manual Headword"],
        )

        plural = prompt_field(
            "Plural",
            row["Manual Plural"],
        )

        definition = prompt_field(
            "Definition",
            row["Manual Definition"],
        )

        notes = prompt_field(
            "Notes",
            row["Manual Notes"],
        )

        print()
        print("-" * 72)
        print("PROPOSED ENTRY")
        print("-" * 72)
        print(f"Headword:   {headword or '—'}")
        print(f"Plural:     {plural or '—'}")
        print(f"Definition: {definition or '—'}")
        print(f"Notes:      {notes or '—'}")
        print()

        confirmation = input(
            "Save and mark reviewed? [Y/n]: "
        ).strip().lower()

        if confirmation in {"n", "no"}:
            continue

        df.at[index, "Manual Headword"] = headword
        df.at[index, "Manual Plural"] = plural
        df.at[index, "Manual Definition"] = definition
        df.at[index, "Manual Notes"] = notes
        df.at[index, "Reviewed"] = True

        save_csv(df)

        completed_this_session += 1

    clear_screen()

    remaining = sum(
        not is_reviewed(value)
        for value in df["Reviewed"]
    )

    print("=" * 72)
    print("REVIEW SESSION COMPLETE")
    print("=" * 72)
    print()
    print(
        f"Completed this session: {completed_this_session}"
    )
    print(
        f"Remaining lexemes:      {remaining}"
    )
    print(
        f"CSV: {CSV_PATH.resolve()}"
    )


if __name__ == "__main__":
    main()