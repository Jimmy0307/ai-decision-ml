# 58 — v2.2 Forensic Audit and Freeze Status

**Date:** 2026-10-11.
**Supersedes:** `48_FORENSIC_AUDIT_AND_V2_1_FREEZE_STATUS.md` as the current freeze status. 48 is kept as v2.1 provenance.
**Scope:** every v2.2 artifact (42 v2.2, 44 v2.2, 45 v2.2, 50–57, `v1_blind/`, `v1_human_packet/`).
**Branch:** `calibration/v1.1-variable-model`, based on canonical head `688c2aeee762cdc352f237b0f6516dd9e46c6aa1`. The branch has not been reset and `main` has not been touched.

## Verdicts

| Track | Verdict |
|---|---|
| Synthetic engineering (Track A) | **`V2_2_SYNTHETIC_ENGINEERING_VERDICT: PASS`** (20/20 required items plus the STATE, REG and AUDIT groups; 52, exit code 0). `SIMULATED_ONLY`. Not empirical, not enterprise, not V7. |
| Independent rederivation | **`INDEPENDENT_COMPUTATIONAL_REDERIVATION_PASS`** (T-ORC-8; 50 §8). |
| V1 G→M blind coding (Track B) | **`V1_AI_PILOT_COMPLETE`** · **`V1_HUMAN_BLIND_CODING_PENDING`**. The AI pilot is classed `AI_BLIND_CODING_PILOT_ACCEPTABLE` under 53B C7. **There is no V1 PASS.** |
| EA-X | Conditional candidate only (a `ρ` grouping key). Human CVI has not started; the AI content-validity pilot gave wording revisions (anchors v2.2.1). |
| V0, V2, V7 | OPEN |
| V3, V4, V5, V6 | COMPLETE at the synthetic level only |

---

## 1. Reference Forensics

| # | Check | Method | Result |
|---|---|---|---|
| 1.1 | Every reference in 44 v2.2 has a verification status | 57 R1–R16 plus Appendix A (N1–N37) | PASS. Nine items moved to VERIFIED (Mikalef & Gupta, Sculley, Teece DOI, Shrestha 61(4) 66–83, Kleinert, Ben-Tal, Dempe Vol. 61, Cohen 1960, Polit et al. 2007) |
| 1.2 | Body citations ↔ reference list | Script: author-year regex over the 44 body vs the list (43 entries) | PASS. No body citation lacks a reference. The only list entries without an author-year match are institutional authors cited by name (EU, ISO/IEC, NIST). Cohen (1960) and Krippendorff (2004) were added to the 3.13 V1 row in this audit |
| 1.3 | Claim strength matches the source | 57 "SUPPORTS / DOES_NOT_SUPPORT" columns | PASS. Mikalef & Gupta's causal wording ("results in") is not adopted; 44 says "reported … associated". Sculley supports ongoing ML maintenance cost; the extension to **shared** infrastructure is labelled as the researchers' own inference |
| 1.4 | Legal source currency | EUR-Lex | PASS with a note: Reg (EU) 2024/1689 is amended by Reg (EU) 2026/1744 (OJ 24.7.2026; consolidated 27.7.2026). 44 states that it relies on no provision introduced by the amendment |
| 1.5 | Residual `[VERIFY]` | 57 residual list | OPEN, six items: McFarlan pages, Savage attribution, Landis & Koch labels, Krippendorff thresholds and 4th-edition year, Polit & Beck (2006) labels, Lynn (1986) pages. None supports an empirical claim. The 53B/56 thresholds are labelled pre-registered study conventions |
| 1.6 | No fabricated sources | All new references in 53B/56/57/44 trace to Crossref, a publisher page or EUR-Lex records in 57 | PASS |

## 2. Provenance

| # | Check | Result |
|---|---|---|
| 2.1 | Canonical head and branch rules | PASS. Local `calibration/v1.1-variable-model` = `688c2ae` plus v2.2 commits only. The old local line is preserved as `local-v2_1-bundle-history`. No reset to `d46822f` or `b0d6b88`; `main` untouched |
| 2.2 | Commit identity | PASS. All v2.2 commits are authored by `Claude <noreply@anthropic.com>` with the session attribution lines |
| 2.3 | V1 freeze chain | PASS. `v1_blind/FREEZE_MANIFEST.txt` stage 1 (53B, 54A, 54B, key plaintext, `sealed_key.json`) and stage 2 (AI coder outputs) were re-hashed in this audit and all seven hashes match. Stage 2 precedes the key reveal (commits `c409a8c` → `2ecf33d` → `9ab2750`) |
| 2.4 | Sealed key custody | The key plaintext is kept outside git (session copy; shipped separately with the v2.2 delivery). Its content is now visible in 54C §3 because the AI pilot revealed it. **Risk:** human coders must receive only `v1_human_packet/`, not repository access. This is recorded in the README for coders and must be enforced by the researcher |
| 2.5 | Corpus lineage | PASS. 44 §1.2 states `6,499 → 3,125 → 783 → 2,180` and V5 Stage 2 `qwen2.5:14b`. The 404 / 2,425 / GPT-5.6 Sol lineage appears only as predecessor provenance (§1.2, Appendix B). No sentence describes 3,125 as an edge count |
| 2.6 | Manuscript authority | **BLOCKER (documentation):** the authoritative 44 v2.1 full text is on Google Drive (file ID `1XNhw0c4…`, 100,827 bytes) and could not be read from this session. 44 v2.2 was rebuilt from the local v2.1 text (99,649 bytes) plus the 49 lineage edits plus the v2.2 changes, and is marked `[DRIVE DIFF PENDING]` (Appendix B11). The roughly 1.2 KB difference has not been compared word by word |
| 2.7 | SIMULATED_ONLY separation | PASS. 51 contains no enterprise data, no G01–G16 O/E, q or counts (grep: no `G01`–`G16`, `O/E` or `q_value` tokens). 44 Ch. 4 puts synthetic numbers only in §4.5; §§4.3, 4.4 and 4.6–4.10 contain only `[EMPIRICAL RESULT PENDING]` placeholders (24 occurrences) and no invented results |

## 3. Numerical Reproduction

| # | Quantity | Recorded | Re-computed in this audit | Result |
|---|---|---|---|---|
| 3.1 | SHA-256 of 51 at run time | `37f26a52…eff516` (52 header) | `37f26a52…eff516` | MATCH |
| 3.2 | Reproducibility hash | `e072fe1a…eefa705` (52 header; T-ORC-13) | `e072fe1a…eefa705` (fresh process) | MATCH |
| 3.3 | Full suite verdict | PASS (52) | n/a. The full suite was run once after all fixes; each changed test was also run individually before that | — |
| 3.4 | AI-pilot reliability JSON | `v1_blind/ai_pilot_reliability_v2_2.json` | Re-run of `reliability_v2_2.py` with the key | IDENTICAL (full JSON equality) |
| 3.5 | Hand oracle | 50 §8 table (66 values) | T-ORC-8 in 52 | MATCH |
| 3.6 | 54C agreement counts | 14/16 primary, 13/16 status per coder | JSON (3.4) | MATCH |
| 3.7 | Synthetic numbers quoted in 44 §4.5 and 50 | F_c^† = 82.497; MMR 15.874; δ sequence 1,1,1,1,0,0,0,1; 10 → 15; 30/15/10 | 52 | MATCH |

## 4. Model Semantics

| # | Invariant | Evidence | Result |
|---|---|---|---|
| 4.1 | Ordinal ≠ cardinal | `Ord` forbids arithmetic, `float()`/`int()` and cross-construct comparison; P5 relabel tests (T-ALG-1, REG) | PASS |
| 4.2 | κ is not a numeric multiplier | κ appears only as a requirement-table key (validator enforces `(Ord('A'), Ord('K'))` keys) | PASS |
| 4.3 | H, EA and EA-X are not assumed to reduce loss monotonically | They enter only as `≥` thresholds or `ρ` keys; P8 shows requirements can screen rather than reduce loss; EA-X is not in any requirement table | PASS |
| 4.4 | G01–G16 statistics are never coefficients | grep (2.7); 42 has no G-indexed parameter | PASS |
| 4.5 | Shared cost counted once | `shared_terms` charges F_c at the enterprise level only; REG regression | PASS |
| 4.6 | Missing = UNIDENTIFIED, never zero | T-MIS-6 (40 mutations, three-way criterion); config-local exclusion; λ never zero-filled | PASS |
| 4.7 | External productivity effects are never OBSERVED | No external effect enters 51; 43 provenance rules unchanged | PASS |
| 4.8 | External evaluators give EXPERT_ELICITED bounds only | Unchanged from 43; no optimizer role in 51 | PASS |
| 4.9 | User layer = ρ by default; third optimizer only if T1–T5 | T-ORC-12: zero tri-level calls unless all five hold | PASS |
| 4.10 | M5 needs longitudinal evidence | 42 §16 unchanged; G11 is contested in the AI pilot, so M5 may rest on G12 alone after human coding | PASS (flagged) |
| 4.11 | Pessimistic and optimistic bilevel values kept separate | All C outputs carry opt/pess; thresholds in C report both | PASS |
| 4.12 | Lemma R scope | ScopeError outside Model B whole-portfolio; `validate_registry` enforces the multilinear precondition | PASS |

## 5. Method Chain (Gap → construct → parameter → equation)

| # | Link | Status |
|---|---|---|
| 5.1 | G01–G16 → M1–M5 (41) | Researcher adjudication. AI pilot: 14/16 primary agree. **G04, G10, G11 contested.** The 53B §11 sensitivity classes all three as mapping-only. 41 v2.1 itself is not edited; the contested flags live in 54C, 55 and 44 §3.4 and should be written back into 41 after the human round |
| 5.2 | M1–M4 → constructs (A, H, WI, EA, G, R, D, κ, EA-X) | Unchanged. EA-X stays conditional (56) |
| 5.3 | Constructs → parameters (43) | Unchanged. v2.2 adds R_j(s)/D_j(s) lookups per capability state and capability-state ρ rows; both fit 43's existing lookup-identification rules (no new parameter class) |
| 5.4 | Parameters → equations (42 v2.2) | (F5e) is now state-indexed for all k; λ-missing semantics, DP, Lemma E′ and robust module as 42 §20 |
| 5.5 | Counterexample discipline | Kept: C-δ non-monotonicity (P4 revised), element-level Lemma R (scope restricted), vertex-VOI overstatement (two-version VOI), joint-infeasibility (four feasibility classes). No test was altered to fit an original proposition |

## 6. Algorithm Consistency (42 v2.2 ↔ 44 Ch. 3 ↔ 51)

| # | Element | 42 v2.2 | 44 v2.2 | 51 | Consistent |
|---|---|---|---|---|---|
| 6.1 | Lemma E′ envelopes | §12.4 | §3.11 | `envelopes_lemmaE` | YES |
| 6.2 | F5e at the chosen state, all k, scale-minimum skip | §5 | §3.11 | `jk_eval.f5e` | YES |
| 6.3 | Capability-state ρ rows | §6 | (implicit in §3.9; not restated) | `expect(capkey)` | YES (44 detail deferred to 42) |
| 6.4 | Missing-input scopes and 13 statuses | §13.4, §18 | §3.11 | `solve`, `_drop_unevaluable`, `unit_plans` | YES |
| 6.5 | λ box scan: exact for B/A+, grid for C | §7.4 | §3.11 | `lambda_scan` | YES |
| 6.6 | DP lower/upper bound and fallback | §12.5 | §3.11 | `mck_dp` | YES |
| 6.7 | Registry validation and commitment | §13.1 | §3.12 | `validate_registry`, `registry_commitment` | YES |
| 6.8 | Four feasibility classes; θ-independent candidates | §13.3 | §3.12 | `feasibility_class`, `enumerate_portfolios(static_only)` | YES |
| 6.9 | MaxRegret exact at vertices (B) | §13.2 | §3.12 | `max_regret`, T-SEN-7 | YES |
| 6.10 | VOI vertex vs grid | §13.5 | §3.12 | `voi_generic` | YES |
| 6.11 | P4: F_c unique (B, C); δ unique in B, set-valued in C | §15 | §3.10, §5.8 | `threshold_mode`, T-SEN-8 | YES |
| 6.12 | Model D gate | §9.2 | §3.9 | `solve_model_D` | YES |

---

## 7. Freeze status

### 7.1 Frozen as v2.2 candidates

- **42 v2.2** (model spec; supersedes 42 v2.1).
- **45 v2.2** (validation plan; supersedes 45 v2.1).
- **51 + 52** (solver and run; 46/47 kept).
- **50** (completion evidence).
- **53A** (commitment), **53B** (frozen protocol), **54A/54B** (frozen packets), **54C**, **55**, **56**, **57**.
- **44 v2.2** is frozen as a *local candidate* subject to `[DRIVE DIFF PENDING]`.

### 7.2 Not frozen / open

- V1 human blind coding: at least two human coders; adjudication per 55.
- EA-X human CVI (anchors v2.2.1).
- V0, V2, V7.
- Residual `[VERIFY]` items (§1.5).
- Drive word-level diff of 44.
- Human code review of 51.
- Writing the contested flags back into 41 after the human round.

### 7.3 Delivery blockers in this session

- **GitHub push:** the push to `Jimmy0307/ai-decision-ml` returned HTTP 403 (the repository is not in this session's authorized set). Delivered instead: a git bundle of `688c2ae..calibration/v1.1-variable-model` plus per-commit patches.
- **Google Drive sync:** no Drive connector in this session and direct access fails. Not synced to `Enterprise_AI_v2_1_Candidate_Freeze_20261011/v2_2_pending_completion/`. All local artifacts and tests were completed first, as instructed.
