# CompleteQuranVocabulary — persistent working instructions

User preferences recorded 2026-11-07. Apply these in future sessions unless the user overrides them. This file records workflow authorization; it does not by itself authorize implementation of the remediation plan or publication of a deck.

## Recover state first

Read `AUDIT_PROGRESS.md` and the relevant sections of `REMEDIATION_PLAN.md` before continuing. Use `CODEX_AUDIT_HANDOFF.md` and `AUDIT_REPORT.md` for original intent and established evidence. Reuse retained diagnostics; do not repeat expensive audits or builds without a concrete evidence gap. Preserve historical audit manifests.

## Shorthand: “use a total of four agents as we've discussed”

Treat this phrase, or an equivalent request, as authorization to use **four agents total: one primary plus three workers**, with the assignments below. It is not four workers plus a primary. Activate all four when independent tasks exist; serialize dependent work and leave workers idle rather than invent work. Do not exceed available session capacity or spawn nested agents to bypass it. If capacity/models are unavailable, explain the limitation and use the closest feasible arrangement without silently changing model roles.

| Agent | Model / effort | Responsibility |
|---|---|---|
| Primary | GPT-6 Astra (`gpt-6-astra`), High; Extra High only for especially difficult decisions | Architecture, contracts, novel evidence evaluation, Arabic/identity judgments, licensing-risk interpretation, integration, review invalidation and final correctness/readiness verdicts. |
| Pipeline worker | GPT-6.1 Sol (`gpt-6.1-sol`), High | Structured Python extraction and specified corpus/lexicon fixes, with parity/delta evidence. Medium is appropriate for bounded adapters after contracts stabilize. |
| Review/package worker | GPT-6.1 Sol, High | Review preservation/migration, manifests, Anki identity/import/update integrity. Medium for routine wiring against approved contracts. |
| Test/media worker | GPT-6.1 Sol, Medium for established fixtures/tests; High for media resolver/cache integration | Independent regression tests or approved audio/media implementation, with isolated outputs. |

A free worker slot may use GPT-6.1 Sol Low for purely editorial work. Do not delegate novel linguistic judgments, evidence adjudication, rights conclusions or final verdicts to cheaper workers. Workers escalate unexpected behavior to the primary. Human expert/listening evidence and permissions cannot be replaced by model agreement.

Follow the W0–W6 assignments and gates in `REMEDIATION_PLAN.md`. Without the four-agent request, use the plan's normal three-agent team only when delegation is authorized and useful. This documentation request alone does not launch agents.

Use explicit model/effort selections and bounded briefs with editable paths, contract versions, finding/test IDs and acceptance criteria. Separate worktrees when feasible; otherwise disjoint file ownership and output directories. Spawning does not inherently isolate the filesystem. Only the primary integrates changes, edits shared contracts, runs shared expensive builds and updates the authoritative checkpoint. No concurrent writes to decisions, caches, packages or Anki collections.

## Git defaults — standing user authorization

- Commit coherent, reviewable progress wherever reasonable: completed fixes, tested extraction steps, documentation and useful recovery checkpoints. Do not wait until the whole project is complete. Separate behavior-preserving extraction, defect fixes and migrations when practical.
- At the end of each completed implementation/planning step, update the checkpoint, run appropriate checks, commit that step and **push to the configured GitHub remote/working branch**. Do not ask again merely to make a normal commit or push within authorized work. Git actions do not authorize unrelated production changes.
- Inspect status/diff and stage explicit relevant paths. Preserve unrelated user changes. Never force-push, rewrite shared history, delete branches or resolve substantive conflicts destructively under this standing authorization.
- Preserve `.gitignore` protections. Do not commit credentials, private review CSVs, raw/licensing-restricted datasets, media, generated decks or audit evidence just to share them or make a backup. A source push does not replace the private restore-tested snapshot required by Phase 0.
- Use appropriate checks for each change; documentation-only steps need consistency/diff checks, not full notebook execution. An incomplete recovery commit must be clearly labeled and must not imply tests passed. Push a recovery checkpoint if safe, explicitly reporting incomplete work.
- Verify push success and report commit/branch. If authentication, network, approval or non-fast-forward conflicts block pushing, preserve the local commit, record the blocker when possible, and report it accurately. Follow environment approval requirements; do not bypass them.

## Progress and cutoff recovery

Keep `AUDIT_PROGRESS.md` concise and current. Update it after every substantial subtask or integration gate, before an expensive/long-running operation, before switching phases, and before yielding or ending a session. During sustained work, checkpoint roughly every 10–15 minutes even if a step is unfinished; checkpoint immediately if usage/context exhaustion is approaching.

Record completed finding IDs, changed files, test commands/results, artifact paths/hashes, decisions, unresolved blockers, current branch/last relevant commit and the exact next executable steps. Distinguish implemented/tested results from proposals. Keep private content and secrets out of tracked progress files. Do not write stream-of-consciousness notes or claim a future commit/push succeeded.

Workers return compact handoffs at task boundaries; the primary consolidates accepted results. Prefer saving a useful checkpoint over starting another investigation when usage is low. Commit/push useful progress when reasonable under the Git rules above, without claiming an unfinished phase is complete.
