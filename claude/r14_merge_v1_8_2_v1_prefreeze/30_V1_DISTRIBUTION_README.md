# 30 — V1 Distribution README (study coordinator)

1. **What each coder gets.** Send exactly one file to each coder, directly from the researcher by e-mail or controlled file transfer. **Never use GitHub, and never send a repository link.**
   - CODER_1 receives `coder_distribution/CODER_1.xlsx`.
   - CODER_2 receives `coder_distribution/CODER_2.xlsx`.
   - CODER_3 receives `coder_distribution/CODER_3.xlsx`.

   Before sending, confirm that each file's SHA-256 equals the value in `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S1.txt`. Log the send date and the hash outside git.
2. **Files that must never reach a coder.** This applies to everything else, in particular:
   - `20_MASTER_PACKET_v1_8_2.xlsx`, which contains all three coder sheets;
   - 24–29;
   - `V1_SEALED/`;
   - `tools/`;
   - SEALED_LOCAL.
3. **S1 is invalidated by any change.** Once any coder has received a packet, any change to the packet content, codebook, protocol or analyzer **invalidates S1**. If a change is unavoidable, it must be versioned, re-frozen and disclosed. Coders who already received the old version are reported separately.
4. **Handling returned sheets.**
   - Keep completed sheets in local, controlled storage only. **Never push them to the public repository**, and never put them in OUT.
   - Run the format check (codebook 26 §2) and request corrections only for format errors. Never give content feedback.
   - Then compute each sheet's SHA-256 and write it into `V1_SEALED/FREEZE_MANIFEST_V1_8_2_S2.txt` (phase S2) before any analysis.
5. **Analysis.** Run phase R only after S2:

   ```
   python -E -P tools/v1_construct_analyzer_v182.py <C1.xlsx> <C2.xlsx> <C3.xlsx> --s2-manifest <S2 manifest> --out <local dir>
   ```

   Then continue as described in 25 §7 and 29.
6. **What may be published.** Only de-identified aggregate results may go into the repository or the manuscript, and only after the researcher has reviewed them. No coder names, raw sheets or individual rationales are published.
7. **Item map and key.** The item map and the researcher key stay in controlled storage (SEALED_LOCAL / outside git). They are used only after S3 (29 §6).
