# 08 — V1.8.6a Precision Harmonization + Erratum Lineage Closure: Final Status

**Date:** 2026-10-18
**Version rule:** V1.8.6 = formal theory integration. V1.8.6a = precision harmonization + erratum lineage closure. V1.8.6a is **not** a new theory version, a new empirical version or a model revision.

**Manuscript:**
- `01_V1_8_6A_MANUSCRIPT.md`, sha256 `12eee36a8c1a762a16603deb4f46d2962cc4019a62e443241c082629546d9517`.
- Built from the V1.8.6 manuscript (`94d41d56…`), which stays read-only and unchanged.
- 52 exact-match replacements (H01–H52) across 45 base lines. Reversing them reproduces V1.8.6 byte for byte.

```
V1_8_6_BASELINE_PRESERVED = YES
RD1_TERMINOLOGY_HARMONIZED = YES
CODER_FACING_TERM = 企業決策過程
THEORETICAL_TERM = 企業決策機制 (組織決策安排 where organizational configuration is emphasized)
CONSTRUCT_CHANGED = NO
RD2_P2_REMARK = PRECISION_EDIT_RETAINED
P2_FORMAL_STATEMENT_CHANGED = NO
RD3_42_ORIGINAL_MUTATED = NO
42A_ERRATUM_CREATED = YES
RD5_OUTER_PRECISION_ITEMS_RESOLVED = YES
NEW_REFERENCES_ADDED = 0
UNVERIFIED_REFERENCES_ADDED = 0
CODER_HASHES = 3/3 PASS
CODER_INSTRUMENT_CHANGED = NO
CODER_PACKET_REISSUE_REQUIRED = NO
STUDY1_CHANGED = NO
G01_G16_CHANGED = NO
V2_2_EQUATIONS_CHANGED = NO
THEORY_STATUS = PARTIAL
HUMAN_RESULTS_CREATED = NO
ENTERPRISE_RESULTS_CREATED = NO
SUBMISSION_READY = NO
GITHUB_PUSH = (recorded at handoff; branch research/v1.8.6a-precision-harmonization-20261018)
DRIVE_CLOUD_SYNC = (recorded at handoff)
V1_8_6A_VERDICT = PASS
```

## Evidence

| Item | Evidence |
|---|---|
| Baseline | V1.8.6 01 hash asserted before patching and unchanged on disk. V1.8.6 reports 02–12 are not edited. |
| RD-1 | 企業決策介面 went from 17 occurrences to 5. All 5 remaining are historical or label explanations: the version line, the §3.9.1 note, the L699 lead-in, the protected Table 3-4A column header and the §3.9.6 S1d note. Bare 介面 went from 69 to 58 (not global-replaced). I1–I5, 介面活化, the 共用介面 data gate and technical interfaces are kept. The required S1e sentence appears exactly once, verbatim, at §3.9.3 (4). §3.9.3, Table 3-14, Table 4-13 and E6 are synced to S1e. See 03. |
| RD-2 | The P2 remark is kept as in V1.8.6, and the P2 formal statement is identical to 59a and V1.8.6. All three strong "P1–P8 unchanged" phrases (L5, L1159, L3125) now carry the standard precision wording; none remain. No remark changes any theorem's domain, so no STOP. |
| RD-3 | 42 (`0249e7b9…`) and 51 (`37f26a52…`) are byte-identical. `42a_CANONICAL_42_ERRATUM_V1_8_6.md` and its identical copy `04_42A_ERRATUM.md` are new files. Manuscript C.10.9 names 42a as the lineage record. |
| RD-5 | Table 1-1 RQ4–6, §2.13, Table 3-10 Q2/Q4/Q7, §4.10.3, Table 4-33 Q5/Q6, and the §5.8.4 and §5.8.5 pointers were resolved against the V1.8.6 06 status matrix. The claim sweep also fixed §5.6 (DL "only positive when" is now stated as necessary conditions only) and §5.7 (V7 marked as not yet run). See 05. |
| References | 06 maps Alonso & Matouschek 2008, Armstrong & Vickers 2010 and Stoye 2011 to exact claims. None is needed, since E51 already disclaims novelty and no existing sentence misstates prior literature; the first two are also redundant. All three are kept in verified research notes. |
| Claim sweep | No minimal-sufficient, complete-taxonomy, full-iff, "generally non-monotone", "validated" or "construct validity" claim exists. Every `iff` hit is an English substring (different, diffusion, …). 162/400 stays primary and 367/400 is labelled sensitivity only. |
| Protected regions | Independently re-verified: math spans 53/53 identical, G rows 36/36 identical, the reference section byte-identical, no number removed, and Tables 3-4/3-4A and C.1–C.9 identical (PH verifier). |
| Coder gate | 07: the S1e packets are byte-identical to the preflight snapshot. |

## Researcher decisions still open (none blocks V1.8.6a)

- **RD-3 (timing):** when to carry the 42a wording into a future canonical revision of 42.
- **RD-4:** optional renaming of clashing labels (T1–T4, G1–G8, the D/R/E series).
- **References:** optionally add a related-literature sentence for DL/GS (Alonso & Matouschek as contrast) or place W6b against Stoye (2011). Either would be a new comparison sentence and therefore a future decision.

Every synthetic number remains SIMULATED_ONLY. No V1 human result, enterprise result or V7 claim exists.
