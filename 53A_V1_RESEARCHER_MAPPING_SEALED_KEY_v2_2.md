# 53A — V1 Researcher Mapping SEALED KEY v2.2 (commitment stub)

The researcher-adjudicated mapping (41 §2 in 53B vocabulary) and the blinded Case-ID ↔ Gap-ID table are **sealed**. Only this hash commitment is kept on the research branch, so that coders given packet access cannot read the key, and so that the key cannot be altered after coder outputs are seen.

| Sealed object | SHA-256 |
|---|---|
| 53A plaintext (markdown table: Case_ID, Gap_ID, families, researcher primary/secondary/status) | `9d9de02bfb68566d94cd7023fbff14b79f29fb5db8cf8d364fb941cb6b2e0d3d` |
| sealed_key.json (machine-readable) | `d1702188359e2efa872ae3d5a3ebdae8b75bb220b49931af4f2f59e524936734` |

**Unsealing rule:** the plaintext is added to this branch only after (i) all coders of a round have submitted and their outputs are hashed in `v1_blind/FREEZE_MANIFEST.txt`, and (ii) the hash of the added plaintext equals the value above. For the AI pilot round the plaintext is reproduced in `54C` after the AI outputs were frozen.

Caveat: file 41 on this public branch contains the same mapping in prose. Human coders must sign the 53B §8 attestation; packets are delivered outside the repository.
