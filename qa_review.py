#!/usr/bin/env python3
"""
qa_review.py

Interactive review tool for CompleteQuranVocabulary Auto QA cards.

Default inputs (same project directory):
    final_anki_lexicon.csv
    vocabulary_frozen.pkl
    manual_lexeme_review.csv

What it does:
    - loads only rows where Auto QA Flag == True
    - shows the current proposed Anki card plus useful source evidence
    - lets you accept the automatic card unchanged OR enter manual overrides
    - writes the decision into manual_lexeme_review.csv
    - autosaves atomically after every reviewed card
    - resumes automatically on the next run

Important:
    Accepting a card unchanged sets Reviewed=True but leaves the manual
    override fields blank. Notebook 04 will therefore keep its automatic
    headword/plural/definition while no longer flagging that lexeme for QA.

Commands:
    Enter   accept current automatic card as reviewed
    e       edit manual overrides, then mark reviewed
    o       open useful lookup pages in your browser
    s       skip for now
    q       save and quit
    ?       show help
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import sys
import tempfile
import textwrap
import urllib.parse
import webbrowser
from collections import Counter
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------
# Terminal formatting
# ---------------------------------------------------------------------

USE_COLOR = (
    sys.stdout.isatty()
    and os.environ.get("TERM", "") != "dumb"
)

RESET = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
DIM = "\033[2m" if USE_COLOR else ""
CYAN = "\033[36m" if USE_COLOR else ""
YELLOW = "\033[33m" if USE_COLOR else ""
GREEN = "\033[32m" if USE_COLOR else ""
RED = "\033[31m" if USE_COLOR else ""
MAGENTA = "\033[35m" if USE_COLOR else ""


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def line(char: str = "─", width: int = 76) -> str:
    return char * width


def is_blank(value) -> bool:
    if value is None:
        return True

    try:
        if pd.isna(value):
            return True
    except (TypeError, ValueError):
        pass

    return str(value).strip() == ""


def as_bool(value) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    text = str(value).strip().lower()

    return text in {
        "1",
        "true",
        "t",
        "yes",
        "y",
    }


# ---------------------------------------------------------------------
# Compact display helpers
# ---------------------------------------------------------------------

def maybe_parse_container(value):
    """
    CSV exports can stringify Python lists/dicts/Counters.
    Parse only simple literal containers when possible.
    """
    if not isinstance(value, str):
        return value

    stripped = value.strip()

    if not stripped:
        return value

    if (
        (stripped.startswith("[") and stripped.endswith("]"))
        or (stripped.startswith("{") and stripped.endswith("}"))
        or (stripped.startswith("(") and stripped.endswith(")"))
    ):
        try:
            return ast.literal_eval(stripped)
        except (ValueError, SyntaxError):
            return value

    return value


def compact_value(value, limit: int = 6, max_chars: int = 500) -> str:
    value = maybe_parse_container(value)

    if is_blank(value):
        return "—"

    if isinstance(value, Counter):
        value = dict(value)

    if isinstance(value, dict):
        items = list(value.items())

        try:
            items.sort(
                key=lambda item: item[1],
                reverse=True,
            )
        except (TypeError, ValueError):
            pass

        shown = items[:limit]
        text = "; ".join(
            f"{key}: {val}"
            for key, val in shown
        )

        if len(items) > limit:
            text += f"; … (+{len(items) - limit})"

    elif isinstance(value, (list, tuple, set)):
        items = list(value)
        text = " / ".join(
            str(item)
            for item in items[:limit]
        )

        if len(items) > limit:
            text += f" / … (+{len(items) - limit})"

    else:
        text = str(value)

    if len(text) > max_chars:
        return text[: max_chars - 1] + "…"

    return text


def print_field(label: str, value, color: str = "") -> None:
    print(
        f"{DIM}{label:<22}{RESET} "
        f"{color}{compact_value(value)}{RESET}"
    )


def render_context(row: pd.Series) -> str:
    before = str(
        row.get(
            "Context Before Arabic",
            "",
        )
    ).strip()

    target = str(
        row.get(
            "Context Target Arabic",
            "",
        )
    ).strip()

    after = str(
        row.get(
            "Context After Arabic",
            "",
        )
    ).strip()

    pieces = []

    if before:
        pieces.append(before)

    if target:
        pieces.append(
            f"{YELLOW}{BOLD}{target}{RESET}"
        )

    if after:
        pieces.append(after)

    if pieces:
        return " ".join(pieces)

    return compact_value(
        row.get(
            "Quranic Form",
            "",
        )
    )


# ---------------------------------------------------------------------
# Load/save
# ---------------------------------------------------------------------

MANUAL_COLUMNS = [
    "Manual Headword",
    "Manual Plural",
    "Manual Definition",
    "Manual Notes",
    "Reviewed",
]


def load_inputs(
    lexicon_path: Path,
    vocabulary_path: Path,
    manual_path: Path,
):
    if not lexicon_path.exists():
        raise FileNotFoundError(
            f"Missing {lexicon_path}. Run Notebook 04 first."
        )

    if not vocabulary_path.exists():
        raise FileNotFoundError(
            f"Missing {vocabulary_path}."
        )

    if not manual_path.exists():
        raise FileNotFoundError(
            f"Missing {manual_path}."
        )

    lexicon = pd.read_csv(
        lexicon_path,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    if "Vocabulary ID" not in lexicon.columns:
        raise ValueError(
            "final_anki_lexicon.csv is missing 'Vocabulary ID'."
        )

    lexicon = lexicon.set_index(
        "Vocabulary ID",
        drop=False,
    )

    if not lexicon.index.is_unique:
        raise ValueError(
            "final_anki_lexicon.csv contains duplicate Vocabulary IDs."
        )

    vocabulary = pd.read_pickle(
        vocabulary_path
    )

    if "Vocabulary ID" in vocabulary.columns:
        vocabulary = vocabulary.set_index(
            "Vocabulary ID"
        )

    vocabulary.index.name = "Vocabulary ID"

    if not vocabulary.index.is_unique:
        raise ValueError(
            "vocabulary_frozen.pkl contains duplicate Vocabulary IDs."
        )

    manual = pd.read_csv(
        manual_path,
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    if "Vocabulary ID" not in manual.columns:
        raise ValueError(
            "manual_lexeme_review.csv is missing 'Vocabulary ID'."
        )

    if manual["Vocabulary ID"].duplicated().any():
        duplicates = manual.loc[
            manual["Vocabulary ID"].duplicated(
                keep=False
            ),
            "Vocabulary ID",
        ].tolist()

        raise ValueError(
            "manual_lexeme_review.csv contains duplicate Vocabulary IDs: "
            + ", ".join(
                map(str, duplicates[:10])
            )
        )

    for column in MANUAL_COLUMNS:
        if column not in manual.columns:
            manual[column] = ""

    return lexicon, vocabulary, manual


def atomic_save_csv(
    dataframe: pd.DataFrame,
    path: Path,
) -> None:
    """
    Write beside the destination, then atomically replace it.
    """
    path = path.resolve()
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=path.stem + "_",
        suffix=".tmp",
        dir=path.parent,
    )

    os.close(fd)
    temp_path = Path(temp_name)

    try:
        dataframe.to_csv(
            temp_path,
            index=False,
            encoding="utf-8-sig",
        )

        os.replace(
            temp_path,
            path,
        )

    finally:
        if temp_path.exists():
            temp_path.unlink()


def manual_row_index(
    manual: pd.DataFrame,
    vocabulary_id: str,
):
    matches = manual.index[
        manual["Vocabulary ID"]
        == vocabulary_id
    ].tolist()

    if matches:
        return matches[0]

    new_row = {
        column: ""
        for column in manual.columns
    }

    new_row[
        "Vocabulary ID"
    ] = vocabulary_id

    manual.loc[
        len(manual)
    ] = new_row

    return manual.index[-1]


def existing_manual_values(
    manual: pd.DataFrame,
    vocabulary_id: str,
):
    matches = manual[
        manual["Vocabulary ID"]
        == vocabulary_id
    ]

    if matches.empty:
        return {
            column: ""
            for column in MANUAL_COLUMNS
        }

    row = matches.iloc[0]

    return {
        column: row.get(
            column,
            "",
        )
        for column in MANUAL_COLUMNS
    }


def save_review(
    manual: pd.DataFrame,
    manual_path: Path,
    vocabulary_id: str,
    overrides: dict | None = None,
):
    idx = manual_row_index(
        manual,
        vocabulary_id,
    )

    overrides = overrides or {}

    for column in [
        "Manual Headword",
        "Manual Plural",
        "Manual Definition",
        "Manual Notes",
    ]:
        if column in overrides:
            manual.at[
                idx,
                column,
            ] = overrides[column]

    manual.at[
        idx,
        "Reviewed",
    ] = True

    atomic_save_csv(
        manual,
        manual_path,
    )


# ---------------------------------------------------------------------
# Why was it flagged?
# ---------------------------------------------------------------------

def qa_reasons(
    final_row: pd.Series,
    evidence_row: pd.Series | None,
):
    reasons = []

    if is_blank(
        final_row.get(
            "Headword"
        )
    ):
        reasons.append(
            "missing headword"
        )

    if is_blank(
        final_row.get(
            "Definition"
        )
    ):
        reasons.append(
            "missing definition"
        )

    if evidence_row is not None:
        status = evidence_row.get(
            "Wiktionary Match Status",
            "",
        )

        if (
            not is_blank(status)
            and str(status) != "matched"
        ):
            reasons.append(
                "Wiktionary match status: "
                + str(status)
            )

    score = final_row.get(
        "Definition Match Score",
        "",
    )

    if not is_blank(score):
        try:
            if float(score) < 0.15:
                reasons.append(
                    f"low definition-match score: {float(score):.3f}"
                )
        except (TypeError, ValueError):
            pass

    if not reasons:
        reasons.append(
            "flagged by Notebook 04 Auto QA"
        )

    return reasons


# ---------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------

def qac_url(row: pd.Series) -> str | None:
    try:
        surah = int(
            row.get(
                "Example Surah"
            )
        )
        ayah = int(
            row.get(
                "Example Ayah"
            )
        )
        word = int(
            row.get(
                "Example Word"
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        return None

    location = urllib.parse.quote(
        f"({surah}:{ayah}:{word})"
    )

    return (
        "https://corpus.quran.com/"
        f"wordmorphology.jsp?location={location}"
    )


def open_lookups(row: pd.Series) -> None:
    headword = str(
        row.get(
            "Headword",
            "",
        )
    ).strip()

    urls = []

    if headword:
        urls.append(
            "https://www.google.com/search?q="
            + urllib.parse.quote(
                f'"{headword}" Arabic dictionary Quran'
            )
        )

        urls.append(
            "https://en.wiktionary.org/wiki/"
            + urllib.parse.quote(
                headword
            )
        )

    corpus_url = qac_url(
        row
    )

    if corpus_url:
        urls.append(
            corpus_url
        )

    if not urls:
        print(
            f"{RED}No lookup URLs available for this row.{RESET}"
        )
        input(
            "\nPress Enter to continue..."
        )
        return

    print(
        f"\n{CYAN}Opening lookup pages:{RESET}"
    )

    for url in urls:
        print(
            f"  {url}"
        )

        webbrowser.open_new_tab(
            url
        )

    input(
        "\nPress Enter to return to review..."
    )


# ---------------------------------------------------------------------
# Review UI
# ---------------------------------------------------------------------

def evidence_value(
    evidence_row: pd.Series | None,
    *names,
):
    if evidence_row is None:
        return ""

    for name in names:
        if name in evidence_row.index:
            value = evidence_row.get(
                name
            )

            if not is_blank(value):
                return value

    return ""


def display_review(
    final_row: pd.Series,
    evidence_row: pd.Series | None,
    manual_values: dict,
    position: int,
    total: int,
    reviewed_session: int,
):
    clear_screen()

    vocabulary_id = str(
        final_row[
            "Vocabulary ID"
        ]
    )

    print(
        f"{BOLD}Complete Qur'an Vocabulary — Auto QA Review{RESET}"
    )

    print(
        f"{DIM}"
        f"Queue {position}/{total}  •  "
        f"Reviewed this session: {reviewed_session}"
        f"{RESET}"
    )

    print(
        line()
    )

    print(
        f"\n{MAGENTA}{BOLD}"
        f"{final_row.get('Headword', '')}"
        f"{RESET}"
    )

    if not is_blank(
        final_row.get(
            "Plural"
        )
    ):
        print(
            f"{DIM}Plural:{RESET} "
            f"{final_row.get('Plural')}"
        )

    print(
        f"{GREEN}"
        f"{final_row.get('Definition', '')}"
        f"{RESET}"
    )

    print()

    print_field(
        "Vocabulary ID",
        vocabulary_id,
    )
    print_field(
        "Root",
        final_row.get(
            "Root"
        ),
    )
    print_field(
        "POS",
        final_row.get(
            "POS"
        ),
    )
    print_field(
        "Frequency",
        final_row.get(
            "Frequency"
        ),
    )
    print_field(
        "Frequency rank",
        final_row.get(
            "Frequency Rank"
        ),
    )

    print(
        f"\n{CYAN}{BOLD}Why flagged{RESET}"
    )

    for reason in qa_reasons(
        final_row,
        evidence_row,
    ):
        print(
            f"  • {reason}"
        )

    print(
        f"\n{CYAN}{BOLD}Qur'anic example{RESET}"
    )

    print(
        f"  {render_context(final_row)}"
    )

    context_english = final_row.get(
        "Context English",
        "",
    )

    if not is_blank(
        context_english
    ):
        print(
            f"  {DIM}{context_english}{RESET}"
        )

    print_field(
        "Reference",
        final_row.get(
            "Example Reference"
        ),
    )
    print_field(
        "Occurrence gloss",
        final_row.get(
            "Occurrence Gloss"
        ),
    )

    print(
        f"\n{CYAN}{BOLD}Current automatic decision{RESET}"
    )

    print_field(
        "Headword",
        final_row.get(
            "Headword"
        ),
    )
    print_field(
        "Headword source",
        final_row.get(
            "Headword Source"
        ),
    )
    print_field(
        "Plural",
        final_row.get(
            "Plural"
        ),
    )
    print_field(
        "Plural source",
        final_row.get(
            "Plural Source"
        ),
    )
    print_field(
        "Definition",
        final_row.get(
            "Definition"
        ),
    )
    print_field(
        "Definition source",
        final_row.get(
            "Definition Source"
        ),
    )
    print_field(
        "Def. match score",
        final_row.get(
            "Definition Match Score"
        ),
    )

    print(
        f"\n{CYAN}{BOLD}Source evidence{RESET}"
    )

    evidence_fields = [
        (
            "QAC lemma",
            (
                "QAC Lemma",
                "Lemma",
            ),
        ),
        (
            "QuranMorph forms",
            (
                "QuranMorphMatchForms",
                "QuranMorph Match Forms",
            ),
        ),
        (
            "Wiktionary status",
            (
                "Wiktionary Match Status",
            ),
        ),
        (
            "Wiktionary basis",
            (
                "Wiktionary Match Basis",
                "Wiktionary Match Method",
            ),
        ),
        (
            "Observed forms",
            (
                "ObservedForms",
                "Observed Forms",
            ),
        ),
        (
            "English glosses",
            (
                "English Glosses",
            ),
        ),
        (
            "Definition evidence",
            (
                "Definition Evidence",
            ),
        ),
        (
            "QuranMorph evidence",
            (
                "QuranMorph Evidence",
                "QuranMorphMatchEvidence",
            ),
        ),
    ]

    for label, names in evidence_fields:
        value = evidence_value(
            evidence_row,
            *names,
        )

        if not is_blank(value):
            print_field(
                label,
                value,
            )

    existing_overrides = [
        (
            "Manual Headword",
            manual_values.get(
                "Manual Headword",
                "",
            ),
        ),
        (
            "Manual Plural",
            manual_values.get(
                "Manual Plural",
                "",
            ),
        ),
        (
            "Manual Definition",
            manual_values.get(
                "Manual Definition",
                "",
            ),
        ),
        (
            "Manual Notes",
            manual_values.get(
                "Manual Notes",
                "",
            ),
        ),
    ]

    if any(
        not is_blank(value)
        for _, value
        in existing_overrides
    ):
        print(
            f"\n{CYAN}{BOLD}Existing manual values{RESET}"
        )

        for label, value in existing_overrides:
            if not is_blank(value):
                print_field(
                    label,
                    value,
                )

    print(
        "\n"
        + line()
    )

    print(
        f"{BOLD}Enter{RESET}=accept automatic card  "
        f"{BOLD}e{RESET}=edit  "
        f"{BOLD}o{RESET}=open lookups  "
        f"{BOLD}s{RESET}=skip  "
        f"{BOLD}q{RESET}=quit  "
        f"{BOLD}?{RESET}=help"
    )


def prompt_override(
    label: str,
    automatic,
    existing,
):
    print(
        f"\n{BOLD}{label}{RESET}"
    )

    print(
        f"  Automatic: "
        f"{compact_value(automatic)}"
    )

    print(
        f"  Existing manual override: "
        f"{compact_value(existing)}"
    )

    value = input(
        "  New override "
        "(Enter = keep existing; :clear = remove override): "
    )

    if value == "":
        return existing

    if value.strip().lower() == ":clear":
        return ""

    return value.strip()


def edit_overrides(
    final_row: pd.Series,
    manual_values: dict,
):
    print(
        f"\n{CYAN}{BOLD}Manual overrides{RESET}"
    )

    print(
        "Only fill fields you actually want to override. "
        "Blank manual fields leave the automatic value in place."
    )

    headword = prompt_override(
        "Headword",
        final_row.get(
            "Headword",
            "",
        ),
        manual_values.get(
            "Manual Headword",
            "",
        ),
    )

    plural = prompt_override(
        "Plural",
        final_row.get(
            "Plural",
            "",
        ),
        manual_values.get(
            "Manual Plural",
            "",
        ),
    )

    definition = prompt_override(
        "Definition",
        final_row.get(
            "Definition",
            "",
        ),
        manual_values.get(
            "Manual Definition",
            "",
        ),
    )

    notes = prompt_override(
        "Notes",
        "",
        manual_values.get(
            "Manual Notes",
            "",
        ),
    )

    print(
        f"\n{BOLD}Review result{RESET}"
    )

    print_field(
        "Headword",
        headword
        if not is_blank(headword)
        else final_row.get(
            "Headword",
            "",
        ),
    )

    print_field(
        "Plural",
        plural
        if not is_blank(plural)
        else final_row.get(
            "Plural",
            "",
        ),
    )

    print_field(
        "Definition",
        definition
        if not is_blank(definition)
        else final_row.get(
            "Definition",
            "",
        ),
    )

    if not is_blank(notes):
        print_field(
            "Notes",
            notes,
        )

    answer = input(
        "\nSave and mark reviewed? [Y/n] "
    ).strip().lower()

    if answer in {
        "",
        "y",
        "yes",
    }:
        return {
            "Manual Headword":
                headword,
            "Manual Plural":
                plural,
            "Manual Definition":
                definition,
            "Manual Notes":
                notes,
        }

    return None


HELP_TEXT = """
Review philosophy

  Auto QA means "the pipeline wants a human sanity check",
  not "this card is definitely wrong."

  Enter
      Accept the automatic card unchanged.
      This sets Reviewed=True but does NOT copy the automatic
      fields into the manual override fields.

  e
      Enter manual overrides. You can override only the fields
      that need correction.

      During editing:
          Enter   keeps the existing manual override
          :clear  removes an existing override and returns that
                  field to the automatic pipeline

  o
      Open a small lookup bundle in your default browser:
          - Google dictionary/Qur'an search
          - English Wiktionary
          - Quranic Arabic Corpus morphology page, when coordinates
            are available

  s
      Skip this card for now. Nothing is written.

  q
      Quit. All prior accepted/edited cards are already saved.

The tool autosaves manual_lexeme_review.csv after every accepted card.
"""


def review_loop(
    lexicon: pd.DataFrame,
    vocabulary: pd.DataFrame,
    manual: pd.DataFrame,
    manual_path: Path,
    limit: int | None = None,
):
    flagged = lexicon[
        lexicon[
            "Auto QA Flag"
        ].apply(
            as_bool
        )
    ].copy()

    if "Frequency Rank" in flagged.columns:
        flagged[
            "_rank"
        ] = pd.to_numeric(
            flagged[
                "Frequency Rank"
            ],
            errors="coerce",
        )

        flagged = flagged.sort_values(
            "_rank",
            na_position="last",
        )

    # final_anki_lexicon.csv was built after manual decisions were
    # applied, so Reviewed=True rows should already have Auto QA=False.
    # This extra exclusion makes the tool robust to stale exports.
    reviewed_ids = set(
        manual.loc[
            manual[
                "Reviewed"
            ].apply(
                as_bool
            ),
            "Vocabulary ID",
        ].astype(str)
    )

    flagged = flagged[
        ~flagged[
            "Vocabulary ID"
        ].astype(str).isin(
            reviewed_ids
        )
    ]

    if limit is not None:
        flagged = flagged.head(
            limit
        )

    if flagged.empty:
        print(
            f"{GREEN}No unreviewed Auto QA cards remain.{RESET}"
        )
        return

    queue = list(
        flagged.index
    )

    reviewed_session = 0
    position = 0

    while position < len(queue):
        vocabulary_id = queue[
            position
        ]

        final_row = lexicon.loc[
            vocabulary_id
        ]

        evidence_row = (
            vocabulary.loc[
                vocabulary_id
            ]
            if vocabulary_id
            in vocabulary.index
            else None
        )

        manual_values = (
            existing_manual_values(
                manual,
                str(
                    vocabulary_id
                ),
            )
        )

        display_review(
            final_row,
            evidence_row,
            manual_values,
            position + 1,
            len(queue),
            reviewed_session,
        )

        command = input(
            "\nAction: "
        ).strip().lower()

        if command == "":
            save_review(
                manual,
                manual_path,
                str(
                    vocabulary_id
                ),
            )

            reviewed_session += 1
            position += 1
            continue

        if command in {
            "e",
            "edit",
        }:
            overrides = edit_overrides(
                final_row,
                manual_values,
            )

            if overrides is not None:
                save_review(
                    manual,
                    manual_path,
                    str(
                        vocabulary_id
                    ),
                    overrides,
                )

                reviewed_session += 1
                position += 1

            continue

        if command in {
            "o",
            "open",
        }:
            open_lookups(
                final_row
            )
            continue

        if command in {
            "s",
            "skip",
        }:
            position += 1
            continue

        if command in {
            "q",
            "quit",
            "exit",
        }:
            print(
                f"\nSaved. Reviewed "
                f"{reviewed_session} card(s) this session."
            )
            return

        if command in {
            "?",
            "h",
            "help",
        }:
            clear_screen()
            print(
                textwrap.dedent(
                    HELP_TEXT
                ).strip()
            )
            input(
                "\nPress Enter to return..."
            )
            continue

    print(
        f"\n{GREEN}Reached the end of the current QA queue.{RESET}"
    )

    print(
        f"Reviewed {reviewed_session} card(s) this session."
    )

    print(
        "Rerun Notebook 04 to regenerate the lexicon and "
        "see which QA flags remain."
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Interactively review CompleteQuranVocabulary "
            "Auto QA cards."
        )
    )

    parser.add_argument(
        "--lexicon",
        type=Path,
        default=Path(
            "./final_anki_lexicon.csv"
        ),
        help=(
            "Final Notebook 04 lexicon CSV "
            "(default: ./final_anki_lexicon.csv)"
        ),
    )

    parser.add_argument(
        "--vocabulary",
        type=Path,
        default=Path(
            "./vocabulary_frozen.pkl"
        ),
        help=(
            "Frozen vocabulary evidence pickle "
            "(default: ./vocabulary_frozen.pkl)"
        ),
    )

    parser.add_argument(
        "--manual",
        type=Path,
        default=Path(
            "./manual_lexeme_review.csv"
        ),
        help=(
            "Manual review CSV updated in place "
            "(default: ./manual_lexeme_review.csv)"
        ),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Review at most N cards this run."
        ),
    )

    return parser.parse_args()


def main():
    args = parse_args()

    lexicon, vocabulary, manual = (
        load_inputs(
            args.lexicon,
            args.vocabulary,
            args.manual,
        )
    )

    review_loop(
        lexicon,
        vocabulary,
        manual,
        args.manual,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
