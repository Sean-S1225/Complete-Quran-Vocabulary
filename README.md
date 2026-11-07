# Complete Qur’an Vocabulary

Python/Jupyter pipeline for building a Qur’anic Arabic vocabulary Anki deck.

Read `AUDIT_REPORT.md` before relying on generated cards. The audit identifies unresolved linguistic, rebuild, audio, and licensing issues. This is not a validated public deck release.

## Pipeline

1. `01_build_corpus.ipynb`: ingest QAC and Quran.Foundation data.
2. `02_frequency_analysis.ipynb`: inspect corpus frequencies.
3. `03_build_vocabulary.ipynb`: build lexical evidence and frozen tables.
4. `04_build_Anki.ipynb`: finalize cards and build an Anki package.

`manual_review.py` and `qa_review.py` manage review decisions. **Notebook 03 currently overwrites the manual-review CSV; preserve existing decisions before running it.**

Set `QF_CLIENT_ID` and `QF_CLIENT_SECRET` in your environment for authenticated ingestion. Previously embedded credentials must be rotated if exposed.

Datasets, review CSVs, audio, generated decks, the local virtual environment, and audit evidence are excluded from Git. Obtain inputs under their applicable permissions; see the source inventory and licensing findings in the audit. The repository alone is not a complete reproducible input bundle. No blanket redistribution license is asserted for third-party content.

The audit describes the pre-publication snapshot. Notebook output removal and credential externalization were performed afterward to prepare this repository for GitHub.
