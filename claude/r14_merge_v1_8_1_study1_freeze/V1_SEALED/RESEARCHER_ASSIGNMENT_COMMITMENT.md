# RESEARCHER ASSIGNMENT COMMITMENT (V1 human construct validation, v1.8.1)

STUDY TEAM ONLY. This file contains hashes only. It contains no G-to-category assignment.

Commitment date: 2026-10-14. All hashes are SHA-256, recomputed by sub-agent I on 2026-10-14. The two sealed-object hashes match the values committed in 53A and in `v1_blind/FREEZE_MANIFEST.txt` stage 1.

## A. Sealed key (primary commitment; used for unsealing)

| Object | Location (outside the repository) | SHA-256 |
|---|---|---|
| sealed_key.json | `W\01_ALL_OUTPUTS\AI_DECISION_THESIS_ALL_OUTPUTS\v2_2\sealed_key_DO_NOT_GIVE_TO_CODERS\sealed_key.json` | `d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734` |
| 53A plaintext | same folder, `53A_V1_RESEARCHER_MAPPING_SEALED_KEY_v2_2.PLAINTEXT.md` | `9d9de02bfb68566d94cd7023fbff14b79f29fb5db8cf8d364fb941cb6b2e0d3d` |

## B. 53A commitment stub (tracked in REPO)

| File | SHA-256 |
|---|---|
| `53A_V1_RESEARCHER_MAPPING_SEALED_KEY_v2_2.md` | `2f864f58a800f17bfd38bf16541f7eff7126c6e1164093159a0d03d72fcc5561` |

## C. Other files that contain the researcher mapping in readable form

These files are hashed so that the mapping cannot be changed after coding without detection. Files marked PUBLIC are tracked in the public repository.

| File | Status | SHA-256 |
|---|---|---|
| `41_G01_G16_CONVERGENCE_AND_CONSTRUCT_FREEZE_v2_1.md` | PUBLIC | `b660fd93875c44cf1fb8ffce3a977295d78d4f225937f10c7e115fa508364e02` |
| `54C_AI_BLIND_CODING_PILOT_RESULTS_v2_2.md` (reproduces the key) | PUBLIC | `b05c72b3071547810b1fa2a2e6cce8d98b30ceb5fb5e8d2e1bd1e52307abdb63` |
| `claude/r14_merge_v1_8_source_closure/08_MERGED_MASTER_THESIS_v1_8_SOURCE_VERIFIED.md` (Tables 3-4, 3-4A, 4-11) | PUBLIC | `1515b0f241846b98a16bea7b13f07d1f82fa9199e1331c2228ffce1d04f7ad58` |
| `W\...\r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.csv` | extracted package, not in git | `7f7d06c4c7d91777dfc2baf7c959a7538780a6a88ffbeec0e891c0d0e7b5aef3` |
| `W\...\r14_merge_v1_7\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX.xlsx` | extracted package, not in git | `be3eda62a10ec9c250c704b63fb0f2ac8a14455c8ba51414be2e08ab476987bd` |
| `OUT\current_artifacts\132_GAP_TO_MECHANISM_TRACEABILITY_MATRIX_v1_8_1.csv` (observed 2026-10-14; written by a sibling agent) | new, uncommitted | `6c7d350960a411be7e1e16d6f70c1ae25ea8f3af5c62035d3b2e2b7e4e35cf5c` |

## D. Frozen analysis script (OA-1)

The `--unseal` mode of this script reads the `sealed_key.json` hash from table A of this file and refuses to compare when the key does not match it.

| File | SHA-256 |
|---|---|
| `tools/I/v1_construct_analyzer.py` | `b5628633a997190a5bf54e25a93c40647ef94494b4ca6f9fe6071454872e278a` |
| `tools/I/test_v1_construct_analyzer.py` (correctness test; random vectors in memory only) | `7fa7b3231a25d17bec4e632df4891ad7707caaf4e4873b5ebca574419f8ad002` |
| `v1_blind/reliability_v2_2.py` (imported unchanged; hash checked at runtime) | `866e9005da8a20e996c93b5c8f6bee916992f24d60c6a96e8f1dcda4556848e7` |

Blinding note: 53A is a hash stub and does not contain the assignments. However, the same mapping appears in readable form in PUBLIC files (41, 54C and the v1.8 manuscript). The hash commitment protects the integrity of the key. It does not protect the blinding of coders. See protocol 19, section 5.
