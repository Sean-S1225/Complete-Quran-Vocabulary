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

## Remediation planning — completed
- Created `REMEDIATION_PLAN.md` from the completed audit/handoff/checkpoint and retained diagnostics; no expensive replay, external research or sampling repeated. No production files/data changed during planning.
- Register preserves D01–D18 and adds P01–P18 for audit caveats/latent risks, with impacts, dependencies, regeneration/review requirements, seven source-rights work packages, Phases 0–6 and R01–R17 acceptance tests. These are proposals, not implemented fixes.
- Post-audit source-only commit `8aee8e2` externalized 01 credentials and stripped notebook outputs. Verified current c1 uses environment configuration. Rotation/exposure remains unverified. Original audit hashes describe the earlier snapshot and must remain intact.
- Current `.gitignore` excludes all manual decisions, inputs/generated data, media and audit evidence. GitHub is NOT a demonstrated backup of human review; private snapshot/restore is the first implementation step.
- Review policy: retain all decisions/history; targeted confirmation of all 188 accepted rows, prioritizing known corruptions; expire only materially changed/unsupported field approvals and dependencies. No automatic inheritance across identity splits/merges. Ninety pending rows and expanded risk queue resume after stable generation/package/review gates.
- Exact next steps, if implementation is authorized: Phase 0 private manifest/snapshot/restore, credential exposure disposition; D01 overwrite protection; early source-viability checks; input/identity contracts and old/new ID migration design. Do not execute production 03 before decision preservation is proved. See plan's ordered 15-step sequence.

## Plan extension — Python workflow and agents
- Integrated required M01 notebook→structured package/CLI migration into `REMEDIATION_PLAN.md`: cell/module map, side-effect boundaries, parity versus intentional fixes, stage manifests, thin notebook cutover before Phase 5, rollback and R18 workflow tests. No implementation performed.
- Added capacity/delegation plan: session ceiling four total including primary; normally Astra High primary + two Sol engineering workers, fourth only for independent tests/media work. Waves W0–W6 specify objectives, model/effort, ownership and integration gates; Low Sol reserved for editorial work. No agents spawned.
- Primary retains novel evidence evaluation, Arabic/identity/rights judgments and final verdicts. Workers implement approved contracts/tests; separate worktrees/output paths, single expensive build owner and no concurrent decision/cache/Anki writes.
- Next steps remain planning-only unless implementation authorized: private snapshot/restore, then M01-A contracts/map and D01 safeguard; follow revised 15-step sequence and W0–W1. Existing audit evidence remains authoritative; no expensive diagnostics repeated.

## Persistent workflow preferences — 2026-11-07
- Added root `AGENTS.md` as the future-session entry point. Four-agent shorthand means Astra High primary + three Sol workers (pipeline, review/package, test/media), with specified effort levels and dependency/ownership rules; no agents launched for this documentation step.
- Recorded standing user authorization: commit coherent progress when reasonable, push at completed steps, preserve ignore/private-data protections, and checkpoint after substantial work plus roughly every 10–15 minutes during sustained work or immediately before usage cutoff.
- Linked instructions from the remediation plan. This step changes documentation only; remediation remains unimplemented. Branch: `main`; documentation commit/push is the next action. Verify Git history/remote status on resumption rather than assuming an in-progress push succeeded.
- Next implementation action, when authorized: Phase 0 private snapshot/restore, then M01-A stage contracts/map and D01 protection.

## Remediation branch — 2026-11-07
- Created `remediation` from clean `main` at `97e4eb1` at the user's request. Future remediation work belongs on this branch; no implementation has started.
- Next: Phase 0 private snapshot/restore, then M01-A contracts/map and D01 protection when implementation is authorized. Verify upstream push status with Git on resumption.
