"""Step 0: data lineage — confirm the private-snapshot metadata matches the official V9 freeze."""
import os, json
from collections import Counter
import ra_lib as L

OUTD = os.path.join(L.OUT, "00_lineage")


def main():
    off = L.read_csv(os.path.join(L.INP, "ANALYTICAL_FREEZE_RECORD_LEVEL.csv"))
    prv = L.read_csv(os.path.join(L.INP, "RECORDS_STRICT_6499_from_private_snapshot.csv"))
    allr = L.read_csv(os.path.join(L.INP, "RECORDS_ALL_26501_from_private_snapshot.csv"))
    docs = {r["document_id"]: r for r in L.read_csv(os.path.join(L.INP, "DOCS_2118_from_private_snapshot.csv"))}
    edges = L.load_official_edges()
    om = {r["record_id"]: r for r in off}
    pm = {r["record_id"]: r for r in prv}
    fields = ["document_id", "left_final_family", "right_final_family", "mapping_completeness", "relation_type"]
    mism = Counter(f for rid in om for f in fields if rid in pm and om[rid][f] != pm[rid][f])
    strict_in_all = sum(1 for r in allr if r["passed_strict_filter"] in ("1", "True", "true"))
    edge_docs = {d for d, _, _ in edges}
    strict_docs = {r["document_id"] for r in off}
    yr = lambda d: docs[d]["year"] if d in docs else ""
    rep = {
        "official_strict_records": len(om), "private_strict_records": len(pm),
        "record_id_sets_identical": set(om) == set(pm),
        "field_mismatches_on_shared_ids": dict(mism),
        "records_all": len(allr), "records_all_passed_strict_filter": strict_in_all,
        "records_all_requires_human_review": dict(Counter(r["requires_human_review"] for r in allr)),
        "docs_total": len(docs), "docs_status": dict(Counter(r["status"] for r in docs.values())),
        "docs_track": dict(Counter(r["track"] for r in docs.values())),
        "strict_documents": len(strict_docs), "strict_documents_in_docs_table": len(strict_docs & set(docs)),
        "edge_documents": len(edge_docs), "edge_documents_in_docs_table": len(edge_docs & set(docs)),
        "edge_documents_status": dict(Counter(docs[d]["status"] for d in edge_docs if d in docs)),
        "edge_documents_track": dict(Counter(docs[d]["track"] for d in edge_docs if d in docs)),
        "edge_documents_with_year": sum(1 for d in edge_docs if yr(d).isdigit()),
        "edge_documents_year_distribution": dict(sorted(Counter(yr(d) for d in edge_docs).items())),
        "edge_documents_identity_level": dict(Counter(docs[d]["identity_level"] for d in edge_docs if d in docs)),
        "edges_by_track": dict(Counter(docs[d]["track"] for d, _, _ in edges if d in docs)),
    }
    L.write_json(os.path.join(OUTD, "LINEAGE_REPORT.json"), rep)
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
