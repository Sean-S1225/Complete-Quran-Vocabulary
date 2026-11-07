# CompleteQuranVocabulary — Codex Audit Handoff

## Purpose

This project builds a comprehensive Arabic→English Anki vocabulary deck for the Qur'an.

The immediate task is not to add features or refactor the project. It is to perform a rigorous, adversarial audit of the entire pipeline:

1. Reconstruct what the project actually does from the repository/files.
2. Check whether the major design and implementation decisions are sound.
3. Identify assumptions, edge cases, data-quality problems, architectural risks, or missing work the current author and prior assistant may have overlooked.
4. Distinguish confirmed correctness, reasonable-but-unverified choices, actual defects, product/design tradeoffs, and unknowns requiring further evidence.

Do not assume this handoff is correct. It is a map of the intended design and known history. The repository and source data are the evidence of record.

---

# 1. Product goal

Create an Anki deck containing essentially every Qur'anic lexeme, compressed pedagogically rather than creating one card per surface form.

## Intended card direction
Arabic → English recognition.

## Intended card content

Front:
- canonical Arabic headword
- plural when useful

Back:
- headword / plural
- concise English definition
- root
- POS
- authentic Qur'anic occurrence
- word audio
- pause-bounded Qur'anic context
- rough word-by-word English support
- reference

Additional/hidden metadata:
- frequency
- frequency rank
- observed forms
- provenance/review status
- Qur'an location tags

## Intended Anki organization

Primary tag:
- `CompleteQuranVocabulary`

Hierarchical location tags:
- `Quran::Surah::002`
- `Quran::Juz::01`
- `Quran::Hizb::003`
- `Quran::Rub::011`

The intent is that a learner memorizing a section can filter, for example:

`tag:CompleteQuranVocabulary is:new tag:Quran::Rub::005`

and learn only not-yet-seen lexemes appearing in that rubʿ.

Default card order should correspond to descending corpus frequency / ascending `Frequency Rank`.

---

# 2. Lexeme inclusion/collapse rules

Intended design:

- singular/plural noun inflections collapse to one lexeme
- subject/person/number verb conjugations collapse to one lexeme
- distinct QAC lexical identities/homographs remain distinct
- adjectives are included
- active/passive participles are independent lexical entries, with participle metadata
- proper nouns are included
- numbers are included
- independent pronouns are included (`PRON`, `DEM`, `REL`)
- disconnected letters (`INL`) are excluded
- attached particles and pronominal suffixes are not part of lexeme identity
- maṣdar forms are generally treated as nouns / lexical entries

Examples of desired canonicalization:
- `مُفْلِحُون → مُفْلِح`
- `مُّكَذِّبِين → مُكَذِّب`
- `مُقَرَّبُون → مُقَرَّب`
- `مُّسْتَضْعَفُون → مُسْتَضْعَف`
- `جَحَدُ → جَحَدَ`
- `يَسْتَعْتِبُ → اِسْتَعْتَبَ`
- `عَتَ → عَتَا`

Important caution:
Do not blindly strip plural endings because weak-final forms and other morphology can make that unsafe.

---

# 3. Major data sources

## 3.1 Quranic Arabic Corpus (QAC) morphology v0.4

Used as the primary occurrence-level morphological source.

Known scale:
- ~128,219 segmented morphology rows
- positions represented as `(surah:ayah:word:segment)`

Important assumptions/design:
- real verbs carry `LEM:`
- `Vocabulary ID` is treated as the stable lexeme-grouping identity
- trailing digits in IDs can distinguish homographs
- QAC lemmas collapse inflection but are not always ideal citation forms

Audit:
- confirm exactly how `Vocabulary ID` is created/loaded and whether it is truly stable and semantically appropriate for deck identity
- confirm segment selection and exclusion logic
- check whether any lexeme classes are accidentally omitted or duplicated

## 3.2 Quran.Foundation / Quran.com word-by-word data

Used for:
- word-by-word English glosses
- Juz / Hizb / Rub metadata
- authentic word audio coordinates

Known scale:
- 77,429 orthographic Qur'anic words

Important historical discovery:
The old imported `Audio` path column appeared misaligned for some rows. The pipeline therefore switched to deterministic coordinate-derived audio paths:

`wbw/{Surah:03d}_{Ayah:03d}_{Word:03d}.mp3`

with base:
`https://audio.qurancdn.com/`

Examples that exposed the problem included selected occurrences for `كَانَ`, `أَرْض`, and `فِي`.

Audit:
- independently verify that coordinate-derived audio is correct
- sample many random positions, not only known examples
- verify downloader error handling and media validation
- verify displayed occurrence and audio always refer to the same orthographic word, including fallback behavior

## 3.3 QuranMorph / Qabas (`quran-morph.csv`)

Known scale:
- 77,429 rows
- one row per orthographic Qur'anic word
- coordinates align with Quran.Foundation

Columns include:
- `surah_number`
- `verse_number`
- `word_position`
- `word`
- `POS`
- `qabas_lemma`

Uses:
- complete orthographic Qur'anic word
- auxiliary headword evidence

Important caution:
Direct QuranMorph lemma promotion proved unsafe in some cases.

Known bad/awkward mappings observed:
- `مُّغْرَقُون → مُغْرِقٌ`
- `مُخَلَّفُون → مُخَلِّفٌ`
- `يَسْتَعْتِبُ → عَتَبَ`
- `مُّلَٰقُوا → لَاقَى`
- `أَطْهَر → طَاهِرٌ`
- `أَكِنَّة → [كَنَّنَ, كِنَانٌ]`

Audit:
- confirm QuranMorph is used as evidence rather than unquestioned authority
- inspect any remaining automatic promotion paths

## 3.4 Kaikki English Wiktionary Arabic JSONL

Historically named similar to:
- `kaikki.org-dictionary-Arabic.jsonl`

Used for:
- canonical headword evidence
- plural evidence
- definitions

Historical matching results were approximately:
- matched: 4226
- POS conflict: 371
- unmatched: 278
- ~86.7% lexeme coverage
- ~98.2% occurrence coverage

Audit:
- inspect normalization/matching logic
- inspect homograph handling
- test POS mapping completeness
- test whether relaxed matching can silently choose the wrong dictionary entry
- inspect definition-selection heuristics

## 3.5 Tanzil Uthmani Qur'an text with pause marks

Current intended file:
- `quran-uthmani.txt`

Used for:
- learner-facing Qur'anic context
- waqf/pause segmentation

Waqf segmentation rules currently intended:

Usable boundaries:
- `ۘ` required stop
- `ۚ` permissible
- `ۗ` stopping preferred
- `ۖ` continuation preferred but stopping permissible
- ayah end

Not used as ordinary boundaries:
- `ۙ`
- paired/interchangeable `ۛ`

Other annotations such as rub/sajdah/sakt marks must not become lexical words.

There were a small number of known token-boundary discrepancies between Tanzil Uthmani and QuranMorph/QF, handled explicitly rather than with broad fuzzy alignment.

Audit:
- confirm exact current implementation
- verify pause-sign semantics from authoritative Tanzil documentation
- verify all 6,236 ayahs and all 77,429 orthographic word coordinates align after explicit exceptions
- verify explicit boundary exceptions are correct and complete
- verify context cannot cross an invalid stop
- verify displayed context preserves Qur'anic text accurately
- verify target highlighting remains synchronized with the selected word

---

# 4. Main dataframe architecture

Names may have evolved; inspect actual code.

## `database`
All QAC prefix/stem/suffix morphology rows.

## `vocabulary_occurrences`

Intended:
one row per vocabulary-bearing QAC lexical segment.

Historical size:
- 77,885 rows

Important columns include:
- `Vocabulary ID`
- `Surah`
- `Ayah`
- `Word`
- `Segment`
- lexical `Arabic`
- `Quranic Word`
- `English`
- `Cleaned English`
- `Audio`
- `Juz`
- `Hizb`
- `Rub el Hizb`
- occurrence-tier / structural metadata
- suffix/prefix metadata
- waqf context fields

Important conceptual distinction:

**QAC lexical segment != complete orthographic Qur'anic word**

Word audio is tied to the complete orthographic word.

## `vocabulary`

Intended:
one row per `Vocabulary ID`.

Historical size:
- 4,875 lexemes

Columns/evidence have included:
- `Lemma`
- `QAC Lemma`
- `Root`
- `POS`
- `IsParticiple`
- `ParticipleType`
- `Surahs`
- `Juzs`
- `ObservedForms`
- `Frequency`
- `Frequency Rank`
- `English Glosses`
- `Definition Evidence`
- observed-form/POS counts
- occurrence metadata
- Wiktionary candidates/matches
- QuranMorph evidence

Audit:
- verify row-count invariants from raw sources
- verify uniqueness
- verify aggregation does not erase meaningful lexical distinctions

---

# 5. Frequency

Historical totals:
- vocabulary-bearing occurrence segments: 77,885
- lexemes: 4,875

Frequency is intended to mean count of vocabulary-bearing lexical occurrences, not orthographic Qur'anic words.

Historical cumulative thresholds were roughly:
- 50% coverage: 64 lexemes
- 75%: 332
- 80%: 471
- 85%: 694
- 90%: 1,102
- 95%: 1,997

Audit:
- verify the frequency definition is pedagogically sensible
- verify no clitic segmentation artifact inflates/deflates counts
- verify ties/ranking behavior
- verify Anki new-card order is actually driven by intended rank

---

# 6. Representative occurrence selection

The pipeline tries to choose a pedagogically clean example.

Desired priorities include:
- avoid attached pronominal suffix where possible
- prefer exact lexical form
- prefer exact whole-word match
- prefer a word with one vocabulary-bearing segment
- prefer no prefix where possible
- prefer singular nominal form where appropriate
- prefer good vocalized similarity
- among otherwise good choices, prefer a shorter waqf segment
- retain other occurrence-quality tie-breakers

Important design:
textual occurrence selection is offline/deterministic.
Network audio availability should not be checked for all 4,875 lexemes during selection because that caused severe runtime slowdown.

At package-build time, if chosen audio fails to download, the builder may try ranked alternative occurrences. If that happens, all displayed occurrence/context/reference fields must move with fallback audio.

Audit:
- inspect exact ordering of sort criteria
- decide whether shortest waqf segment is at the correct priority
- test nouns, verbs, participles, particles, pronouns, proper nouns
- test whether “cleanest” examples are actually pedagogically preferable
- verify fallback audio cannot desynchronize context/text/reference

---

# 7. Definitions

Historical problem examples:
- `قَد → to lead` due to POS mismatch/homograph failure
- `يَوْمٌ → Judgment Day` too context-specific
- `غَيْر → more than` contextual artifact
- `كَفَرَ → to be ungrateful` is valid but may need broader supported senses

Current intended logic:
1. manual definition wins
2. function words rely strongly on cleaned QF gloss evidence
3. content words use Wiktionary senses only when supported by QF evidence
4. allow up to ~3 concise supported meanings separated by semicolons
5. otherwise QF fallback
6. last-resort dictionary fallback

Audit:
- reconstruct actual implementation
- test high-frequency and low-frequency samples
- test polysemy
- test homographs
- test particles/function words
- test whether QF support is too restrictive or too permissive
- check whether definitions are dictionary-like rather than verse-specific paraphrases
- inspect English cleanup rules for semantic distortion

---

# 8. Headword/canonicalization

Desired:
- nouns/adjectives: citation form, normally singular where linguistically appropriate
- verbs: 3rd-person masculine singular perfect
- plural stored separately when pedagogically useful
- participles remain lexical entries rather than collapsing to underlying verbs

Important historical architecture:
Notebook 03 should ideally produce evidence.
Notebook 04 finalizes using manual review + automatic evidence.

Audit:
- identify current source-precedence rules
- test whether automatic choices violate citation-form conventions
- inspect weak verbs, defective nouns, broken plurals, duals, elatives, participles, proper nouns, collective nouns, verbal nouns
- check singularization is never naïve suffix stripping
- check plural evidence quality

---

# 9. Manual review and Auto QA

Historical manual-review queue:
- initially 278 unmatched/problem lexemes
- approximately 178 were reviewed at one point
- roughly 100 remained, but current repository state is authoritative

Existing file:
- `manual_lexeme_review.csv`

Typical columns:
- `Vocabulary ID`
- `Manual Headword`
- `Manual Plural`
- `Manual Definition`
- `Manual Notes`
- `Reviewed`

Important semantics:
- `Reviewed=True` means human-reviewed
- blank manual override fields mean “keep the automatic value”
- nonblank manual overrides should win

Separate final warning:
- `Auto QA Flag`
- Anki tag `NeedsReview`

A terminal tool now exists:
- `qa_review.py`

It should:
- load `final_anki_lexicon.csv`
- find Auto-QA rows
- exclude already-reviewed rows
- allow accept-as-is or manual overrides
- update `manual_lexeme_review.csv`
- autosave safely

Audit:
- verify `qa_review.py` semantics against Notebook 04
- ensure accept-as-is suppresses future QA without blanking automatic values
- ensure CSV additions remain compatible with original manual-review workflow
- verify atomic save / duplicate-ID behavior
- inspect whether Auto QA flags are well designed or produce false confidence / false alarms
- identify better QA criteria if appropriate

---

# 10. Waqf context and English context

Desired:
- smallest valid pause-bounded segment containing selected occurrence
- target word visually highlighted
- rough word-by-word English gloss sequence
- English is intentionally not presented as polished translation

Example:
Arabic:
`وَقَدْ كَانَ فَرِيقٌ مِّنْهُمْ`

English support:
`and indeed / had been / a group / among them`

Audit:
- verify segmentation accuracy
- verify target highlighting
- verify English gloss order aligns to orthographic words
- verify merged/special word-boundary exceptions do not misalign glosses
- inspect whether slash-joined glosses create misleading semantic readings
- consider whether labeling should make the “word-by-word support” nature clearer

---

# 11. Anki package generation

Expected output:
- `.apkg`
- approximately 4,875 notes/cards unless current repository says otherwise

Audio:
- MP3
- standard Anki syntax: `[sound:filename.mp3]`

Media filenames are intended to be deterministic and occurrence-sensitive so changed occurrences do not silently reuse stale media.

Audit:
- verify model ID / deck ID stability
- verify note GUID stability across rebuilds
- verify reimport updates existing notes rather than creating duplicates
- verify field-order stability
- verify tags are valid and hierarchical
- verify media filenames and package media list
- verify missing-audio behavior
- verify network responses are actually audio and not HTML/error bodies saved as `.mp3`
- verify Anki template HTML/CSS on desktop and mobile where feasible
- verify RTL / Arabic rendering
- verify card sorting/new-card order
- verify a rebuild after manual edits behaves predictably

This is a particularly important “things we may have overlooked” area.

---

# 12. Source licensing / redistribution / attribution

This has not been fully audited and could be a major release-readiness issue.

Investigate current authoritative terms for every redistributed input or derived content, including:
- Quranic Arabic Corpus
- Quran.Foundation/Quran.com word-by-word data
- Quran CDN audio
- QuranMorph/Qabas
- Wiktionary/Kaikki
- Tanzil Qur'an text
- any other dataset actually used

Questions:
- May the derived Anki deck be redistributed?
- What attribution is required?
- Are share-alike requirements triggered?
- Must source text remain unmodified?
- Are audio files redistributable inside an `.apkg`?
- Are notices required in deck/repository?
- Are licenses mutually compatible?

Do not guess. Use authoritative license/terms pages and clearly separate legal uncertainty from confirmed requirements.

---

# 13. Known historical failure modes

Use these as regression tests, not as an exhaustive list.

## Audio/display mismatch
Examples historically included:
- `كَانَ`
- `أَرْض`
- `فِي`
- `إِذَا`
- `أَرْسَلَ`
- `كَافِر`

## Lexical-segment vs orthographic-word confusion
Example:
- lexical `فِي`
- complete orthographic word may be `فِيمَا`

Display accompanying word audio must match the audio unit.

## Headword problems
Known unsafe automatic QuranMorph mappings listed earlier.

## Definition problems
Examples:
- `قَد`
- `غَيْر`
- `يَوْم`
- `كَفَرَ`

## Runtime
Never perform thousands of network availability requests inside representative-occurrence ranking.

## Notebook state
Stale Jupyter outputs previously masked broken code. Audit should work from clean kernel / fresh execution.

---

# 14. What the audit should NOT assume

Do not assume:
- prior assistant-generated code is correct
- comments match implementation
- current notebook is the only file that matters
- row-count equality proves semantic alignment
- successful `.apkg` build proves the deck is correct
- dictionary match = correct sense
- QAC, QuranMorph, Wiktionary, or QF are individually error-free
- current QA flags cover every meaningful failure mode
- current deck is legally redistributable

---

# 15. Required audit approach

## Phase A — Repository reconstruction

Before judging anything:
1. inventory relevant files
2. identify pipeline order and dependencies
3. identify authoritative vs stale/generated/experimental files
4. reconstruct actual dataflow from raw data → intermediate artifacts → final lexicon → `.apkg`
5. note discrepancies between this handoff and code

Do not make source edits during this phase.

## Phase B — Deterministic execution/invariants

Run the pipeline from a clean state if feasible.

Check:
- row counts
- uniqueness constraints
- joins
- nulls
- coordinate alignment
- cardinality
- rank uniqueness
- reproducibility
- deterministic outputs

Prefer explicit diagnostics over “looks okay”.

## Phase C — Decision-by-decision audit

For every important design decision, classify:
- `PASS`
- `PASS WITH CAVEAT`
- `UNVERIFIED`
- `FAIL`

For each include:
- decision
- where implemented
- rationale
- evidence/tests
- failure modes considered
- verdict
- severity
- recommended action

## Phase D — Adversarial missing-things review

This is the most important phase.

Ask:
- What could be wrong even if all current assertions pass?
- What assumptions are encoded implicitly?
- What edge cases are not represented in our examples?
- What could make a learner memorize wrong information?
- What could break when the deck is rebuilt or imported?
- What could make redistribution problematic?
- What tests would a careful maintainer expect but are absent?
- What architecture is fragile or too dependent on notebook state?
- Are there validation resources we should have used but did not?

Do not restrict this section to issues mentioned in this handoff.

## Phase E — Empirical sampling

Use stratified samples, not only random samples:
- top-frequency lexemes
- hapax/rare lexemes
- nouns
- verbs
- particles
- pronouns
- participles
- proper nouns
- plurals
- weak verbs
- homographs
- multi-segment orthographic words
- suffixed words
- prefixed words
- relaxed dictionary matches
- manually reviewed entries
- Auto-QA entries
- entries with audio fallback
- waqf edge cases

Where useful, compare against authoritative external references.

## Phase F — Release-readiness verdict

Answer:
- Is the deck safe to use personally?
- Is it ready for public distribution?
- What must be fixed before each?
- What should merely be documented?
- What is optional polish?

---

# 16. Desired audit deliverable

Produce one Markdown report with:

1. Executive verdict
2. Repository/pipeline reconstruction
3. Decision audit matrix
4. Confirmed defects
5. Unverified assumptions
6. Missing checks / overlooked risks
7. Linguistic/data-quality risks
8. Anki/package/rebuild risks
9. Licensing/redistribution findings
10. Recommended tests
11. Prioritized action list
12. Personal-use readiness vs public-release readiness
13. Appendix: evidence and commands run

For defects include:
- severity: Critical / High / Medium / Low
- affected file/cell/function
- reproducible evidence
- proposed fix
- whether the fix changes generated data and therefore requires re-review

Prioritize correctness over elegance.

---

# 17. Audit constraints

- First pass should be read-only with respect to production project files.
- Diagnostics may be created in temporary locations.
- Do not silently “fix” the project while auditing it.
- Do not rewrite notebooks merely because code style could be cleaner.
- Separate correctness issues from maintainability/style issues.
- Do not over-weight this handoff; trust actual code/data.
- If an external factual claim is important, verify it from an authoritative source.
- Explicitly say when something cannot be verified from available evidence.
