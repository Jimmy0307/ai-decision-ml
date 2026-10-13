# 27 — V1 Pre-freeze Audit (v1.8.2)

Every line below was computed by `tools/audit_v182.py`. No value was typed by hand.

```
CODER_FILES=3
ALL_RESPONSE_CELLS_EMPTY=YES
ALL_ATTESTATION_CELLS_EMPTY=YES
GID_VISIBLE_TO_CODERS=NO
RESEARCHER_MAPPING_VISIBLE_TO_CODERS=NO
AI_PILOT_VISIBLE_TO_CODERS=NO
SENSITIVITY_TARGET_MARKERS_VISIBLE=NO
LEAKAGE_FINDINGS=0
OA2=APPROVED_WITH_SCOPE_LIMIT
OA3=APPROVED
PRIMARY_RELIABILITY=KRIPPENDORFF_ALPHA_Q2_3_CODERS
PAIRWISE_KAPPA=SECONDARY
THRESHOLD_PROVENANCE=RESEARCH_CONVENTION
STUDY1_FREEZE_CHANGED=NO
ENTERPRISE_MODEL_CHANGED=NO
HUMAN_VALIDATION_EXECUTED=NO
```

| Audit line | Value | Evidence |
|---|---|---|
| CODER_FILES | 3 | coder_distribution = ['CODER_1.xlsx', 'CODER_2.xlsx', 'CODER_3.xlsx']; one CODER sheet per file = True; no master there |
| ALL_RESPONSE_CELLS_EMPTY | YES | openpyxl count over CODER_* Q1-Q5 cells in 4 workbooks |
| ALL_ATTESTATION_CELLS_EMPTY | YES | openpyxl count over ATTESTATION answer column |
| GID_VISIBLE_TO_CODERS | NO | leakage: cell + raw-XML (all parts incl. docProps) G-ID scan; OUT text pairing scan |
| RESEARCHER_MAPPING_VISIBLE_TO_CODERS | NO | leakage: category codes in item rows, researcher vocabulary, hint words, network numbers |
| AI_PILOT_VISIBLE_TO_CODERS | NO | leakage: 1161 AI-pilot 6-word shingles + 'pilot' vocabulary |
| SENSITIVITY_TARGET_MARKERS_VISIBLE | NO | leakage: per-item row style/fill/height/hidden uniformity incl. 3 sealed sensitivity rows; 'sensitivity' vocabulary |
| LEAKAGE_FINDINGS | 0 | tools/leakage_check_result_v1_8_2.json (verdict PASS) |
| OA2 | APPROVED_WITH_SCOPE_LIMIT | 24 D-1 |
| OA3 | APPROVED | 24 D-2 |
| PRIMARY_RELIABILITY | KRIPPENDORFF_ALPHA_Q2_3_CODERS | analyzer constant; Q2 alpha nominal over 3 coders |
| PAIRWISE_KAPPA | SECONDARY | analyzer constant; pairs tagged role=SECONDARY |
| THRESHOLD_PROVENANCE | RESEARCH_CONVENTION | analyzer constant |
| STUDY1_FREEZE_CHANGED | NO | git status --porcelain: tracked changes = 0 |
| ENTERPRISE_MODEL_CHANGED | NO | git status --porcelain on enterprise model / solver / schema files |
| HUMAN_VALIDATION_EXECUTED | NO | analyzer on blank packets -> NO_HUMAN_DATA; S2 manifest present = False |

Analyzer correctness test: `PASS kappa_vs_sklearn_max_abs_diff=2.498e-16 (n=300) alpha_vs_krippendorff_max_abs_diff=4.441e-16 (n=300) classification_rule=PASS oa3_none_validation=PASS`

Coder-facing workbook hashes at audit time:

| File | SHA-256 |
|---|---|
| coder_distribution/CODER_1.xlsx | `840addf9978ee30b725d4e190b940adfa13f0c1683c7ab2b3bde60a0ff4ce301` |
| coder_distribution/CODER_2.xlsx | `74d72705876681e3dcae411f83e144d2c846fc94068114f172a47d8c3368bc86` |
| coder_distribution/CODER_3.xlsx | `01b292791111a89b7d86e595d6cbde15c2305222bb8a72399def2e69bd8669fc` |
| 20_MASTER_PACKET_v1_8_2.xlsx | `38614e60aadb4974d4c1fc2b1dc5bce297746f0bd664d1ab51d5aa96be4afa48` |

V1_HUMAN_CONSTRUCT_VALIDATION_STATUS=READY_TO_RUN
