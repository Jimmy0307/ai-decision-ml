# V1 human blind-coding packet (v2.2.1)

You will code 16 cases. Time: about 45–60 minutes. Work alone.

1. Read `CODER_PROTOCOL_53B_sections_1-8.md`, then `CODER_CLARIFICATIONS_v2_2_1.md`.
2. Open the packet you were assigned (`PACKET_A.csv` or `PACKET_B.csv`) and the matching `RESPONSE_SHEET_A.csv` / `RESPONSE_SHEET_B.csv`.
3. Fill one row per case. Do not change case IDs.
4. Sign the attestation in protocol §8 (name, date) and return the response sheet to the study coordinator.

Do not consult the project repository, the manuscript, or other coders until you have submitted.

## For the study coordinator

- Assign at least two coders; alternate packets A and B.
- On receipt, compute SHA-256 of each response sheet and append it to `v1_blind/FREEZE_MANIFEST.txt` (stage 3) **before** running the analysis or revealing the key.
- Run `python v1_blind/reliability_v2_2.py <sheet1> <sheet2> [...]`; then, only after the hashes are recorded, add `--key` with the unsealed key (verify its hash against 53A).
- Record every disagreement in `55_V1_BLIND_CODING_ADJUDICATION_TEMPLATE_v2_2.md` and apply 53B §9–§11.
- Disclose that the clarifications were written after the AI pilot was compared with the researcher key (54C §6).
