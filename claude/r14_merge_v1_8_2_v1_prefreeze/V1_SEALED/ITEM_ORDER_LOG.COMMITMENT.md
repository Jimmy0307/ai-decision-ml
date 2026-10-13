# ITEM_ORDER_LOG — COMMITMENT (v1.8.2)

| File | SHA-256 | Bytes |
|---|---|---|
| ITEM_ORDER_LOG.json | `79cd727f1bde80da735dcdd2bd2486a217c6cabe75150988343966880ce3957d` | 1628 |
| SECRET_SEED_v1_8_2.txt | `79caee63306e333f50a7487c92fa1ae419fdc93c534250200a1bc65a2cc9e4e9` | 19 |

The log holds the secret seed, the input G order, the neutral-ID assignment and the three per-coder item orders. The seed was generated once with Python `secrets`; neutral IDs and orders are derived from it by the rules in `tools/build_v1_packet_v182.py`. The seed is secret because the builder is public, and anyone holding the seed could recompute the map.

The plaintext is held in study-team-only controlled storage (`20261014_V1_8_2_PREFREEZE\SEALED_LOCAL_STUDY_TEAM_ONLY\`). It is not committed because the repository is public.
