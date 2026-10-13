# RESEARCHER ASSIGNMENT COMMITMENT (V1 human construct validation, v1.8.2 pre-human freeze)

STUDY TEAM ONLY. Hashes only. This file contains no item-to-category or G-to-mechanism assignment. All hashes are SHA-256, recomputed on 2026-10-14. The hashes are carried forward unchanged from `claude/r14_merge_v1_8_1_study1_freeze/V1_SEALED/RESEARCHER_ASSIGNMENT_COMMITMENT.md` (SHA-256 `f01a494d82b06e708d6a5e2e629a77874cf9237f9bae55bdf64d7b76c12ffbb6`).

## A. Sealed researcher key (used at phase K; the analyzer reads the hash from this table)

| Object | SHA-256 | Location |
|---|---|---|
| sealed_key.json | `d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734` | outside git: `20261014_AI_DECISION_V1_8_SOURCE_CLOSURE\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\v2_2\sealed_key_DO_NOT_GIVE_TO_CODERS\` |
| 53A plaintext | `9d9de02bfb68566d94cd7023fbff14b79f29fb5db8cf8d364fb941cb6b2e0d3d` | same folder |
| 53A commitment stub (tracked) | `2f864f58a800f17bfd38bf16541f7eff7126c6e1164093159a0d03d72fcc5561` | REPO root |

## B. Files containing the researcher mapping in readable form

These files are hashed so that the mapping cannot change undetected. "PUBLIC" means the file is in the public repository.

| File | Status | SHA-256 |
|---|---|---|
| `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md` | PUBLIC | `b660fd93875c44cf1fb8ffce3a977295d78d4f225937f10c7e115fa508364e02` |
| `54C_AI_BLIND_CODING_PILOT_RESULTS_v2_2.md` | PUBLIC | `b05c72b3071547810b1fa2a2e6cce8d98b30ceb5fb5e8d2e1bd1e52307abdb63` |
| `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` | PUBLIC | `1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58` |
| `claude/r14_merge_v1_8_1_study1_freeze/16_MERGED_MASTER_THESIS_v1_8_1_CLEANUP_CANDIDATE.md` | PUBLIC | `cddeb89b07439ff2bba9af1ba119824cb1cf815c4fc8a78e084900cd24e06bda` |
| `claude/r14_merge_v1_8_1_study1_freeze/current_artifacts/132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.csv` | PUBLIC | `6c7d350960a411be7e1e16d6f70c1ae25ea8f3af5c62035d3b2e2b7e4e35cf5c` |
| `W\…\r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv` | extracted package, not in git | `7f7d06c4c7d91777dfc2baf7c959a7538780a6a88ffbeec0e891c0d0e7b5aef3` |
| `W\…\r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.xlsx` | extracted package, not in git | `be3eda62a10ec9c250c704b63fb0f2ac8a14455c8ba51414be2e08ab476987bd` |

## C. Frozen analysis code (v1.8.2)

| File | SHA-256 |
|---|---|
| `tools/v1_construct_analyzer_v182.py` | `9ce02b2a735e2baf7704ed3710ae2a740562a26d6e866d949d94cd8ccd862f9c` |
| `tools/test_v1_construct_analyzer_v182.py` | `bfcb526e2ce51dcce7319e1ca8919884b7942a74b65f73bd31beb3203d4e271c` |
| `v1_blind/reliability_v2_2.py` (imported unchanged; hash checked at runtime) | `866e9005da8a20e996c93b5c8f6bee916992f24d60c6a96e8f1dcda4556848e7` |

Blinding note: the hash commitment protects the integrity of the key. It does not protect coder blinding, because the mapping is readable in PUBLIC files (see 28).
