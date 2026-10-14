# S1B_ITEM_ORDER_LOG — COMMITMENT

| File | SHA-256 | Bytes |
|---|---|---|
| S1B_ITEM_ORDER_LOG.json | `a866e074429bc896c7175e5eab53e34457857943033e1adeb84b4aa6366cbb0e` | 1366 |

Plaintext is held in study-team-only storage (`outputs\20_SEALED_PRIVATE\V1_8_2B_S1B_STUDY_TEAM_ONLY\`), not in git (public repository). It contains the three S1b per-coder item orders and their seeds; it contains no item-to-G assignment. The seeds are non-secret (orders are over neutral IDs only and are visible in the coder files); they are also listed in `S1B_PACKET_MANIFEST.csv`.

Checks recorded at build time: the three orders are pairwise distinct, differ from the identity order, and differ from every S1 per-coder order.

The sealed ITEM-ID to G-ID map is unchanged from S1 and was not opened: see `claude/r14_merge_v1_8_2_v1_prefreeze/V1_SEALED/ITEM_ID_TO_GID_MAP.COMMITMENT.md`, SHA-256 of the map `2a84d5de58ec3d13878281d684d82b959d8bc73be7068845bd4cd2f2448cbe81`.
