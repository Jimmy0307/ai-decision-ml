"""Assemble W/05_LEGACY_SOURCE_BOUNDARY.md from header/footer + audit json.
Usage: python -I assemble.py <audit_json> <header_md> <footer_md> <out_md>
"""
import json, sys
from pathlib import Path

res = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
TYPE = {".md": "Markdown text", ".csv": "CSV data", ".png": "PNG figure", ".json": "JSON data"}
rows = ["| # | Relative path (under 完整資料來源/) | sha256[:16] | Type | Size (B) | Analysis family | Filename date | Zip entry mtime | Inventory sha match |",
        "|---:|---|---|---|---:|---|---|---|---|"]
for i, f in enumerate(res["files"], 1):
    rows.append(f"| {i} | `{f['rel']}` | `{f['sha16']}` | {TYPE.get(f['ext'], f['ext'])} | {f['size']} | {f['family']} | "
                f"{f['name_date'] or '—'} | {f['zip_mtime']} | {'YES' if f['inventory_sha_match'] else 'NO'} |")
fam = {}
for f in res["files"]:
    fam[f["family"]] = fam.get(f["family"], 0) + 1
famtab = ["| Analysis family | Files |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in sorted(fam.items(), key=lambda x: -x[1])]
body = Path(sys.argv[2]).read_text(encoding="utf-8")
body = body.replace("{{FAMILY_TABLE}}", "\n".join(famtab)).replace("{{FILE_TABLE}}", "\n".join(rows))
body += Path(sys.argv[3]).read_text(encoding="utf-8")
Path(sys.argv[4]).write_text(body, encoding="utf-8")
print("rows", len(res["files"]), "families", fam)
