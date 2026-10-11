# 49 — V5 Corpus Lineage Reconciliation v2.1

**Status: RESOLVED provenance note.**

This note resolves the apparent conflict between the earlier two-track corpus lineage and the V5 network denominator used by G01–G16.

## 1. Frozen V5 chain

The protected V9/V5 artifacts identify four different analytical levels:

1. **6,499 analytical strict-frame records**
2. **3,125 fully mapped / pair-eligible semantic records**
3. **783 pair-eligible unique documents**
4. **2,180 document-level deduplicated AI-family × Decision-family edges**

Thus:

`6,499 strict frame → 3,125 pair-eligible semantic records → 783 pair-eligible documents → 2,180 document-level edges`

The difference between 3,125 and 2,180 is **945** record-level edge occurrences collapsed at document-level deduplication. These are not competing corpus sizes.

Protected-artifact hashes recorded by the V9 human-audit provenance package:

- `analytical_record_level_6499`
  - SHA-256: `FBB5F59286D308771D5DB77B176ABEBAB8EF851A896652A3807EBF6A4B335A8F`
- `fully_mapped_records_3125`
  - SHA-256: `9EE5FD537FED2819C0AC7998D6A786CC8F90DD008EBC1758BB92C8E7487C2E92`
- `document_edges_2180`
  - SHA-256: `3BA370C1804960ED35880F87172114E2C14AF98E2691848F6306F5FE5B1715A2`

## 2. Stage-2 model identity

V5 Stage 2 uses the constrained double-pass mapping workflow with:

`qwen2.5:14b`

This model identity belongs to the V5 family-mapping stage.

## 3. Why the handoff numbers differ

The earlier handoff lineage containing:
- 404 final publications,
- 2,425 strict records,
- GPT-5.6 Sol semantic coding,

describes a predecessor two-track corpus / evidence-generation lineage.

It is retained as historical provenance, but it is **not** the denominator of the frozen V5 G01–G16 network.

Therefore it must not be mixed into the V5 methods sentence that defines `M = 2,180`.

## 4. Canonical manuscript rule

For the enterprise-AI manuscript:

- use `6,499 → 3,125 → 783 → 2,180` when describing the V5 network construction;
- state that `M = 2,180` is the document-level edge denominator used in the network/null-model analysis;
- identify `qwen2.5:14b` specifically as the V5 Stage-2 constrained mapping model;
- retain the earlier 404 / 2,425 / GPT-5.6 Sol lineage only as predecessor provenance if needed in an appendix;
- retain the AI-vs-Decision full-text parity limitation;
- never use corpus counts, O/E, or q-values as enterprise optimization coefficients.

## 5. Freeze implication

The former `[AUTHOR DECISION REQUIRED]` lineage blocker is closed.

This does **not** close:
- V1 independent blind coding,
- enterprise empirical parameter identification,
- solver PENDING items,
- corpus-parity sensitivity,
- reference `[VERIFY]` items.
