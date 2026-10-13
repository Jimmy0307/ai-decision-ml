# Coder clarifications v2.2.1 (human round)

These clarifications supplement the protocol (sections 1–8). They do not change the codes or the question.

## A. Status decision procedure

Answer in order and stop at the first "yes":

1. To study how this connection is configured, would you need outcomes observed over more than one period (for example, results from one cycle used to change the next)? → `dynamic`
2. Does a configuration choice exist only if a specific dataset is available (name it — e.g., labelled outcomes, score distributions)? → `optional`
3. Is there a distinct choice the enterprise makes in a single period about this connection? → `static`
4. Otherwise → `evidence-only` (or `insufficient` if you cannot decide).

## B. When to use EVIDENCE_ONLY

Ask: "Would naming this specific pairing change what an enterprise has to decide, compared with any other AI function feeding the same decision function?" If the only mechanism you can name would apply equally to almost any AI function (for example, "validate the output"), consider `EVIDENCE_ONLY`; if the pairing raises a mechanism question specific to it, code the mechanism. Both answers are legitimate.

## C. Residual decision families

"General Decision Process" is a residual category. Code it like any other family if you can name a mechanism from the definitions; use `EVIDENCE_ONLY` or `INSUFFICIENT_INFORMATION` if you cannot.

## D. Secondary codes

Leave `secondary_code` blank unless a second mechanism is clearly necessary. Secondary codes are not used in the main reliability statistic.

## E. Confidence

Use the full 0–100 range; it is diagnostic only.
