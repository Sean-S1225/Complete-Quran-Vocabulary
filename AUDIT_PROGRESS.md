# Audit checkpoint — complete

Audit date: 2026-11-06 (America/New_York).

## Deliverable and status
- Completed consolidated `AUDIT_REPORT.md`: all 13 requested sections, 18 reproducible defect entries, decision matrix, readiness verdict, licensing register, evidence appendix.
- Verdict: FAIL for trusted unattended learning and public release; PASS WITH CAVEAT for offline snapshot reproducibility.
- Production files were not edited. SHA256 verification against `audit_evidence/source_manifest.json` found zero changes; see `final_verification.txt`.
- No further investigation is required to finish this audit pass. Corrections remain recommendations, not authorized implementation work.

## Completed evidence (do not rerun without reason)
- Repository reconstruction: active notebooks 01→03→04; 02 descriptive; older copy/empty test/exploratory converter identified. No Git metadata/lockfile.
- Offline raw QAC + cached QF replay exactly reproduced merged data. Complete 03 replay matched every frozen column, including CAMeL evidence. Isolated review queue reset proved destructive overwrite.
- Fresh 04 executed twice; final CSV byte-identical. 4,875 IDs, 77,885 included segments, 77,429 orthographic words, 6,236 ayahs. All selected coordinates and tag sets checked.
- 365 unique stratified rows exported; candidate meanings traced for concrete wrong headwords/plurals/definitions. This does not mean 365 independently certified translations.
- Per-word source comparisons: 208 QuranMorph words append literal نَن; three selected exported forms affected, while current Tanzil package targets avoid those extra letters. Refined QAC/Tanzil comparison leaves two source spelling residuals at 12:39:1 and 12:41:1.
- Audio: 35 live verses/494 words matched cached metadata; provider paths disagree with coordinate formula for 223 sampled words. 45 URL checks: 44 HTTP200 MP3, one provider-path 404. Existing 100 MP3s parse. No listening-based certification.
- Fault tests: HTTP200 HTML accepted as MP3; fallback synchronizes context/English/reference but excludes lower-preference occurrences. Reviewed blanks bypass QA. Accept-as-is and duplicate rejection tested.
- Disposable Anki 26.9.4 backend: 100→4,875→4,875 notes, stable GUIDs and review scheduling. Always-update overwrites local fields/tags; if-newer retains newer local edits. Initial sampled queue follows rank; changing ranks does not reposition existing new cards (all due=0).
- Primary-source research completed: Tanzil license/pause docs; QAC download/GPL/FAQ; QF developer terms/audio docs; Quran.com terms; official QuranMorph/Qabas pages/download form; Wiktionary/Wikimedia/CC; CAMeL package licenses. Links and uncertainty in report.

## Principal defects
- 03 c37 erases manual decisions on rebuild.
- Wrong dictionary identities and unconstrained QuranMorph promotion, cross-candidate plurals, semantically invalid fuzzy English support.
- 20 malformed doubled-final-letter manual headwords; `rijoz` plural `:skip`; English contamination. Re-review all 188 reviewed rows.
- Raw-form pronoun identities fragment variants and include attached forms despite intended independent-only policy.
- Auto QA fails to catch semantic errors and approvals never expire.
- Waqf display drops nonboundary annotations; audio validation/fallback limits; frequency update/order mismatch.
- Final CSV omits ten current reviews; production package only 100 cards.
- Plaintext credential in 01 c1 (never used; value not copied into report).
- Missing release notices and unresolved redistribution grants.

## Important correction retained
The five QF gloss strings `None` are valid negative-word translations. Their display is not erroneous. Notebook 03's default pandas CSV parsing loses them as NaN; Notebook 04 preserves them correctly.

## Outstanding external/acceptance questions
- Audible identity of every selected recording and full-deck media availability.
- Independent expert certification of linguistic content.
- Historical acquisition grants and permission for public content/audio redistribution.
- Android/iOS/desktop visual rendering and accessible playback.
- Portable clean-install/network rebuild and future GUID/schema migrations.
These are explicitly UNVERIFIED or future release gates, not concealed unfinished diagnostics.

## Evidence retention
Scripts, logs, samples, hashes and isolated generated artifacts remain in `audit_evidence/` (approximately 646 MB before any future cleanup). No cleanup was performed on resumption. Some artifacts are intentionally invalid/test-only: `faults/fake.mp3` contains HTML, `audit_full_no_audio.apkg` omits audio, and rank-test packages deliberately change ranks. Never distribute these as the deck. Expensive replay is unnecessary for reading the report.
