# ITEM_ID_TO_GID_MAP — COMMITMENT (v1.8.2)

| File | SHA-256 | Bytes |
|---|---|---|
| ITEM_ID_TO_GID_MAP.json | `2a84d5de58ec3d13878281d684d82b959d8bc73be7068845bd4cd2f2448cbe81` | 416 |

The plaintext is held in study-team-only controlled storage (`20261014_V1_8_2_PREFREEZE\SEALED_LOCAL_STUDY_TEAM_ONLY\`). It is not committed because the repository is public.

Use: the analyzer (`tools/v1_construct_analyzer_v182.py`) accepts the map only after phase S3 (adjudication frozen), and only if its SHA-256 equals the value above. The map is used only for the G04/G10/G11 sensitivity analysis and to index the researcher key at phase K. Primary reliability (phase R) is computed on neutral item IDs without the map.
