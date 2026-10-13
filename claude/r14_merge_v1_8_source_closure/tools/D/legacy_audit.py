"""Phase 6 legacy-zip audit (sub-agent D). Read-only over W.
Usage: python -I legacy_audit.py <W_root> <out_json>
"""
import csv, hashlib, json, re, sys
from pathlib import Path

W = Path(sys.argv[1])
OUT = Path(sys.argv[2])
LEG = W / "03_LEGACY_FULL_SOURCE" / "完整資料來源"
M = W / "01_ALL_OUTPUTS" / "AI_DECISION_THESIS_ALL_OUTPUTS" / "r14_merge_v1_7"
TARGETS = {
    "130": next(M.glob("130_*v1_7*.md")),
    "128": M / "128_CANONICAL_STATE.md",
}
BIG = {"q1_upgrade_citation_multisource_mapping_2026-04-22.csv",
       "q1_upgrade_citation_multisource_mapping_phase2_2026-04-22.csv"}

def family(rel):
    r = rel.lower()
    if "pca" in r or "fa_" in r or "temporal_phase" in r: return "PCA/FA (yearly temporal features)"
    if "main_path" in r or "splc" in r or "citation" in r or "multi_path" in r: return "Citation network / main path (SPLC/SPNP)"
    if "structural_hole" in r or "tier" in r or "top15_gap" in r: return "Structural-hole tier ranking + Monte Carlo"
    if "info_gap" in r or "expert" in r: return "Info-gap / structural-hole priority + expert question bank"
    if "external" in r or "openalex" in r: return "External validation (OpenAlex/temporal holdout)"
    if "ablation" in r: return "Ablation sensitivity of gap_priority"
    if "network_baseline" in r or "uncertainty" in r or "classical_metrics" in r: return "Classical network metrics (betweenness/Burt constraint) vs gap_priority"
    if "backbone" in r or "concept_network" in r or "enhanced_concept" in r: return "Concept co-occurrence backbone network"
    if "thesis" in r or "q1_improvement" in r or "task" in r: return "Old thesis draft / revision plans"
    if "error_taxonomy" in r or "reproducibility" in r or "closeout" in r or "dashboard" in r: return "QA / closeout / manifest"
    if "readme" in r: return "Package README"
    return "Other"

inv = {}
with open(W / "01_FILE_INVENTORY.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if row["source_package"] == "03_LEGACY_FULL_SOURCE":
            inv[row["relative_path"].replace("完整資料來源/", "", 1)] = row

files = []
for p in sorted(LEG.rglob("*")):
    if not p.is_file(): continue
    rel = p.relative_to(LEG).as_posix()
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    m = re.search(r"(20\d\d-\d\d-\d\d)", p.name)
    iv = inv.get(rel, {})
    files.append({"rel": rel, "sha256": sha, "sha16": sha[:16], "ext": p.suffix.lower(),
                  "size": p.stat().st_size, "name_date": m.group(1) if m else "",
                  "zip_mtime": iv.get("modified_time", ""),
                  "inventory_sha_match": (iv.get("sha256") == sha) if iv else None,
                  "family": family(rel)})

# distinctive tokens from legacy text
num_re = re.compile(r"(?<![\w.])-?\d+\.\d{3,}(?![\d])|(?<![\w.])\d{1,3}(?:,\d{3})+(?![\d,])|\d+\.\d+%")
tokens = {}
for fobj in files:
    if fobj["ext"] not in (".md", ".csv", ".json"): continue
    p = LEG / fobj["rel"]
    text = p.read_text(encoding="utf-8-sig", errors="replace")
    if p.name in BIG or "edges_in_corpus" in p.name: text = text.splitlines()[0]
    for t in num_re.findall(text):
        tokens.setdefault(t, set()).add(fobj["rel"])
concepts = []
for line in (LEG / "輸出" / "structural_hole_marked_list_2026-04-22.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*\d+\s*\|\s*([^|]+?)\s*\|", line)
    if m: concepts.append(m.group(1))
terms = ["structural hole", "結構洞", "Burt", "constraint", "約束", "制約", "main path", "主路徑", "SPLC", "SPNP",
         "SPC", "PCA", "主成分", "factor analysis", "因素分析", "varimax", "Kaiser", "citation network", "引用網路",
         "citation edge", "OpenAlex", "Monte Carlo", "gap_priority", "Tier-A", "Tier-B", "info_gap", "完整資料來源",
         "2,003", "1,981", "98.90", "AI 治理", "AI governance", "bridging", "betweenness", "Jaccard", "backbone", "骨幹"]

def hits(path, needle, ci=True):
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if (needle.lower() in line.lower()) if ci else (needle in line):
            out.append({"line": i, "ctx": line.strip()[:220]})
    return out

res = {"files": files, "term_hits": {}, "token_hits": {}, "concept_hits": {}, "n_tokens": len(tokens)}
for k, tp in TARGETS.items():
    res["term_hits"][k] = {t: hits(tp, t, ci=(t not in ("SPC", "PCA"))) for t in terms}
    res["token_hits"][k] = {t: {"legacy_files": sorted(src), "hits": h} for t, src in tokens.items()
                            if (h := hits(tp, t, ci=False))}
    res["concept_hits"][k] = {c: h for c in concepts if (h := hits(tp, c, ci=False))}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("files", len(files), "inv_match", sum(1 for f in files if f["inventory_sha_match"]), "tokens", len(tokens))
for k in TARGETS:
    print(k, "terms:", {t: len(v) for t, v in res["term_hits"][k].items() if v})
    print(k, "token hits:", {t: [x["line"] for x in v["hits"]] for t, v in res["token_hits"][k].items()})
    print(k, "concept hits:", {c: [x["line"] for x in v] for c, v in res["concept_hits"][k].items()})
