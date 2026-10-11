# 55 — V1 Blind-Coding Adjudication Template v2.2

Rules (53B §9 C5): adjudication starts only after all coder outputs of a round are hashed in `v1_blind/FREEZE_MANIFEST.txt`. Coders first discuss without the researcher key; unresolved cases go to an adjudicator who did not author 41. The researcher key is revealed only after adjudicated codes are frozen. If the 41 author adjudicates, mark the row `AUTHOR_ADJUDICATED` and report it as a limitation.

`final_adjudicated_code` stays **blank** until the human round is complete. AI-pilot rows are kept in a separate block and can never fill the human columns.

Disagreement types: `PRIMARY` (primary code differs), `STATUS` (status differs), `SECONDARY` (secondary only), `KEY` (coders agree with each other but not with the researcher key), `NEW_CONSTRUCT` (any coder says yes).

Model-change classes (53B §11): `mapping-only`, `manuscript-only`, `model-structural`.

---

## Block H — Human round (to be completed)

| Case_ID | Coder A (primary/secondary/status) | Coder B | Coder C (optional) | Disagreement type | Evidence used in adjudication | Final adjudicated code (primary/secondary/status) | Adjudicator | Rationale | Model changes? (class) | Manuscript changes? |
|---|---|---|---|---|---|---|---|---|---|---|
| C01 | | | | | | | | | | |
| C02 | | | | | | | | | | |
| C03 | | | | | | | | | | |
| C04 | | | | | | | | | | |
| C05 | | | | | | | | | | |
| C06 | | | | | | | | | | |
| C07 | | | | | | | | | | |
| C08 | | | | | | | | | | |
| C09 | | | | | | | | | | |
| C10 | | | | | | | | | | |
| C11 | | | | | | | | | | |
| C12 | | | | | | | | | | |
| C13 | | | | | | | | | | |
| C14 | | | | | | | | | | |
| C15 | | | | | | | | | | |
| C16 | | | | | | | | | | |

Round statistics (from `v1_blind/reliability_v2_2.py`): α(primary) = ____ [CI ____], κ = ____; α(status) = ____ [CI ____]; class per 53B C1–C3: ____; V1 decision per C6: ____.

---

## Block P — AI-BLIND-CODING PILOT (diagnostic only; not human evidence)

| Case_ID | AI Coder A | AI Coder B | Disagreement type | Evidence considered | AI-pilot provisional reading | Adjudicator | Rationale | Model changes? (class) | Manuscript changes? |
|---|---|---|---|---|---|---|---|---|---|
| C01 (G11) | M4/M5/static | M4/M5/static | KEY (primary + status) | coder rationales; 42 §16 (D1); G05 static I4 gate | unresolved — retained as contested; human round decides | none (pilot) | both AI coders read a single-period assurance gate on allocation; researcher reads cross-period feedback | no (`mapping-only`) | yes: flag G11 as contested in 41/44; M5 rests on G12 if human coders agree with AI |
| C03 (G04) | M4/M3/static | M4/—/static | KEY (primary + status); SECONDARY | coder rationales; I4 elements in 42 | unresolved | none (pilot) | generic "validate generated output" reading versus researcher's "no distinct decision" | no (`mapping-only`) | yes: evidence-only count may change |
| C11 (G10) | M3/M1/static | M3/M4/static | KEY (status); SECONDARY | 43 Block R identification rule for `P(z,ω|k_τ)` | unresolved | none (pilot) | data gate not salient in coding; it is enforced by identification rules anyway | no (`mapping-only`) | yes: describe "optional" as an identification condition |
| C07 (G05) | M4/M1/static | M4/M3/static | SECONDARY | — | none needed (primary and status agree with each other and key) | — | — | no | no |
| C12 (G03) | M2/M1/static | M2/M4/static | SECONDARY | — | none needed | — | — | no | no |
| C08 (G14) | M2/—/static | M2/—/static | none (low confidence 45; B flags EVIDENCE_ONLY as plausible) | — | watch item for human round | — | residual decision family | no | no |
