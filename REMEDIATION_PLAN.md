# CompleteQuranVocabulary remediation plan

Planning baseline: 2026-11-06 audit and subsequent source-only GitHub preparation. **No remediation is implemented by this document.**

The safe sequence is: preserve decisions → settle identity and source alignment → repair lexical generation → stabilize examples and audio → prove package updates → migrate and resume review → clear distribution. Do not resume the remaining manual queue against the present generator. Repairing individual cards now would repeatedly review unstable outputs and would leave many unflagged errors untouched.

## Evidence and current state

This plan consolidates `AUDIT_REPORT.md`, `CODEX_AUDIT_HANDOFF.md`, `AUDIT_PROGRESS.md`, and retained `audit_evidence/` scripts, logs and samples. Existing offline replay, sampling, network research and Anki experiments were reused; no expensive audit was repeated. Notebook cell references are the audit's **zero-based JSON cell indices**, not displayed execution numbers. `01`, `02`, `03`, `04` below mean `01_build_corpus.ipynb`, `02_frequency_analysis.ipynb`, `03_build_vocabulary.ipynb`, `04_build_Anki.ipynb` respectively.

Established baseline: 4,875 lexemes, 77,885 included lexical segments, 77,429 orthographic words, 6,236 ayahs; 278 manual rows, 188 accepted and 90 pending. Fresh 04 has 461 Auto-QA rows. The saved final CSV applies only 178 reviews and the production APKG has 100 notes. These are baseline observations, **not counts to hard-code after an intentional identity-policy change**.

Offline transformations and tested coordinate/tag joins are reproducible. Stable GUIDs and review scheduling survived tested Anki 26.9.4 imports. This does not establish semantic accuracy, audible identity, portable installation, or redistribution permission. The 365-row stratified export is a sampling instrument, not certification of 365 correct definitions.

Post-audit source commit `8aee8e2` externalized 01's credential to `QF_CLIENT_ID`/`QF_CLIENT_SECRET` and removed notebook outputs. Current 01 c1 confirms environment loading. Rotation/exposure resolution remains unverified. The historical audit's “no Git” and plaintext-source descriptions apply to its original snapshot. `.gitignore` excludes the decisions, data, media and diagnostics: **the GitHub commit is not a backup of the review work**. Preserve the historical audit manifest and create a separate current baseline; do not replace it to make changed notebook hashes appear unchanged.

## Reading the finding register

D01–D18 retain audit identifiers. P01–P18 identify additional risks or missing safeguards already described by the audit; they are not newly asserted data failures. D17 has source-specific work packages below.

Each entry specifies status/severity/confidence, location, cause/consequence, impact, regeneration, missed checks, action/test and dependencies. Confidence refers to the stated observation; an unverified outcome is not assigned false certainty.

**Impact codes:** I = lexeme identity/Vocabulary ID; X = inclusion/exclusion; H = headword; P = plural; D = definition; M = root/POS/morphology; F = frequency/rank; O = representative occurrence; Q = Qur'anic context; E = English context; A = audio; T = tags; K = Anki note/package identity or rebuild; L = licensing/distribution. Only listed domains are directly affected or can change through the proposed remedy. Unlisted domains are not expected to change. “Learner harm” means potential incorrect memorization, not merely inconvenience.

**Regeneration codes:** `3→4→B` means rerun 03 and 04, then rebuild APKG; `4→B` means no rerun of 01/03; `B` means packaging only; `—` means none. `1→3→4→B` uses cached licensed source inputs where possible, not automatically a network reacquisition. **02 is required only when included populations/frequencies change (D08/P02) or its report changes; it is descriptive, never a dependency of 03.** Otherwise no 02 rerun. `A:validate` reuses valid bytes; `A:delta` fetches/rebuilds only changed or failed assets, never indiscriminate redownload. Audio is recorded speech, not generated TTS. Every entry states QA and human-review requirements. All production candidates ultimately receive the full automatic suite even when an individual remedy needs no data rerun.

Dependencies name prerequisites for accepting a remedy; every implementation depends on Phase 0. Tests may be drafted earlier using protected fixtures. Logical investigation may proceed in parallel, but production rebuilds must respect dependencies.

## Phase 0 — Protect current state

Before editing or executing production notebooks:

1. Create an access-controlled, versioned snapshot **outside the working tree**, retaining hashes, timestamps and a restore procedure. Respect source storage permissions; do not publish excluded material to GitHub. Verify restoration of the manual CSV and frozen evidence into a temporary directory. Keep at least one independent copy.
2. Preserve `manual_lexeme_review.csv` byte-for-byte and parsed values, including all notes, blank overrides, Reviewed flags, 188 accepted rows and 90 pending rows. Preserve both review tools and the old final CSV: differences are evidence, not permission to overwrite either.
3. Preserve all four active notebooks, source commit, `.gitignore`, README, handoff, audit report/checkpoint, **all `audit_evidence/` including its historical manifest**, and the inactive notebook copy separately labeled archival. Do not ship deliberately invalid audio or synthetic/no-audio audit packages.
4. Preserve raw QAC, `QF_Database.csv`, `quran-morph.csv`, Kaikki JSONL, both Tanzil files/notices; `qac_morphology.parquet`, `QuranTotalMergedDatabase.csv`, both frozen vocabulary and occurrence formats; `final_anki_lexicon.csv`, `quran_vocabulary_test.apkg`, and all `anki_media*` caches. Record exact source versions, acquisition evidence, hashes and installed dependency/resource versions. A source-only clone cannot recreate these snapshots.
5. Record the actual model/deck IDs, field schema, namespace/GUID algorithm and baseline ID set. If a user has imported the deck, require a collection backup before any future migration; audit disposable collections are not user backups.
6. Capture current source hashes separately from audit hashes. Resolve credential exposure/rotation (D16) without copying credentials into logs, manifests or Git. Snapshot access controls must account for old outputs or archives that could contain credentials.
7. Introduce D01's non-destructive decision handling and a dry-run/diff path **before the first 03 rerun**. Keep a frozen baseline for comparing all later outputs. Do not use current review flags as permission to skip validation.

Exit: demonstrated restoration; code and private data recovery paths; complete baseline manifest; no execution path can silently overwrite decisions. The source commit alone does not satisfy this gate.

## Finding register

### D01 — Destructive manual queue regeneration
- **FAIL · Critical · high confidence.** Location: 03 c37, manual queue initialization and `manual_review.to_csv`; `manual_lexeme_review.csv`.
- **Cause → consequence:** queue generation recreates the decision file; isolated replay resets all 278 rows, losing 188 acceptances and overrides (`replay03.log`: `RESET REVIEW {False: 278}`). Learner harm: **indirect yes**, corrected values can revert to wrong automatic content. Impact: H,P,D,K.
- **Action / regression:** separate generated queue from durable decisions; append new IDs, retain old/retired IDs with status, reject duplicate keys, write atomic versioned backups. Run 03 twice against a seeded copy and require all old decisions/notes unchanged plus only intended additions; inject a failed write.
- **Missed checks:** frozen-table equality and row counts do not inspect decision preservation. **Regeneration:** — for the safeguard; test 03 in isolation. A:none; QA: preservation tests; human: none if restored exactly, otherwise recover missing decisions before review. **Dependencies:** Phase 0 snapshot. Implement first.

### D02 — Wrong dictionary identities
- **FAIL · High · high confidence.** Location: 03 c17/21/23/25/27 normalization, POS/query/index/matching; 04 c6–7. `linguistic_samples.log`: `qaAnit`→summit, `kita`biY`→bookseller, `wa`liday`→child, `Hunayon`→nostalgia.
- **Cause → consequence:** undiacritized inflection matches and broad POS/first-match precedence erase lexical distinctions. Learner harm: **yes**. Impact: H,P,D,M,O,Q,E,A.
- **Action / regression:** retain candidate/entry/sense identity and match route; require compatible vocalization, root, derivation and grammatical role; ambiguous matches remain unresolved. Gold-test all named cases plus exact/relaxed, numbered homographs, proper names and inflection collisions. Do not fix only the 63 relaxed matches.
- **Missed checks:** matched status, match coverage, coordinate joins and fuzzy English score. **Regeneration:** 3→4→B; A:delta if examples change; QA: all candidate-driven fields; human: changed candidate identities and unresolved conflicts, including accepted rows with live automatic fields. **Dependencies:** D08, P01, P02; coordinate the candidate contract with D03/P03.

### D03 — Morphology-unsafe headword promotion
- **FAIL · High · high confidence.** Location: 04 c7 `choose_headword`, 03 c23 QuranMorph queries. Form-X `yasotaEotibu`→form-I عتب; comparative `>aTohar`→طاهر; `mula`qiy`, `muxal~afuwn`, `m~ugoraquwn` change participial identity/voice.
- **Cause → consequence:** singleton/source priority substitutes for morphological compatibility; 2,575 fresh headwords use QuranMorph. Learner harm: **yes**. Impact: H,P,D,M,O,Q,E,A.
- **Action / regression:** assert derived form, voice, participle type and lexical category compatibility before promotion, including indirect dictionary routes. Annotate disagreement; use supported citation forms, never blind ending removal. Test weak/derived verbs, elatives, active/passive participles and proper names with expert-approved expectations.
- **Missed checks:** unique roots/consistent aggregated metadata do not compare final headword to that metadata. **Regeneration:** 3→4→B; A:delta; QA: all headword promotions; human: changed or conflicting headwords and dependent definitions/plurals. **Dependencies:** D08, P02, P03; implement alongside D02.

### D04 — Cross-candidate plural contamination
- **FAIL · High · high confidence.** Location: 04 c11–12 `extract_plural_candidates`, `choose_plural`. غلي receives أغلال; خزي receives خزوز; خالق receives أخلاق/خلق/خلقان.
- **Cause → consequence:** plural union is detached from accepted lexical identity. Learner harm: **yes**. Impact: P,M.
- **Action / regression:** link each plural to accepted entry and meaning; label dictionary supplement versus Qur'anic attestation; allow explicit suppression. Test all named wrong associations, valid broken plurals, duals, collective/plural-only nouns and “no useful plural.”
- **Missed checks:** a dictionary plural string can be valid Arabic yet belong to another word. **Regeneration:** 4→B after corrected 03 evidence; A:none; QA: all automatic plurals; human: validate all retained automatic plural assignments, prioritize changed/reviewed ones. **Dependencies:** D02,D03,P03,P08.

### D05 — English similarity accepted as semantics
- **FAIL · High · high confidence.** Location: 04 c9–10 `fuzzy_token_match`, `definition_support`, `choose_definition`; 03 c12 evidence tiers. Actual Creator→creation; synthetic lie/live scores ≈0.988; `labiva` uses one narrow gloss despite 30 occurrences; `walada` retains verse clauses.
- **Cause → consequence:** character similarity and cleanest-tier frequency do not establish meaning, voice or lexical register. Learner harm: **yes**. Impact: D,M,E.
- **Action / regression:** retain broad occurrence evidence; select verified senses from accepted identities, distinguishing contextual gloss from citation definition. Similarity may retrieve candidates but cannot approve them. Test negation, agent/action, voice, polysemy, function words and the named counterexamples; preserve dissenting evidence.
- **Missed checks:** score thresholds, nonempty definitions and source labels. **Regeneration:** 3→4→B; A:none unless another remedy changes examples; QA: all definitions, not just 819 dictionary+QF rows; human: changed senses and unverified contextual fallbacks (3,868 current QF definitions are a risk population, not 3,868 proven errors). **Dependencies:** D02,D03,D10,P04,P03.

### D06 — Corrupted accepted manual values
- **FAIL · High · high confidence in anomalies; input mechanism unknown.** Location: manual CSV rows identified in `linguistic_samples.log`; 04 c7/10/12. Twenty doubled-terminal-base-letter headwords; `rijoz` plural `:skip`; `s~aAhirap` malformed Arabic and English contamination.
- **Cause → consequence:** unchecked input is promoted as authoritative; QA=False. Learner harm: **yes**. Impact: H,P,D,O,Q,E,A.
- **Action / regression:** preserve originals; compare all 188 accepted rows against source evidence and saved display; correct confirmed errors only. Add command/content separation, Unicode preview and field checks. Repeated letters trigger review, not automatic deletion. Round-trip every anomalous fixture and valid gemination.
- **Missed checks:** Reviewed flag bypasses validation; no semantic/manual anomaly gate. **Regeneration:** 4→B after reviewed corrections; A:delta for changed headword-driven examples; QA: all manual rows; human: **all 188 get a targeted integrity/semantic confirmation**, not blanket deletion or forced re-entry of valid decisions. **Dependencies:** D02–D05 stable, D07,P08,P09 before saving migrated confirmations.

### D07 — Non-expiring approvals and weak Auto QA
- **FAIL · High · high confidence.** Location: 04 c13 `needs_review`, `qa_review.py` queue/save. Reviewed blank rows bypass QA; current score floor ≈0.637 makes `<0.15` ineffective for selected definitions.
- **Cause → consequence:** one global Boolean substitutes for field/evidence validation. Learner harm: **yes**, bad data gains false assurance. Impact: H,P,D,M,O,Q,E,A,K.
- **Action / regression:** unconditional integrity failures; separate reason codes and acceptance from validation; field/evidence fingerprints and reviewer/schema versions. Test accepted-as-is fields after source/code changes, stable manual overrides, missing required fields, and derived-field changes. No single numeric score may certify semantics.
- **Missed checks:** current `needs_review` is itself the deficient check. **Regeneration:** 4→B; A:none for QA alone; QA: all rows and reason reconciliation; human: affected fields, with conservative evidence-based migration described below. **Dependencies:** final Phase 1–4 contracts, P08,P09,P11; preservation design starts in Phase 0, acceptance migration is Phase 5.

### D08 — Pronoun inclusion and unstable lexical identity
- **FAIL · High · high confidence in policy mismatch; final replacement policy needs linguistic approval.** Location: 01 c6 `is_vocabulary_entry`, `get_vocabulary_id`; PRON groups through 03/04.
- **Cause → consequence:** QAC STEM is mistaken for grammatical independence; 2,461 prefixed PRON occurrences and raw-form IDs such as `hum/humo/humu`; downstream `PRON:ki`→لِ and `PRON:himu`→بِ. Learner harm: **yes**. Impact: I,X,H,P,D,M,F,O,Q,E,A,T,K.
- **Action / regression:** specify bound/independent policy and allowed recitational collapse; build reviewed source-coordinate→lexeme mapping and old→new ID migration. Do not merge by Arabic front alone. Test لَكِ at 3:37:21, بِهِم at 34:9, independent pronouns, genuine homographs, excluded prefixes/suffixes and 30 INL stems. Account explicitly for all removed/merged/split occurrences.
- **Missed checks:** stem selection, unique IDs and correct totals only prove implementation consistency. **Regeneration:** 1→3→4→B, plus 02; A:delta; QA: all counts/tags/IDs and affected lexical fields; human: every identity split/merge/exclusion and affected inherited decisions. **Dependencies:** Phase 0; design P10 migration before applying changed IDs.

### D09 — Faulty auxiliary orthographic tokens
- **FAIL · Medium · high confidence in mismatch, upstream cause unknown.** Location: `quran-morph.csv` `word`, 04 c1 and ranking. 208 extra نَن strings; selected exports for `laday`, `wa`liday`, `nakiyr`; package Tanzil target currently avoids these extra letters.
- **Cause → consequence:** auxiliary source text is used without textual validation, affecting ranking/export provenance. Learner harm: **possible**, particularly CSV consumers; not proof current package displays those suffixes. Impact: O,Q,E,A.
- **Action / regression:** quarantine affected tokens; select a validated display source with explicit coordinate mapping, preserving raw inputs. Test all 208 and the two refined QAC/Tanzil residuals at 12:39:1,12:41:1; distinguish encoding differences from errors.
- **Missed checks:** row counts and join keys. **Regeneration:** 4→B for current display/ranking route; 3 also if auxiliary evidence construction changes; A:delta; QA: all-source token checks; human: changed examples and unresolved source disagreements. **Dependencies:** P01; source replacement, if necessary, invokes D17.

### D10 — Literal negative gloss parsed as null
- **FAIL · Medium · high confidence.** Location: 03 c1 `pd.read_csv`, gloss evidence. Five `None` glosses at 14:9:14,16:79:9,18:22:19,18:27:8,56:79:1; 04 already preserves them.
- **Cause → consequence:** default NA parsing discards real English evidence. Learner harm: **possible**, through definition selection. Impact: D,E.
- **Action / regression:** explicit column-specific missing-value rules; round-trip `None`, empty text, genuine missing values, IDs and booleans without conflating them. Retain “None” on display.
- **Missed checks:** complete joins and nonempty aggregated evidence from other occurrences. **Regeneration:** 3→4→B; A:none; QA: CSV contract and changed definition evidence; human: changed definitions only. **Dependencies:** P01 data contract.

### D11 — Display annotations stripped during waqf parsing
- **FAIL · Medium · high confidence.** Location: 04 c4 `split_tanzil_ayah`; `quran-uthmani.txt`. Strips ۙۛۜ۞۩ (68/12/7/199/15 input occurrences).
- **Cause → consequence:** indexing/boundary normalization mutates display text. Learner harm: **possible**, recitation/context interpretation. Impact: Q,L.
- **Action / regression:** separate original display spans from boundary/index maps; preserve nonboundary signs. Reconstruct source text under documented whitespace/highlight handling; test every sign and explicit merge at 2:181,8:6,13:37,37:130. Do not add arbitrary stop rules as part of this fix.
- **Missed checks:** target equality and word counts do not retain intervening marks. **Regeneration:** 4→B; A:none if selection unchanged, delta otherwise; QA: all context spans; human: changed pause-edge displays, not unrelated definitions. **Dependencies:** P01,D09; D17 permission for excerpt/formatting before release.

### D12 — Unvalidated/non-atomic audio downloads
- **FAIL · High · high confidence in reproduced failure path.** Location: 04 c23 `download_audio`; `fault_checks.log` accepts HTTP200 HTML as MP3. Existing 100 MP3s decode; do not label them corrupt.
- **Cause → consequence:** status/cache existence substitutes for media validation; interrupted writes persist. Learner harm: **possible** via misleading/corrupt media; availability harm established. Impact: A,K.
- **Action / regression:** validate nonempty bytes, format/decode/duration/completeness, atomically finalize cache, quarantine invalid files, record failures. Test HTML, empty/truncated MP3, timeout, interrupted write and corrupt existing cache. Establish an explicit missing-audio release policy.
- **Missed checks:** HTTP status, filename extension and referenced-file existence. **Regeneration:** B; A:validate all, replace failures only; QA: media and package references; human: listening for replaced recordings/changed occurrences. **Dependencies:** P05 mapping policy, P11 provenance, P12 cache contract.

### D13 — Fallback loses lower-preference occurrences
- **FAIL · Medium · high confidence.** Location: 04 c15 filters and c26 `resolve_audio_for_card`. `samaA^'` 310→1 candidate; `kaAna` 1,358→323; injected failure proves limited search.
- **Cause → consequence:** ranking discards candidates instead of ordering them; available valid audio may be missed. Learner harm: **possible** if a fallback example changes the taught sense. Impact: O,Q,E,A,K.
- **Action / regression:** retain full ranked alternatives or explicit progressive relaxation, bounded download attempts with clear exhaustion state. Force primary and preferred-tier failures; require lower-tier success and synchronized target/context/English/reference; test all unavailable. Lexical/sense suitability remains mandatory at every tier.
- **Missed checks:** successful fallback branch synchronization covers only surviving candidates. **Regeneration:** 4→B; A:delta; QA: all resolver branches; human: realized changed examples, no unrelated headword review. **Dependencies:** D09,D11,D18,P04,P05,P06,P11.

### D14 — Updated frequencies do not reposition new cards
- **FAIL · Medium · high confidence.** Location: 04 c26 note `due`, model sort field; `rank_import.log`. All due=0; after rank change rank9999 precedes rank1.
- **Cause → consequence:** insertion order works initially but reimport is not a scheduler migration. Learner harm: **no direct semantic harm**. Impact: F,K.
- **Action / regression:** explicit initial new-card positions plus documented/tested repositioning of **new cards only** on update. Merely setting `due` in a rebuilt package is insufficient proof. Test rank reversal in actual Anki queues; preserve learning/review due dates, intervals, repetitions and history.
- **Missed checks:** CSV sort/rank uniqueness and initial-import queue. **Regeneration:** B plus explicit user collection migration workflow; A:none; QA: import/scheduler; human: none. **Dependencies:** D08,P02,P10,P13.

### D15 — Stale CSV and partial production package
- **FAIL · Medium · high confidence.** Location: `final_anki_lexicon.csv`, `quran_vocabulary_test.apkg`, 04 c27. Ten current reviews unapplied; six headwords/nine definitions differ; only 100 packaged cards.
- **Cause → consequence:** independent exports and test build masquerade as current/full output. Learner harm: **yes**, outdated corrections or omissions. Impact: H,P,D,O,Q,E,A,T,K.
- **Action / regression:** versioned full-build mode with declared subset/full status and immutable manifest; compare expected approved ID set, fields and media against extracted package. Refuse stale input hashes. Do not solve by packaging today's broken full deck.
- **Missed checks:** successful package creation and declared full path. **Regeneration:** 4→B after upstream phases; A:validate/delta, full availability required; QA: all output comparisons; human: only content changed/unverified, not all merely repackaged rows. **Dependencies:** D01–D14 as applicable,D18,P05,P10–P14,D07 migration before release candidate.

### D16 — Historical plaintext credential exposure
- **Historical FAIL; current source PASS WITH CAVEAT · High · high confidence removal, exposure/rotation UNVERIFIED.** Location: original 01 c1 and any prior outputs/snapshots; current c1 uses environment variables.
- **Cause → consequence:** embedded credential could escape in shared source/archive. Learner harm: **no direct**. Impact: K (authenticated rebuild/access), not lexical content.
- **Action / regression:** establish exposure/rotation status; rotate/revoke if exposure cannot be ruled out; scan shareable files and Git history without printing secrets; verify missing-env failure is clear. Protect private archival evidence rather than publishing it.
- **Missed checks:** successful API authentication never proves secrecy. **Regeneration:** —; A:none; QA: credential hygiene only; human: none. **Dependencies:** Phase 0; resolve before authenticated ingestion or further sharing. No redundant credential-externalization work.

### D17 — Missing notices and unestablished distribution rights
- **FAIL for notices; UNVERIFIED for grants/compatibility · High · high confidence in absence, legal scope unresolved.** Location: 04 deck description/templates/package, source provenance records and release files; audit §9.
- **Cause → consequence:** a source label or public URL substitutes for a retained license, attribution and redistribution grant. Learner harm: **no direct**, but source replacement can change teachings. Impact: L; conditional source replacement affects all dependent domains.
- **Action / regression:** execute source work packages below; retain acquisition-date grants, attribution/exception inventories and component boundaries; machine-check notice coverage against content manifest. Obtain clarification where terms conflict; do not assert a blanket mixed-deck license.
- **Missed checks:** all technical/linguistic tests can pass without permissions. **Regeneration:** B for notices only; source replacement reruns earliest affected stage through B (01 for QAC/QF,03 for dictionary/QuranMorph evidence,04 for context; 02 if counts change). A:delta/replacement if recordings change; QA: rights inventory and all affected content; human: source-dependent changes. **Dependencies:** source usage inventory/P11. Start grant discovery in Phase 0; final distribution decision in Phase 6. Resolve source viability before investing in large-scale review.

### D18 — Combining-mark order defeats normalization
- **FAIL · Low · high confidence.** Location: 04 c14 `vocalized_compare_key`; `fault_checks.log` unequal keys for مُّقَرَّب and مُقَرَّب.
- **Cause → consequence:** fixed character offset assumes shadda precedes other combining marks after NFC; ranking preference fails. Learner harm: **low/indirect**, example quality. Impact: O,Q,E,A.
- **Action / regression:** inspect marks belonging to the first base character; test NFC/NFD and alternate mark ordering, preserving meaningful shadda elsewhere. Do not globally strip shadda to force equality.
- **Missed checks:** counts and valid Unicode strings. **Regeneration:** 4→B; A:delta; QA: normalization plus selection diff; human: changed examples only. **Dependencies:** P01 coordinate/display contract.

### P01 — Weak source alignment and null/duplicate guards
- **PASS WITH CAVEAT on current joins; FAIL for latent guards · High · high confidence guards are inadequate; no current permutation proved.** Location: 04 c1 `missing_quranic_words`, c4 QF deduplication/context map; 01 joins and 03/04 coordinate consumers.
- **Cause → consequence:** `astype(str)` hides NaN, dedup precedes uniqueness assertion, and counts cannot detect same-length permutations; source basmala/token conventions can drift. Learner harm: **yes if triggered**. Impact: I,X,M,F,O,Q,E,A,T.
- **Action / regression:** typed null/key constraints before conversion/dedup, conflict rejection, explicit source-coordinate/text reconciliation and versioned exceptions. Inject duplicate conflicting glosses, NaNs, swapped same-length tokens, unexpected basmala and changed merge conventions. Preserve raw source values.
- **Missed checks:** existing word-count assertions; audit stronger checks passed current snapshot. **Regeneration:** 1→3→4→B validation replay after contracts; no new network fetch required. A:none if outputs identical; QA: all joins/coordinates; human: only new residuals/changed outputs. **Dependencies:** Phase 0; precedes lexical fixes.

### P02 — Aggregation, frequency scope and tie stability
- **PASS WITH CAVEAT · Medium · high confidence current totals, future semantics unverified.** Location: 03 group aggregation (`IsParticiple`/voice/root/POS, frequency/rank), 02 historical denominator; 04 tags/rank consumers.
- **Cause → consequence:** first-value aggregation can hide future conflicts; ties depend on order; excluded affixes mean coverage is of selected segments, not comprehension. Learner harm: **possible** if morphology collapses; coverage claims mainly mislead expectations. Impact: I,X,M,F,T,K.
- **Action / regression:** assert group compatibility while allowing deliberate multi-POS identities; deterministic declared tie-break; derive denominator; describe excluded classes. Test mixed voice/root fixtures, shuffled inputs and sum/frequency/location-set identities. Current groups are consistent; do not invent new splits without evidence.
- **Missed checks:** current sums do not test conflict handling or environment/order changes. **Regeneration:** 3→4→B plus 02 if rank/count/report changes; A:delta only if examples change; QA: all aggregation/ranks/tags; human: only changed identity/morphology. **Dependencies:** D08,P01.

### P03 — Citation-form, homograph and sense policy incomplete
- **UNVERIFIED / PASS WITH CAVEAT · High · high confidence policy gap, item-level correctness unresolved.** Location: 03 candidate metadata; 04 headword/plural/definition selection and front template. Audit §7: 563 shared headwords, 498 shared headword+plural fronts, 15 numbered homographs.
- **Cause → consequence:** source IDs retain distinctions that matching/display may omit; weak verbs, gender, participles, proper names, collectives and function words require explicit conventions. Learner harm: **yes**. Impact: H,P,D,M,K; I only if separately approved identity change.
- **Action / regression:** expert-approved citation/sense policy; preserve numerical discriminator semantics; disambiguating learner cues where distinct fronts need them; retain attested plural-only/collective forms. Test stratified minimal pairs including PN/common nouns, derived/weak verbs, participles, إل/إلى-like spelling collisions and multi-function particles. Do not merge the 498 fronts automatically.
- **Missed checks:** unique Vocabulary IDs and dictionary coverage. **Regeneration:** 3→4→B if evidence contract changes; otherwise 4→B; A:delta; QA: collisions and morphology; human: unresolved policy strata/changed fields, expert approval of gold fixtures. **Dependencies:** D08,P02; policy precedes acceptance of D02–D05.

### P04 — Whole-word English cannot reliably define each lexical segment
- **UNVERIFIED semantic allocation; confirmed heuristic limitation · High · high confidence risk.** Location: 03 `clean_english_gloss`/definition evidence; 04 English context assembly; 486 multi-vocabulary orthographic words.
- **Cause → consequence:** regex removal cannot allocate whole-word meaning across segments; contextual negation/person can leak into a definition or be lost. Learner harm: **yes**. Impact: D,M,E.
- **Action / regression:** keep word gloss and lexical gloss separate; require explicit segment evidence or uncertainty; never infer a verified lexical meaning from cleanup alone. Test all 486 structurally and stratified linguistic cases including فِيمَا, bound pronouns and prefixes; compare word-level context order to coordinates.
- **Missed checks:** equal word/gloss counts and fluent-looking English. **Regeneration:** 3→4→B; A:none; QA: multi-segment allocation/negation; human: affected definitions and contextual sense conflicts. **Dependencies:** D08,P01,P03; feeds D05.

### P05 — Spoken audio identity and full availability unverified
- **UNVERIFIED · High · high confidence evidence is insufficient.** Location: 04 coordinate-derived URL selection/downloader, QF `Audio` paths, `network_sample.log`/`remote_audio.json`.
- **Cause → consequence:** provider paths and coordinate formula disagree (223/494 live sampled words); format/status cannot establish spoken identity; sampled provider path also returned 404. Learner harm: **yes if mismapped**. Impact: O,Q,E,A,K.
- **Action / regression:** listening-backed gold set and documented recording/token numbering contract, covering frequent/rare, multi-segment, basmala/merge verses, pause edges and fallbacks. Investigate disagreements against heard words; do not blindly prefer either URL scheme. Validate every packaged asset's availability/identity provenance; human-check unresolved mappings and changed recordings. A sample certifies its scope, not all recordings.
- **Missed checks:** 100 decoded MP3s, 44/45 successful responses and coordinate agreement are not listening. **Regeneration:** 4→B if mapping/selection changes, B if only bytes; A:validate/delta; QA: full media inventory; human: listening gold set plus unresolved/changed mappings. **Dependencies:** P01,D09,P04; verify permissible access under D17 before new downloads.

### P06 — Waqf span is not necessarily a complete semantic unit
- **PASS WITH CAVEAT · Medium · high confidence boundary implementation, linguistic sufficiency unverified.** Location: 04 c4 context boundaries/ranking. Four ordinary signs and ayah end are defensible; ignoring paired stops is conservative, not always minimal.
- **Cause → consequence:** short valid stop spans may be syntactically dependent; slash glosses are rough support, not polished translations. Learner harm: **possible**. Impact: O,Q,E,A.
- **Action / regression:** document context policy; preserve paired-stop relationships and mark dependent/truncated sense where needed; prefer semantically adequate context without inventing translation. Expert-test paired signs, no-stop/sakt, ayah endings and references extending beyond an explanatory clause.
- **Missed checks:** boundary and target containment assertions. **Regeneration:** 4→B only if spans/selection change; A:delta if target changes; QA: span validity; human: pause/syntax edge examples, not all unchanged lexemes. **Dependencies:** D11,P04,P03.

### P07 — Residual linguistic correctness is not certified
- **UNVERIFIED · High · high confidence coverage gap, unknown remaining error count.** Location: all final lexical fields; `stratified_samples.csv`, audit §7.
- **Cause → consequence:** neither matching statistics nor broad exported samples establish expert accuracy, especially rare words/polysemy. Learner harm: **yes**. Impact: H,P,D,M,O,Q,E.
- **Action / regression:** expert-curated gold fixtures and risk-based review beyond current QA flags; include top-frequency, hapax, verbs, nouns, particles/pronouns, participles, PN, weak forms, plurals, homographs, relaxed/strict matches, manual/QA and multi-segment strata. Record evidence and unresolved alternatives; no unsupported “fully validated” claim.
- **Missed checks:** all structural assertions and current review flags. **Regeneration:** 4→B for confirmed corrections, 3 too if evidence logic changes; A:delta only if examples change; QA: all rows; human: risk-ranked population, expanding when systematic failures recur. **Dependencies:** Phases 1–4 stable, D07. Gold-set preparation is earlier; mass review is Phase 5.

### P08 — Blank override cannot explicitly suppress automatic content
- **FAIL in schema capability · Medium · high confidence.** Location: manual CSV schema; `manual_review.py`, `qa_review.py`; 04 override selection. Blank means inherit; `:clear` removes override.
- **Cause → consequence:** a reviewer cannot persist “no plural” distinctly from automatic inheritance; commands may enter content (D06). Learner harm: **yes** if unwanted automatic values return. Impact: H,P,D,K.
- **Action / regression:** explicit per-field inherit/replace/suppress states, with required-field restrictions; versioned lossless migration. Preserve old blanks as inherit, never silently suppress. Test round-trip, literal colon input, clear, accept-as-is and intentional empty plural.
- **Missed checks:** nonblank precedence and basic CSV round-trip. **Regeneration:** 4→B only if resulting values change; A:delta for changed headwords; QA: schema and downstream values; human: ambiguous existing suppression intentions, not every blank. **Dependencies:** D01; finalize with D07 before Phase 5 saves.

### P09 — Concurrent review can lose updates
- **PASS WITH CAVEAT · Medium · high confidence mechanism; no observed lost concurrent decision.** Location: save paths in both review tools; duplicate handling differs (`manual_review.py` lacks equivalent guard).
- **Cause → consequence:** atomic file replacement prevents partial writes, not stale-reader overwrites. Learner harm: **indirect yes**. Impact: H,P,D,K.
- **Action / regression:** file-version compare-and-swap/locking with conflict resolution, duplicate-ID checks and append-only decision history; two-reader disjoint/conflicting edits must preserve both or reject stale write explicitly.
- **Missed checks:** atomic-save test and single-process QA duplicate check. **Regeneration:** —; A:none; QA: workflow tests; human: conflict resolution only. **Dependencies:** D01,P08; required before resumed editing.

### P10 — Source-ID and Anki split/merge migration undefined
- **PASS WITH CAVEAT for current GUIDs; UNVERIFIED migrations · High · high confidence gap.** Location: 01 IDs; 04 c26 GUID namespace, deck/model and 16-field schema; audit Anki logs.
- **Cause → consequence:** QAC IDs may change; reimport neither retires old notes nor resolves splits/merges. Field reordering can corrupt updates. Learner harm: **yes**, duplicate/stale/misassigned meanings. Impact: I,X,H,P,D,M,F,O,Q,E,A,T,K.
- **Action / regression:** immutable identity registry and explicit old→new mapping, retained aliases/tombstones, human adjudication of split/merge scheduling. Preserve deck 2059400110, model 1607392319 and namespace unless deliberate tested migration; freeze field order. Test unchanged, rename, split, merge and retirement in disposable real Anki collections; never silently delete studied notes or copy one review history to multiple new meanings.
- **Missed checks:** stable 100→4,875→4,875 imports only cover unchanged identities. **Regeneration:** B for schema/migration, upstream D08 stages for changed IDs; A:delta if media names/targets change; QA: GUID/schema/import fixtures; human: identity mapping, no blanket lexical rereview of unchanged IDs. **Dependencies:** design before D08 application; execute after identity registry settles.

### P11 — No realized-build provenance or stale-input guard
- **FAIL for provenance completeness · Medium · high confidence.** Location: 04 CSV export before c26 audio fallback; package fields `QuranicForm`/`OccurrenceGloss` store full contexts; audit package CSV comparisons.
- **Cause → consequence:** realized audio fallback can diverge from pre-fallback CSV; no persistent manifest captures exact segment/word, source hashes or selected recording. Learner harm: **possible** in debugging/review/update decisions; tested fallback display synchronization itself passed. Impact: O,Q,E,A,K.
- **Action / regression:** immutable build manifest with code/env/input/manual hashes, field provenance, planned and realized coordinates, segment, URL/byte hash and failures. Compare final exported rows to extracted package; simulate fallback and changed input during build. Prefer sidecar metadata first; schema additions require P10 migration.
- **Missed checks:** earlier CSV coordinate tests and successful package creation. **Regeneration:** 4→B; A:validate/hash, no redownload by default; QA: manifest consistency; human: realized example changes only. **Dependencies:** P01,P10 schema contract; implement before D12/D13 integration and D07 fingerprints.

### P12 — Cache identity does not track recording bytes
- **PASS WITH CAVEAT · Medium · high confidence missing policy; no observed hash collision.** Location: 04 media-name hash of Vocabulary ID/reference/path and cache reuse.
- **Cause → consequence:** changed bytes at same URL can retain stale local/Anki media; truncated name hashes have no collision guard. Learner harm: **possible**. Impact: A,K.
- **Action / regression:** record full byte hash, validate collisions, define refresh/version policy consistent with source terms; content-versioned media or explicit safe replacement semantics. Test same URL/new bytes, different URLs/same filename collision fixture, offline cached build and Anki media update.
- **Missed checks:** deterministic filenames and file existence. **Regeneration:** B; A:validate/hash and delta replacement; QA: cache/import; human: newly changed recording identity. **Dependencies:** P05,P11,D17 storage terms; integrates D12.

### P13 — Import options overwrite local fields/tags or retain stale fixes
- **PASS WITH CAVEAT · Medium · high confidence from backend experiments.** Location: Anki import workflow; 04 generated tags/fields; `anki_queue_check.log`, `anki_import_check.log`.
- **Cause → consequence:** always-update replaces local fields/tags; if-newer preserves newer local corrections even against deck fixes. Learner harm: **possible**. Impact: H,P,D,T,K.
- **Action / regression:** document supported import policy, backups and conflict review; distinguish generated location/NeedsReview tags from user tags and provide preservation workflow. Test user tag/edit survival or explicit warned replacement, stale NeedsReview removal, corrected fields and scheduling. Do not promise Anki merges tags automatically.
- **Missed checks:** total note count and no duplicate GUIDs. **Regeneration:** B only if generated policy/schema changes; A:none; QA: actual import modes; human: local conflict adjudication, not corpus-wide rereview. **Dependencies:** P10,D07 flag semantics; initial tests can precede final flags.

### P14 — RTL, labels, fonts and accessibility unverified
- **UNVERIFIED · Medium · high confidence testing gap.** Location: 04 model HTML/CSS; desktop/mobile clients. Escaping/RTL isolation exist; fonts are requested, not bundled.
- **Cause → consequence:** clipping, combining-mark rendering, night mode or ambiguous labels may mislead; audio is the highlighted orthographic word, not necessarily canonical headword/whole phrase. Learner harm: **possible**. Impact: H,P,Q,E,A,K.
- **Action / regression:** render on supported desktop/Android/iOS, night mode and long/difficult Arabic cases; label lexical headword, word audio and rough English distinctly; test keyboard/screen-reader playback. Bundle fonts only with permission. Keep field-order contract despite misleading internal names.
- **Missed checks:** backend SQL/HTML escaping and media existence. **Regeneration:** B for templates; A:none; QA: visual/playback fixtures; human: presentation acceptance, not lexical re-review unless text was misread. **Dependencies:** D11,P05,P10,P11; semantic labels required before review preview is trusted, cosmetic polish can wait.

### P15 — Portable/network rebuild not established
- **UNVERIFIED · Medium · high confidence limitation.** Location: notebook install magics, 01 API fetch/authentication, CAMeL resource installation, source snapshots and environment.
- **Cause → consequence:** unpinned packages/resources, changing APIs, token lifetime/retry gaps and order-sensitive processing can change or prevent results. Learner harm: **possible** if drift changes output silently. Impact: I,X,H,P,D,M,F,O,Q,E,A,T,K.
- **Action / regression:** lock supported environment/resources and source hashes; separate cached deterministic build from authorized acquisition; timeouts/retries/token refresh and all-or-nothing snapshot validation. Clean-install offline replay and mocked 401/429/timeout/partial chapter failure; live test only when permitted. Compare semantic package payloads, not timestamps/ZIP bytes.
- **Missed checks:** fresh-process replay in existing environment skipped installation and authenticated network ingestion. **Regeneration:** isolated 1→3→4→B validation, 02 when frequency outputs change; A:reuse fixture cache; QA: reproducibility/full diff; human: only changed content. **Dependencies:** D01,D16,P01,P02,P11,D17 acquisition/storage permission. Minimal reproducible test environment before review; broader acquisition tooling may follow.

### P16 — Pickle trust boundary undocumented
- **PASS WITH CAVEAT · Medium · high confidence general mechanism; no compromised artifact observed.** Location: 03 frozen `.pkl` writes and 04 reads.
- **Cause → consequence:** loading a replaced/untrusted pickle can execute code. Learner harm: **no direct linguistic harm**, integrity/security risk. Impact: K.
- **Action / regression:** restrict to locally generated hash-verified artifacts; document trust boundary and reject mismatched manifest before loading. Optional later migration to a safe typed interchange format must preserve nested evidence exactly. Test tampered/mismatched input rejection without executing payloads.
- **Missed checks:** dataframe invariants run after unsafe deserialization. **Regeneration:** — for validation policy; 3→4→B equivalence test if format changes; A:none; QA: manifest/serialization; human: none if equivalent. **Dependencies:** P11. Format replacement can wait; trust check cannot wait before loading outside artifacts.

### P17 — Private artifacts lack a demonstrated recovery path
- **UNVERIFIED recovery; confirmed Git exclusion · High · high confidence.** Location: `.gitignore`, manual CSV, frozen files, `audit_evidence/`, source/media inputs.
- **Cause → consequence:** source push excludes irreplaceable human decisions and reproducibility evidence. Learner harm: **indirect yes** if corrections are lost. Impact: H,P,D,K.
- **Action / regression:** Phase 0 private backup and restore drill, with manifest and permission-aware retention; later snapshot before each review/schema migration. Confirm restored 188 accepted decisions and notes against original hashes/values.
- **Missed checks:** clean Git status and successful push. **Regeneration:** —; A:none; QA: restore verification; human: none. **Dependencies:** none; first action.

### P18 — Documentation and inactive paths obscure supported behavior
- **PASS WITH CAVEAT · Low · high confidence.** Location: README, stale notebook comments, older 03 copy, unused helpers, output path/test/full naming, 02 coverage descriptions.
- **Cause → consequence:** users may run destructive/obsolete paths, mistake a test deck for a full release, or infer comprehension coverage. Learner harm: **indirect possible**. Impact: F,K,L.
- **Action / regression:** document active 01→03→04 pipeline, optional02, source acquisition, subset/full modes, limitations, review/update policy and release status; archive experiments visibly. Implement the required structured-Python migration M01; defer unrelated cleanup. Documentation checks must agree with actual manifest and command paths.
- **Missed checks:** code execution does not validate instructions. **Regeneration:** — for documentation; A:none; QA: documented workflow smoke test after fixes; human: none. **Dependencies:** final policies/D15/D17; early warning preservation in Phase 0.

## D17 source-specific work packages

These inherit D17's severity, confidence qualifications, missed checks and regression requirements. They are separate completion gates, not evidence that every source has identical restrictions. External findings below reuse the audit's primary-source research; current terms do not prove the historical acquisition grant. Record the actual grant/version before deciding applicability. Source replacement may make earlier phases necessary again.

| Work package / verdict | Exact affected stage and root issue | Remedy and acceptance evidence | Regeneration / review / dependencies |
|---|---|---|---|
| D17-Tanzil: FAIL notices; UNVERIFIED modification scope | `quran-uthmani.txt` → 04 c4/template; stripped annotations and missing complete notice | Retain [Tanzil notice/link](https://tanzil.net/docs/text_license); resolve excerpt/highlighting/modification treatment alongside verbatim conditions. Preserve original source and D11 display spans. | Notices: B, no audio/lexical review. Text changes: 4→B, QA span diffs, human pause-edge confirmation; A:delta only if target changes. Depends D11/P11. L,Q; possible learner harm from text handling, not missing notice itself. |
| D17-QAC: FAIL attribution; UNVERIFIED combined scope | `quranic-corpus-morphology-0.4.txt` → 01/03; GPL/download/FAQ and embedded older Tanzil notice not reconciled | Retain [download terms](https://corpus.quran.com/download/), [GPL page](https://corpus.quran.com/license.jsp), [FAQ](https://corpus.quran.com/faq.jsp) and local notices; clarify restrictions on raw versus derived data and applicable historical grant. | Notices B; replacement 1→3→4→B plus02, QA all identities/counts, human changed meanings/IDs; A:delta. Depends D08/P10/P11. L only unless source changes. |
| D17-QF-data: UNVERIFIED grant/storage compliance | `QF_Database.csv`, gloss/location metadata, 01 acquisition, 03/04 and backups | [Developer terms](https://api-docs.quran.com/legal/developer-terms/) researched as updated 2026-10-11 require separate licensing for content-package redistribution and constrain long-term storage/offline sync. Determine applicability and written permission; free distribution is not automatically exempt. | Grant/notices B if required; replacement 1→3→4→B,02 if counts change, QA coordinates/English/tags, human changed definitions/context; A:delta if coordinates change. Depends P01/P11/P15. L; storage/access can affect personal use too. |
| D17-audio: UNVERIFIED redistribution rights | 04 downloader, `anki_media*`, APKG audio; public CDN access is not a grant | Obtain recording-specific license/attribution and permitted caching/distribution; [QF audio docs](https://api-docs.quran.com/docs/sdk/javascript/audio/) and [Quran.com website terms](https://quran.com/terms-and-conditions) are not interchangeable grants. Use a licensed replacement if necessary. | B or4→B if examples change; A:replace affected recordings, full audio QA/listening identity; human changed audio/examples. Depends P05/P12/P11. L,A; permission alone does not affect memorized meaning. |
| D17-QuranMorph/Qabas: UNVERIFIED | `quran-morph.csv` → 03/04 auxiliary lexical/display evidence; local acquisition license absent | Recover actual grant/version from [QuranMorph](https://sina.birzeit.edu/quran/)/[Qabas](https://sina.birzeit.edu/qabas/). Institutional form/open-resource descriptions or third-party CC claims do not settle rights. Clarify retention of derived evidence. | Notices B; source removal/replacement 3→4→B, QA all candidate/headword diffs, human affected fields; A:delta. Depends D02/D03/D09/P11. L unless source changes. |
| D17-Wiktionary/Kaikki: FAIL attribution packaging; UNVERIFIED local provenance/exceptions | Kaikki JSONL → 03 entry matching → 04 headword/plural/definition | Preserve entry/page history attribution, snapshot lineage, modifications and applicable share-alike notices/exceptions under [Wiktionary copyrights](https://en.wiktionary.org/wiki/Wiktionary:Copyrights), [Wikimedia §7](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). [Kaikki current page](https://kaikki.org/dictionary/Arabic/index.html) does not identify local snapshot automatically. | 03 provenance export→04→B; unchanged text needs no human rereview, missing identity provenance may require candidate review; A:none unless example changes. Depends D02/P11. L; a replacement affects H,P,D. |
| D17-CAMeL: UNVERIFIED output/distribution scope | 03 CAMeL diagnostics, frozen evidence and local installed database | Inventory software versus database versus output. [Official package list](https://camel-tools.readthedocs.io/en/latest/reference/packages.html) identifies MSA morphology database GPLv2; clarify scope before sharing frozen resources. Current outputs are evidence, not directly selected card definitions. | Notices/packaging only if evidence unchanged; 03→04 equivalence QA if removed/replaced, B only for changed deliverable; A:none, human only changed derived decisions. Depends P11/P15. L only for unchanged content. |

Before any release, map every bundled field/asset to its source/grant/notice; determine component-license boundaries and compatibility with appropriate clarification. Do not publish a blanket license or raw evidence dump to solve attribution. Source viability investigation starts early so late licensing failures do not force avoidable re-review. Final clearance remains Phase 6.

## Remediation phases and exit gates

### Phase 1 — Data identity and pipeline correctness

Execute M01-B/C package extraction alongside this phase, separating parity evidence from intentional corrections. Implement P01's typed contracts and source-coordinate checks; settle D08's pronoun/affix policy with a proposed old/new mapping and P10 migration design **before applying it**. Fix D10 evidence parsing, D09 orthographic authority, P02 aggregation/rank scope. Recompute from protected inputs only after D01 is safe. Preserve raw data and record exceptions, not ad hoc silent edits.

Exit: every source coordinate accounted for; duplicates/nulls/conflicts rejected; all ID changes explained; no accidental homograph merge; frequencies sum to the declared population; tag occurrence sets exact; deterministic ties; old/new diff manifest. Unexpected count differences block progression. No fixed requirement to retain 4,875 after approved policy correction.

### Phase 2 — Linguistic correctness

Move lexical production logic into M01's `lexicon/` modules with a historical cell map and isolated fixtures. Agree P03 citation/sense conventions and expert gold cases. Repair D02/D03 jointly around one accepted lexical identity with morphology evidence. Implement P04 segment/gloss distinction and D05 semantic definition policy, then D04 plural linkage/suppression. Preserve ambiguity as review-needed; never use a dictionary source label as proof. Prepare D06 anomaly fixtures now, but save final review confirmations only through Phase 5's migrated workflow.

Exit: all named wrong-word/form/voice/plural/sense regressions fail closed or have independently justified correct values; all changes have provenance. All automatic plural assignments and risky definitions are queued for validation. A smaller queue is not an acceptance criterion.

### Phase 3 — Occurrence/context/audio correctness

Extract M01's `context/` and `media/` boundaries before concurrent edits; no package export may secretly download or change an occurrence. Implement D11 display preservation, D18 Unicode ranking, P06 context policy; establish P05's listening-backed mapping. Implement P11 realized manifest foundation and P12 cache identity, D12 validated atomic downloads and D13 complete fallback ordering. Run ranking offline; do not place thousands of availability probes inside lexical selection. Resolve media during a controlled, permitted packaging step.

Exit: selected lexical segment belongs to declared lexeme; highlighted orthographic token, Arabic/English span, reference and heard word agree for the gold set and every unresolved mapping. All packaged media pass validation; unknown audible identity remains explicitly pending. Full failures/realized fallbacks are recorded. If audio is intentionally omitted for a review candidate, label it as such and do not approve audio fields.

### Phase 4 — Anki/package/rebuild integrity

Complete M01-D/E: end-to-end CLI, parity/delta evidence, thin notebook cutover and R18. Complete P10 identity/schema migration and P13 import contract; D14 new-card order; P11 field/package provenance; P12 media updates; P14 meaningful labels/RTL preview. Produce D15's candidate full package from stabilized fields in a disposable collection, not a release claim. Complete the minimum P15 reproducible environment and P16 trust checks used for that build.

Exit: expected notes/fields/tags/media reconcile to manifest; unchanged IDs retain GUIDs; split/merge/retirement behavior explicit; repeated imports have no unintended duplicates; local edits/tags and scheduling behave as documented; actual new-card queues follow intended rank after supported migration; supported clients render essential content legibly. Media or schema failures block affected review acceptance.

### Phase 5 — QA and human-review workflow

Finalize P08/P09 and D07; migrate decisions on a copy, preserving old values/history. Run all automatic checks on the entire new population. Perform D06's targeted confirmation of all 188 accepted rows; prioritize the 20 doubled-letter anomalies and command/English contamination without assuming those are the only errors. Then resume the 90 pending rows and expanded P07 queue, organized by risk and frequency.

**Migration rules:**

- Preserve explicit manual values, notes and historical acceptance even when current approval expires. A decision's history and its validity for the new card are different records.
- Legacy `Reviewed=True` has no evidence fingerprint. Reconstruct the old automatic values from retained inputs/replay where possible. If unavailable, mark acceptance provenance unknown rather than fabricating a hash.
- One-to-one unchanged ID, same manual override, same supporting lexical identity/morphology and same relevant content: carry forward after the targeted legacy check. Pure notice/template changes do not invalidate lexical decisions.
- Blank overrides inherit automatic content. Changed headword/plural/definition or its supporting identity/sense invalidates that field's acceptance. A changed function implementation with provably identical relevant evidence/content need not trigger blanket rereview.
- A changed citation form can alter plural/definition compatibility and occurrence ranking: invalidate dependent fields, not just changed text. Conversely a different compatible example does not automatically invalidate an unchanged well-supported definition.
- Identity split/merge/exclusion requires a reviewed mapping. Never duplicate overrides or approvals blindly across children; retain retired decisions separately. Frequencies/tags changing alone need automatic checks, not lexical rereview.
- Changed target/span/gloss/audio invalidates example/audio acceptance; unchanged lexical approvals remain if semantically compatible. Store planned and realized choices so fallback cannot bypass this rule.
- New confirmed corruption or conflicting evidence overrides an old acceptance even if the string itself did not change. Preserve the original, record the correction reason.
- Explicit suppress/inherit migration must be lossless. Existing blank plural cannot be inferred to mean suppression. Resolve ambiguous intentions with the reviewer.

**Safe resume point:** Phases 1–4 contracts and automated gate below pass, legacy migration is reversible, gold-set semantic/audio blockers are addressed, and review preview shows the exact versioned evidence/fields to be approved. Isolated unresolved rows can remain quarantined in a stable queue; they must not be silently approved or included as trusted cards. Source replacement decisions likely to invalidate review must be settled first. Final public distribution permission need not delay private review when lawful source use is established.

### Phase 6 — Distribution/readiness

Complete D17 notices/grants and compatible source boundaries; P18 supported-workflow documentation; release manifest, checksums and clear version/subset status. Build a fresh full artifact after accepted corrections and compare it with the approved manifest. Keep unverified rows out of a “validated” release or clearly separate the experimental population without implying NeedsReview catches everything. M01 notebook-to-package cutover must already be complete; optional further refactoring, safe-format conversion and cosmetic font polish follow correctness. Any replacement source reopens its upstream phase and dependent approvals.

## Structured Python migration — M01

**Required implementation workstream, not an additional confirmed audit defect.** This extends P15/P18 and makes the test boundaries required by P01/P11 explicit. The notebook-to-Python conversion is now part of the remediation critical path, not deferred cosmetic refactoring. The conversion itself does not establish correctness; it must expose the existing behavior, then incorporate separately traceable fixes.

### Target workflow and ownership

Use one installable Python package with a small CLI, explicit stage inputs/outputs and isolated tests. Keep notebooks as optional read-only exploration/reporting clients of the package. Do not maintain duplicate production logic in notebooks and modules. Do not simply export each notebook to a monolithic `.py` script that retains globals, notebook execution order and unconditional writes.

Proposed layout (names are a design proposal, not files created by this plan):

```text
pyproject.toml                    package, CLI entry point, test configuration
<dependency lock>                one chosen supported tool and locked resources
src/quran_vocab/
  cli.py                         explicit commands and exit status
  config.py                      paths/options; secrets only from environment
  contracts.py                   versioned records and stage contracts
  artifacts.py                   manifests, hashes, atomic stage publication
  sources/                       QAC/QF/QuranMorph/Kaikki/Tanzil readers
  corpus/                        coordinates, inclusion/ID map, joins, counts
  lexicon/                       evidence, candidates, headwords/plurals/senses
  context/                       display spans, waqf, ranking, English alignment
  media/                         URL mapping, download/cache/validation
  anki/                          fields/GUIDs/tags/templates/package manifest
  review/                        durable decisions, migration, QA, review CLI
  reports/                       optional frequency/coverage reports
notebooks/                       thin optional analysis clients after cutover
tests/                           unit, contract, regression, integration tests
```

Keep raw snapshots, private decisions and generated builds in separately configured directories; do not move ignored/private data into a publishable package. Stage records must distinguish lexical-segment identity, orthographic coordinate, accepted dictionary entry/sense, planned example and realized audio example. Dataframes may remain internally; a validated schema at each stage boundary is sufficient. A new database, task scheduler, web UI or distributed execution framework is not required.

Proposed command contract, to implement and test later:

| Command family | Replaces | Required behavior |
|---|---|---|
| `quran-vocab acquire …` | 01 online fetch | Explicit permitted network operation; produces a complete versioned raw snapshot, never silently runs during offline build. |
| `quran-vocab corpus …` | 01 parsing/join | Consumes declared local snapshots; emits validated coordinates, included segments and ID-map version. |
| `quran-vocab evidence …` | 03 | Produces frozen lexical evidence and a separate proposed queue; never writes durable human decisions. |
| `quran-vocab finalize …` | 04 lexical/context selection | Consumes evidence plus a specified decisions revision; produces canonical fields, QA reasons and planned examples offline. |
| `quran-vocab media …` | 04 audio resolution | Explicit network/cache policy; emits validated media and realized examples with manifest. Does not mutate lexical decisions. |
| `quran-vocab package …` | 04 genanki export | Consumes realized manifest; offline packaging; full versus subset mode explicit. No hidden downloader/fallback inside export. |
| `quran-vocab validate …` / `diff …` | audit/QA checks | Machine-readable results, nonzero failures, old/new field/evidence diffs; no approval mutation. |
| `quran-vocab review …` / `review migrate …` | review scripts | Explicit decision writes with version checks/history; preview exact candidate revision; migration starts in dry-run mode. |
| `quran-vocab report frequency …` | 02 | Descriptive report against declared population; not a build prerequisite. |
| `quran-vocab build …` | ordered pipeline | Thin orchestration of explicit stages; default offline, no decision writes or acquisition. Requires resolved media manifest/cache or an explicitly labeled no-audio candidate mode. |

Every command must accept explicit configuration and output location, operate from any working directory, avoid import-time work, and refuse accidental overwrite of protected inputs. Publish complete stage directories atomically where feasible; distinguish failed/incomplete runs from usable outputs. Cache keys include relevant input/code/config/schema versions. Resume only matching completed stages; a changed decision revision invalidates downstream finalization/media selection/package, not raw-source ingestion. One writer owns each build directory. The generic build command does not automatically approve reviews, migrate user Anki collections or distribute artifacts.

### Migration sequence and proof obligations

| Step | Placement | Deliverable / acceptance gate |
|---|---|---|
| M01-A — Capture and design | Phase 0, after snapshot | Cell→module/function map, stage graph, I/O schemas and side-effect inventory. Identify c37 decision overwrite, network calls, credentials, notebook magics and global state. Primary signs off contracts before parallel edits. |
| M01-B — Skeleton and adapters | Early Phase 1 | Package/CLI, config, manifests and isolated-output harness; retain current input formats initially. Extract 01/03 computational stages and separate optional02 reporting. No bulk source refresh or storage-format conversion. |
| M01-C — Characterize then fix | Phases 1–3, one stage at a time | Run extracted logic against retained baseline artifacts; compare field/evidence values and coordinate sets. Separate extraction changes from intentional D/P fixes. Extract 04 into lexical, context, media and package boundaries before agents change those areas. |
| M01-D — Integrate command pipeline | Phase 4 | End-to-end offline candidate build from CLI, explicit permitted media preparation, real Anki checks, locked environment and stage-resume tests. Review scripts call shared review library; compatibility wrappers may remain. |
| M01-E — Cut over | Before Phase 5 resume | CLI is authoritative; notebooks become thin consumers with no independent writers/matchers/builders. Old implementation retained in protected history, clearly obsolete. R18 passes and documented workflow is usable without Jupyter. |
| M01-F — Retire transitional code | Phase 6 or later | Remove redundant compatibility paths only after migration validation; optional safe-serialization migration and further cleanup remain separate. |

**Parity is a migration test, not a correctness target.** Compare unchanged behavior against the existing audit outputs without repeating the entire old audit. Where the old implementation is defective, first characterize it in isolated fixtures, then assert the corrected behavior and record the authorized difference. Never restore D01's overwrite or a wrong headword merely to obtain byte-for-byte parity. For a stage extracted and corrected in one branch, retain separate commits/test evidence for extraction and correction, with an explicit difference allowlist. A full baseline rerun is justified only if stored evidence cannot establish the needed comparison.

Notebook cell numbers remain valid historical evidence references. Maintain a migration map containing notebook/cell, new module/function, associated D/P IDs and test IDs so future reviewers can trace every moved decision. Preserve existing CSV/ID/GUID/field-order contracts until a separately tested migration changes them. An import or `--help` command must not load large corpora, download media, create output files or mutate decisions.

**Regeneration cost:** one integrated parity pass per extracted stage plus the already planned corrected recomputation; reuse those outputs across workers. Packaging compares semantic payloads because timestamps/ZIP layout may differ. Equivalent extraction alone causes **no human re-review** and no audio redownload. Any changed normalization, ordering, defaults, data types or evidence must be investigated as a behavior change and use the existing field-level invalidation rules. Do not invalidate all approvals merely because function paths changed.

**Rollback:** retain immutable pre-cutover sources and artifacts; select a prior build manifest, not an arbitrary mix of old frozen tables and new decisions. Rollback cannot overwrite later human work; incompatible decisions remain preserved for migration. Notebook production execution stops at cutover; investigation can still use thin notebooks against declared artifacts.

## Parallel-agent implementation plan

Persistent execution instructions are in `AGENTS.md`. The request **“use a total of four agents as we've discussed”** selects the primary-plus-three-worker roster below, within dependency/capacity limits. `AGENTS.md` also records standing authorization for reasonable commits, pushes at completed steps, and frequent recovery checkpoints. These defaults do not authorize unrelated implementation or data/deck publication.

### Capacity and model policy

**Recommended working team: three agents total for most engineering waves; up to four total at well-separated peaks.** This session exposes four concurrent slots **including the primary**, so the maximum is one primary plus three workers, not four workers plus a coordinator. Start with two total during contract design and use one during final adjudication. Recheck available capacity when implementation starts; this is a session observation, not a universal account limit.

The dependency chain and shared notebooks prevent useful parallel execution of all six phases. Four agents are reasonable only after contracts and module/file ownership are fixed. Do not assign one agent to each notebook: 04 contains several dependent domains, 02 is not critical, and 03 writes human decisions. Adding agents also increases duplicated context and integration work; no linear speedup or token-saving guarantee is assumed.

Model names below are available in this session's tool catalog. Effort levels are **task-specific recommendations**, not benchmark claims or pricing estimates. Official [OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents) supports bounded parallel tasks, explicit model/effort selection and caution with concurrent writes. The four-slot ceiling comes from this session, not that documentation.

Preserve the original division of responsibility: **primary Astra owns new evidence evaluation, Arabic linguistic judgments, source/legal-risk interpretation, unresolved defect identification and final correctness/readiness verdicts**. Workers implement specified contracts and tests; they report unexpected discrepancies for primary investigation rather than deciding new linguistic policy. Expert human Arabic/listening review and rightsholder clarification remain necessary where the audit requires them. The present request authorizes planning this engineering delegation; no agents or implementation jobs are launched by this document.

| Role | Model / reasoning effort | Main objectives and bounded ownership | Must not decide |
|---|---|---|---|
| A — Primary architect and auditor | **GPT-6 Astra (`gpt-6-astra`), High**; temporarily Extra High (`xhigh`) for contested identity/morphology, migration or rights decisions | Own contracts, cell→module map, D08/P03 policies, gold expectations, source-rights interpretation, integration, change/review invalidation and final gates. Own shared schemas/config/lockfile and authoritative plan/checkpoint. | Cannot replace external linguistic/listening evidence or grants with model confidence. |
| B — Pipeline migration engineer | **GPT-6.1 Sol (`gpt-6.1-sol`), High** for extraction/contracts; Medium for routine adapters after contracts stabilize | M01 package implementation in assigned modules; extract corpus/evidence then lexicon functions, implement D01/P01/D10/P02 and specified D02–D05 corrections. Supply parity/diff evidence and precise source map. | No independent lexeme merging, Arabic correction, source substitution or approval of unexpected parity deltas. |
| C — Review/artifact engineer | **GPT-6.1 Sol, High** for lossless review/Anki migrations; Medium for manifests/CLI wiring under a fixed schema | Own `review/`, then `anki/` or artifact modules as assigned; P08/P09, D07 implementation, P10/P13/D14 specified behavior, durable decisions and import fixtures. Modules are handed over explicitly between waves. | No blanket invalidation of old reviews, deletion of studied notes, or reinterpretation of accepted linguistic decisions. |
| D — Test or media worker, rotating slot | **GPT-6.1 Sol, Medium** for transcription of established fixtures/CLI tests; High for specified media resolver/cache integration | Own assigned `tests/` partition or `media/` implementation, never both sides of the same acceptance oracle without primary verification. Build R01–R18 fixtures from audit evidence, mocked faults, isolated import runs and manifests; later D12/D13/P12 against approved mapping. | No claims that HTTP200/decoder success proves pronunciation; no independent legal or semantic gold expectations. |
| Editorial role — substitutes for an idle worker, not a fifth slot | **GPT-6.1 Sol, Low** | Format already-established findings, migration maps, API usage docs and release notes. Return edits for primary verification. | No new audit judgment, policy invention or final readiness conclusion. |

Use the High setting where state preservation or multi-stage contracts require careful implementation. Drop to Medium once behavior is precisely specified and the task is bounded; use Low for editorial work only. Do not use Max/Ultra by default. If a worker is blocked on an unresolved Arabic/identity/source issue, return it to A rather than increasing worker effort and letting it invent policy. Do not automatically substitute a cheaper model for substantive primary judgment.

### Execution waves and maximum useful concurrency

Counts include A. Each wave has an integration gate; workers may prepare fixtures downstream using frozen contracts, but cannot approve downstream outputs before prerequisites land.

| Wave / phase | Agents at once | Main objectives and disjoint outputs | Gate before next dependent work |
|---|---:|---|---|
| W0 — Protection/contracts (Phase 0) | **2: A+B** | A: snapshot/restore, credential/rights triage, ID/schema decisions. B: read-only cell/function/side-effect inventory and draft migration map in a separate document. A alone performs protected state operations. | Phase 0 backup proven; shared contracts approved. |
| W1 — Safe extraction foundation (early Phase 1) | **3: A+B+C** | A: schemas/config/package bootstrap and identity-policy decisions. B: approved corpus/evidence extraction, D01 safe queue output. C: review persistence adapter and preservation tests on copied fixtures. A serializes changes to central files. | Extracted stage parity, R01/R02, no decision writes from build; D08 migration design approved. |
| W2 — Data and lexical correction (Phases 1–2) | **3 normally; 4 only for isolated tests** | A: linguistic gold/policy and discrepancy evaluation. B: corpus corrections, then lexicon implementation in approved order. C: P08/P09 workflow and manifest plumbing against frozen schema. Optional D: already-specified contract/gold fixture harness in `tests/contracts/` and `tests/regression/`. | Phase 1 then Phase 2 gates; all new semantic outcomes reviewed by A. Test fixtures cannot outrun approved expectations. |
| W3 — Context/media/package boundaries (Phase 3, Phase 4 preparation) | **4: A+B+C+D** | A: audio mapping/waqf evidence and integration. B: `context/` extraction and D11/D18/P06 changes. C: `anki/` extraction/schema/import fixtures using immutable synthetic manifests. D: `media/` D12/D13/P12 implementation using agreed candidate-list and realized-record contracts. | Context/media oracle approved; integrated fallback synchronization and provenance pass. No live shared-cache writes. |
| W4 — End-to-end and Anki acceptance (Phase 4) | **3: A+C+D**, B idle unless a bounded defect needs repair | A: integrate and run the single full candidate pipeline. C: Anki migration/order/update tests in its own disposable collection. D: CLI/package-isolation/render fixtures against a fixed candidate revision. | R13–R16 and R18; essential client checks; notebook cutover accepted. |
| W5 — Review migration/resume (Phase 5) | **2: A+C**, optionally a third Low editorial worker | A: invalidation decisions and legacy linguistic confirmation with reviewer. C: migration dry-run, lossless comparisons and approved queue generation. Editorial worker documents approved instructions only. | R08/R09, reversible migration, targeted 188-row confirmation; human queue can resume under stated gates. |
| W6 — Release (Phase 6) | **2–3: A + test worker + optional Low editor** | A: grant/notice sufficiency and final verdict. Worker: fixed release artifact checks. Editor: approved notices and usage docs, no legal interpretation. | Full rights/readiness gates and approved release manifest. |

### Coordination, integration and cost controls

- One owner per module/file per wave; A owns shared `contracts.py`, configuration schema, `pyproject.toml`, dependency lock, migration registry and integration decisions. Workers request contract changes before implementing incompatible assumptions. Pure integration work is serial.
- Prefer explicitly created isolated worktrees/branches for workers. This environment otherwise shares a filesystem: spawning does **not** imply isolation. If worktrees are unavailable, enforce disjoint write sets and agent-specific output directories. Do not concurrently edit the same notebook, CSV, cache, SQLite/Anki collection or generated build directory.
- Each task brief names finding/test IDs, approved behavior, input artifact hashes/schema revision, editable files, forbidden writes, expected output and stop condition. Give short relevant excerpts and fixture paths, not the entire audit conversation. Use explicit model and effort settings; for this tool's overridden model spawning, provide a fresh task context (`fork_turns="none"`) with the complete bounded brief.
- Agents may implement mechanical tests and report failures, but A evaluates novel implications. Every return includes changed files, exact checks run/results, fixture provenance, intentional output deltas and unresolved issues. A reviews patches and integrates dependency-first. Passing worker tests alone does not approve a semantic fix.
- One coordinator runs each expensive full replay/build. Other workers use small immutable fixtures and the same approved candidate artifact. No duplicate network audits, full corpus runs or large-scale samples without a specific evidence gap. Network acquisition/media validation and user-facing review writes have a single owner.
- Version test inputs and expected results separately from implementation. Never let a worker update gold expectations simply to make its patch pass. Unexplained parity changes stop that branch; retain evidence for A.
- Use short per-worker handoff files in isolated workspaces. A alone updates `AUDIT_PROGRESS.md` with accepted results, artifact hashes and exact next steps. Commit approved batches separately: extraction, defect correction, data/decision migration and packaging. Never commit excluded private data merely to share it between agents.
- Keep workers idle when the critical path is policy review or integration. Do not launch nested subagents to exceed the four-slot ceiling. Reassign a finished slot to tests or Low-effort editorial work only when there is independent useful work.

**Recommended default deployment:** A (Astra High) + B (Sol High) + C (Sol High); add D only in W2's isolated fixture work or W3's genuinely separate context/media/package work. Human approval and expert review remain outside this agent count and cannot be accelerated simply by spawning more agents.

## Exact recommended implementation order

This order avoids the dependency cycles created by implementing review approval before deciding what a card means. “Design” steps do not mutate the production inventory.

1. P17/Phase 0 private restore-tested snapshot; separate current/historical manifests; D16 exposure disposition.
2. M01-A cell/module/side-effect map and approved stage contracts; M01-B package skeleton with protected outputs. D01 decision-preserving queue; prototype lossless P08/P09 schema/history handling. Coordinate W0–W1 before parallel code edits.
3. Start D17 grant/source-viability inventory. Choose sources suitable for intended use before expensive new review; defer final notice packaging.
4. Extract 01/03 stages under M01-C with parity evidence, then implement P01 typed input/join/coordinate contracts; retain all raw-source exceptions and gold fixtures. Keep optional02 as a package-backed report.
5. Design D08 inclusion/identity policy and P10 old→new migration; approve mappings before applying them.
6. Apply D08, D10, D09 and P02; isolated 01→03 validation and optional02 regeneration; inspect ID/count/source diffs.
7. Extract 04 lexical/context/media/package boundaries with traceable parity checks (M01-C). Define P03 linguistic conventions and P04 segment evidence; repair D02/D03 candidate identity/morphology together.
8. Repair D05 definitions and D04 plurals; collect D06 fixtures, preserving manual values. Compare complete lexical output and provenance.
9. Implement D11, D18, P06 context/ranking; verify coordinate/text/gloss spans.
10. Establish P05 audio mapping gold set; implement P11 realized manifest and P12 cache contract, then D12/D13; validate available media under permitted access.
11. Complete P10 package migration, P13 import behavior and D14 new-card repositioning; verify 16-field contract, tags and media updates in real Anki.
12. Complete P14 semantic labels/essential render checks, P15 reproducible candidate environment, P16 trusted artifact guard; M01-D CLI end-to-end build produces D15 candidate full package. Compare manifest, pass R18 and perform M01-E notebook cutover before review resumes.
13. Finalize D07/P08/P09 fingerprinted, conflict-safe workflow; run the full gate; migrate and confirm D06's 188 legacy rows. Resume remaining and P07 expanded review only now.
14. Apply reviewed corrections through versioned 04 builds; rerun affected automatic tests plus full release checks; never reuse an approval across a material evidence change.
15. Finish D17 permissions/notices, P18 documentation, release reimport checks and final full package. M01-F transitional cleanup and unrelated refactoring follow.

## Blocking findings before further manual review

- **Workflow blocker:** M01-E CLI cutover and R18 must pass; notebooks cannot remain an alternate source of production logic. Equivalent extraction alone does not invalidate human decisions.

- **Absolute protection blockers:** P17 and D01; migrated review writes must satisfy P08/P09. No destructive production rebuild beforehand.
- **Generation blockers:** D08/P01/P02/D09/D10 before lexical review; D02–D05/P03/P04 before accepting headword/plural/definition decisions. Broad source replacement still under consideration is also a review-investment blocker.
- **Evidence/preview blockers:** D11–D13/D18/P05/P06/P11/P12 and essential P14 labels for accepting complete cards with audio/context. An explicitly scoped text-only investigative review may collect evidence, but is not resumed full-card approval.
- **Persistence blockers:** P10/P13/D14 and candidate D15 integrity must demonstrate stable imports; D07 cannot bless rows before their schema/evidence contract stabilizes.
- **Legacy blockers:** D06 anomalies and unsupported legacy approvals must be quarantined or confirmed. P07 is the continuing substantive review task, not a reason to demand that all future human judgments already be complete before opening the queue.

## Findings that can safely wait

Final publication notices and grant packaging can wait until Phase 6 **only if current acquisition/storage and source viability are resolved**. They still block public release. The M01 structured-Python migration cannot wait until release: it must reach tested CLI cutover before Phase 5. Unrelated refactoring, inactive-helper cleanup, a full pickle-format replacement, cosmetic font enhancements and acquisition-interface polish can wait. P18's accurate safety/workflow instructions and P16's trust guard cannot. Audio listening, semantic corrections and content-sensitive approval expiry cannot be reclassified as polish. D14 can wait for a text-only preview but must precede trusted package/update acceptance.

## Personal-use versus distribution effects

Personal trusted learning is affected by D02–D13, D15,D18 and P01–P14; D01/P17 can destroy corrections, D14 affects study order, P15/P16 affect rebuild integrity/security. D16 concerns credential access rather than memorized Arabic. A reviewed, clearly bounded subset may become personally usable sooner than the entire population, with any unvalidated audio omitted/labeled rather than implied correct.

Missing redistribution attribution/notices, public-package grants, share-alike packaging and component-license compatibility are **distribution-only when source acquisition/storage is already lawful and content is unchanged**. They do not make a definition linguistically wrong. D17 is not wholly distribution-only: QF storage/access, acquisition restrictions and possible source replacement also affect personal workflows. Personal use is not assumed to override source terms. Public release requires all technical, linguistic and rights gates; a free deck is still distribution.

## Expected regeneration and re-review cost

| Work | Expected scope and cost control |
|---|---|
| Backup/protection | Copy/hash existing artifacts and restore-test; no card regeneration. Audit evidence alone is approximately 646 MB; inventory all media/input sizes rather than estimate total. Git does not hold these. |
| Python migration | M01 adds extraction/contract tests and one shared parity pass per stage. Reuse recorded audit artifacts and corrected build outputs; equivalent movement causes no re-review/audio redownload. Integration overhead prevents assuming linear gains from agent count. |
| Data pass | One controlled cached 01→03 pass after identity/contracts stabilize, optional02; retain old/new ID map. Avoid repeated API acquisition. 128,219 raw QAC segments and 77,429 words are the audited baseline scale. |
| Lexical pass | Full 03 evidence and 04 automatic recomputation for ~4,875 baseline IDs; several cheap isolated fixtures before full pass. All automatic plurals and all definitions receive QA. Changes may affect far more than the original unmatched queue. |
| Context/package pass | Full 04 context/selection/tag/export pass and full candidate APKG. Existing diagnostic full package lacks audio; existing production media cover only the 100-card test artifact. Inventory reusable cache before budgeting network work. |
| Audio | Decode/hash valid existing assets once; download only missing/invalid/changed permitted assets. Full availability and mapping are unknown; no honest precise download/listening time estimate exists. Source switch may require replacing every selected recording. |
| Legacy human work | Preserve all 278 rows. Confirm all 188 accepted rows, prioritizing 20 headword anomalies plus other contaminated fields. This is a bounded check of existing work, not automatic deletion of 188 decisions. Ninety pending rows remain, subject to ID migration. |
| Expanded human work | Deduplicated union of changed identities, accepted automatic-field changes, evidence conflicts, all automatic plural validation, unverified lexical senses and changed examples/audio. The 461 current QA flags are not an upper bound. A systemic change could require assessment across all 4,875 baseline lexemes; exact scope comes from field/evidence diffs, not guesswork. |
| License-only update | Notices/description/attribution repackaging, no linguistic rereview if content/evidence unchanged. Replacing QAC/QF/dictionary/text/audio restarts its affected upstream stages and reviews. |

Do not add overlapping risk-population counts to estimate unique work. Build a per-ID/per-field invalidation table with old/new evidence and reason codes; count its union after one stabilized recomputation. No reliable hour estimate follows from current evidence.

## Proposed regression suite and resume gate

Tests below are specifications, not claims that fixes or tests have been implemented. Existing scripts supply fixtures; migrate them into isolated tests without executing production writes. Keep original audit evidence immutable. Every test has an explicit oracle; string similarity or a matching row count alone is never a semantic oracle.

| Test ID | Required fixture / acceptance criterion | Findings |
|---|---|---|
| R01 Recovery and no overwrite | Restore snapshot; run queue generation twice with old/new/retired IDs; decisions/notes identical; failed writes and stale concurrent writers cannot erase work. | D01,P09,P17 |
| R02 Parsing and joins | Preserve all five literal `None` glosses and Unicode/newlines/booleans; reject null keys and conflicting duplicates before dedup; injected token permutations fail text reconciliation. | D10,P01 |
| R03 Identity/population | Explicit pronoun/affix policy fixtures, 15 numbered homographs, split/merge map; all source segments accounted for, permitted exclusions documented, root/form/voice conflicts detected. | D08,P02,P10 |
| R04 Source token alignment | Every coordinate compared under explicit normalization; all 208 QuranMorph anomalies quarantined/reconciled; two refined residuals adjudicated; basmala and four merge verses retained as fixtures. | D09,P01 |
| R05 Frequency/tags | Sum counts equals approved included population; stable tie order under input shuffle; exact Surah/Juz/Hizb/Rub sets per ID; denominator derived and correctly labeled. | P02,D08 |
| R06 Lexical gold set | Expert-approved identities for all D02/D03 examples; derived/weak forms, proper names, active/passive participles, homographs and function words. Ambiguity yields unresolved state, never a forced wrong match. | D02,D03,P03,P07 |
| R07 Plural and definition agreement | Wrong shackle/silk/morals plural links rejected; accepted entry governs plural/senses; Creator/creation and lie/live rejected as semantic proof; negation/voice/segment fixtures retain meaning. | D04,D05,P04 |
| R08 Manual field integrity | All D06 fixtures flagged; valid repeated letters/shadda preserved; commands cannot become values; inherit/replace/suppress round-trip; required fields checked even Reviewed=True. | D06,D07,P08 |
| R09 Approval migration | Unchanged supported manual decisions survive; live automatic/evidence changes expire dependent approvals; legacy missing hashes remain explicit; splits/merges require adjudication; unrelated rank/notices do not expire definitions. | D07,P08,P10,P11 |
| R10 Context and Unicode | Original display marks preserved; target/segment/reference valid; NFC/NFD initial marks normalize as intended; paired/no-stop/sakt/ayah-end and all explicit merges checked; English ordered at word level. | D11,D18,P04,P06 |
| R11 Audio identity | Listening-backed recorded gold results with exact URLs/byte hashes and displayed words; every unexplained numbering disagreement quarantined; fallback and multi-segment cases included. No unexplained selected mapping accepted. | P05,D13 |
| R12 Audio failure paths | HTML, empty, truncated, timeout, interrupted/cache-corrupt assets rejected; lower-tier fallback succeeds where valid; exhaustion explicit; context/English/reference moves with audio. | D12,D13,P12 |
| R13 Realized artifact | Extract full APKG: expected ID/field/tag set, exact realized coordinates/media hashes, no missing/colliding media; CSV and package agree after fallback; stale input/manual hashes block build. | D15,P11,P12 |
| R14 Real Anki import/migration | Initial/repeated/changed-rank imports; user edits/tags under supported modes; reviewed scheduling/history preserved; new-card order verified in queue; split/merge/retirement and schema changes explicit and reversible. | D14,P10,P13 |
| R15 Rendering/playback | Desktop and supported mobile screenshots/manual checks for combining marks, clipping, long glosses, night mode, word-audio labels, keyboard/screen-reader operation. Essential reading/listening must work. | P14 |
| R16 Rebuild/environment | Fresh supported environment and frozen permitted inputs yield identical semantic outputs; authorized/mocked API error paths cannot publish partial snapshots; manifests checked before pickle load; secrets absent from shareable artifacts. | D16,P15,P16 |
| R18 Python workflow/cutover | Imports/CLI help have no data/network/write side effects; build works outside repo CWD; stage parity or approved defect delta recorded; missing/stale/incomplete manifests rejected; interrupted runs resume only compatible stages; decisions untouched; offline build has no network; notebooks call package; CLI output matches accepted package manifest. | M01,P15,P18,D01,P11 |
| R17 Source rights/release | Every distributed field/asset covered by applicable grant/notice/attribution and component compatibility decision; exact version/subset status and documentation match manifest. | D17,P18 |

**Before human review resumes:** R01–R10, R12–R16 and R18 pass for the stabilized candidate; R11 passes for the mapping gold set and all currently disputed selected mappings, with other audio certification status visible per row. Human expert approval of gold fixtures is a prerequisite, not something automated tests can invent. R17's lawful acquisition/storage and source-viability portion must be resolved; publication packaging can remain pending. Unresolved individual linguistic/audio rows are quarantined for review, not counted as validated. If full audio proof is not achievable yet, only explicitly scoped non-audio evidence work may proceed; complete-card approval remains blocked for those rows.

**Before personal trusted use:** each included card's material lexical/context/audio uncertainties resolved or the uncertain component explicitly excluded; no known defective field may be waived by Reviewed=True.

**Before public release:** full R01–R18 and rights clearance, final reviewed manifest, full media inventory, supported import instructions, reproducible release build and no unsupported completeness claims. A source or identity policy change reopens its dependency gates.

## Evidence index for implementation

- `AUDIT_REPORT.md` §§4–9: defect evidence, semantic caveats, package contract and authoritative source links. `CODEX_AUDIT_HANDOFF.md` records intended design; the audit records observed behavior.
- `audit_evidence/replay.py`, `replay03.log`: exact frozen replay and review overwrite. `replay04.log`, `repeat04.log`, `repeat_result.txt`: deterministic cached final CSV; baseline SHA256 `7f11f06c19b87065dac1377c27ab52a287c1fc837f882d3d8afc543a9d06a899`.
- `deep_checks.py/.log`, `QAC_mismatches.csv`, `Context_Target_Arabic_mismatches.csv`, `QAC_Tanzil_residuals.csv`: stale outputs, counts/tags/coordinates and source-token differences. Initial normalization residuals are not all textual defects.
- `linguistic_samples.py/.log`, `stratified_samples.csv`: 365-row stratification, wrong candidate traces, manual anomalies. Gold expectations still require independent linguistic judgment.
- `fault_checks.py/.log`: invalid media acceptance, fuzzy semantic failures, QA bypass, Unicode/fallback faults and successful synchronized fallback branch.
- `network_sample.py/.log`, `remote_comparison.csv`, `remote_audio.json`: 35 verses/494 live word records and 45 audio requests; no audible-identity certification.
- `anki_import_check.py/.log`, `anki_queue_check.py/.log`, `rank_import.py/.log`, `rank_package.py`: real backend import/update/scheduling tests; disposable collections only.
- `additional_checks.py/.log`, package-note CSVs, `source_manifest.json`, `final_verification.txt`: baseline fields/media/environment and original production-file preservation. Keep audit manifests historical after GitHub sanitation.

No production notebook, dataset, review decision or package was changed while preparing this plan. The next authorized implementation should begin at Phase 0, not with bulk regeneration or individual card patching.
