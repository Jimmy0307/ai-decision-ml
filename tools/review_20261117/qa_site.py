"""Static QA gate for the AI x Decision research website (standard library only).

    python tools/review_20261117/qa_site.py [--repo .] [--base origin/main]

Exit code 0 only if every gate passes. Output is a plain-text gate table.
"""
from __future__ import annotations

import argparse
import csv
import html.parser
import os
import re
import subprocess
import sys
import urllib.parse


def read_text(path: str, **kw) -> str:
    with open(path, encoding="utf-8", **kw) as f:
        return f.read()

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
NEGATION = re.compile(r"(不|非|未|勿|否|沒|無|≠|不可|不能|不得|不等於|不是|not|no |never|isn't|is not|cannot)", re.I)

# Phrases that must never appear as an affirmative claim on the public site.
OVERCLAIMS = [
    r"16\s*(個|组|組)?\s*Burt\s*(holes?|結構洞)",
    r"16\s*(個|組)\s*結構洞",
    r"Pages\s*(已|已經)?\s*(部署|上線)\s*(成功|完成)",
    r"deployed\s+successfully",
    r"(142|100)\s*(個|篇|項)?\s*(未解|confirmed)",
    r"V11\.1\s*(是|=|＝)\s*Limitation",
    r"constraint\s*(已|已經)?\s*(失效|被證偽)",
    r"structural[- ]hole theory (is|was) (falsified|refuted)",
]

REQUIRED_INDEX_LABELS = [
    "V11.1 user-reported raw local-only",
    "V9 full reanalysis pending",
    "Limitation candidate scan only",
    "PENDING_LOCAL_RECOVERY",
]

ORIGINAL_SECTION_IDS = ["weekly", "summary", "timeline", "methods", "numbers", "core",
                        "candidates", "risk", "recover", "sources", "literature"]

REVIEW_FILES = [
    "docs/review/20261117/INDEPENDENT_SOURCE_AUDIT.md",
    "docs/review/20261117/CORRECTION_LOG.csv",
    "docs/review/20261117/BIBLIOGRAPHY_VERIFICATION.csv",
    "docs/review/20261117/FORMULA_VALIDITY_NOTES.md",
    "docs/review/20261117/PROVENANCE_LIMITS.md",
    "docs/review/20261117/METRIC_AUDIT_90.csv",
    "docs/review/20261117/RECOMPUTE_RESULTS.json",
    "docs/review/20261118_data_validity/DATA_VALIDITY_VERDICT.md",
    "docs/review/20261118_data_validity/data/ROBUSTNESS_MASTER_TABLE.csv",
]

FORBIDDEN_ADDED_EXT = {".zip", ".pdf", ".sqlite", ".db", ".7z", ".rar", ".docx", ".xlsx", ".pptx", ".pem", ".key"}
SECRET_PATTERNS = {
    "github-token": r"ghp_[A-Za-z0-9]{20,}",
    "github-fine-grained-token": r"github_pat_[A-Za-z0-9_]{20,}",
    "private-key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "aws-key": r"AKIA[0-9A-Z]{16}",
    "api-key": r"sk-[A-Za-z0-9]{20,}",
    "work-email": r"[A-Za-z0-9._%+-]+@jpcco\.com",
    "local-user-path": r"[A-Za-z]:(?:\\|/)+Users(?:\\|/)",
}


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.tables: dict[str, int] = {}
        self._table: list[str | None] = []
        self._in_tbody = 0
        self.tables_unwrapped: list[str] = []
        self.meta_viewport = False
        self.lang = None
        self.title = ""
        self._in_title = False
        self._div_classes: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name") == "viewport":
            self.meta_viewport = True
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "title":
            self._in_title = True
        if tag == "table":
            tid = a.get("id") or f"(anon@{self.getpos()[0]})"
            self._table.append(tid)
            self.tables.setdefault(tid, 0)
            if not any("table-scroll" in c for c in self._div_classes[-1:]):
                self.tables_unwrapped.append(tid)
        if tag == "tbody":
            self._in_tbody += 1
        if tag == "tr" and self._in_tbody and self._table:
            self.tables[self._table[-1]] += 1
        if tag == "div":
            self._div_classes.append(a.get("class") or "")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "title":
            self._in_title = False
        if tag == "table" and self._table:
            self._table.pop()
        if tag == "tbody":
            self._in_tbody -= 1
        if tag == "div" and self._div_classes:
            self._div_classes.pop()
        # HTML optional end tags (p, li, td, th, tr ...) are tolerated by closing implicitly.
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, line in self.stack[i + 1:]:
                    if t not in {"p", "li", "td", "th", "tr", "thead", "tbody", "option", "dt", "dd"}:
                        self.errors.append(f"unclosed <{t}> (line {line}) before </{tag}>")
                del self.stack[i:]
                return
        self.errors.append(f"stray </{tag}> at line {self.getpos()[0]}")

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def parse(path: str) -> Page:
    p = Page()
    with open(path, encoding="utf-8") as f:
        p.feed(f.read())
    p.close()
    for t, line in p.stack:
        if t not in {"p", "li", "td", "th", "tr", "thead", "tbody", "html", "body"}:
            p.errors.append(f"unclosed <{t}> at EOF (opened line {line})")
    return p


def visible_text(path: str) -> str:
    raw = read_text(path)
    raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))


def overclaims(text: str) -> list[str]:
    hits = []
    for pat in OVERCLAIMS:
        for m in re.finditer(pat, text, flags=re.I):
            window = text[max(0, m.start() - 80):m.start()]
            if not NEGATION.search(window):
                hits.append(f"{pat!r} -> …{text[max(0, m.start() - 40):m.end() + 20]}…")
    return hits


def csv_rows(path: str) -> int:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return len(list(csv.DictReader(f)))


def check_links(repo: str, page_path: str, page: Page) -> list[str]:
    bad = []
    base = os.path.dirname(page_path)
    ids = set(page.ids)
    for h in page.hrefs:
        if h.startswith(("http://", "https://", "mailto:")):
            continue
        if h.startswith("#"):
            if h[1:] and h[1:] not in ids:
                bad.append(f"missing anchor {h}")
            continue
        target = urllib.parse.unquote(h.split("#", 1)[0].split("?", 1)[0])
        if not os.path.exists(os.path.normpath(os.path.join(base, target))):
            bad.append(f"missing file {h}")
    return bad


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, encoding="utf-8").stdout


def run(repo: str, base: str) -> list[tuple[str, bool, str]]:
    gates: list[tuple[str, bool, str]] = []
    add = lambda name, ok, detail="": gates.append((name, bool(ok), detail))
    docs = os.path.join(repo, "docs")
    index = os.path.join(docs, "index.html")
    theory = os.path.join(docs, "THEORY_LITERATURE_COMPARISON_20261117.html")

    for path in (index, theory):
        p = parse(path)
        rel = os.path.relpath(path, repo).replace(os.sep, "/")
        add(f"{rel}: well-formed tags", not p.errors, "; ".join(p.errors[:5]))
        dups = sorted({i for i in p.ids if p.ids.count(i) > 1})
        add(f"{rel}: no duplicate id", not dups, ", ".join(dups))
        bad = check_links(repo, path, p)
        add(f"{rel}: relative href/anchor targets exist", not bad, "; ".join(bad[:8]))
        add(f"{rel}: lang+title+viewport", p.lang and p.title.strip() and p.meta_viewport, f"lang={p.lang}")
        add(f"{rel}: every table wrapped in .table-scroll (mobile)", not p.tables_unwrapped, ", ".join(p.tables_unwrapped))
        oc = overclaims(visible_text(path))
        add(f"{rel}: no affirmative overclaims", not oc, " | ".join(oc[:3]))
        if path == index:
            idx = p
    css = read_text(index)
    add("index: responsive @media rule present", re.search(r"@media\s*\(max-width", css) is not None)
    expect = {"versions": 13, "methods-table": 20, "metrics": 90, "core-table": 32, "refs-table": 12, "formula-table": 8}
    for tid, n in expect.items():
        got = idx.tables.get(tid)
        add(f"index: table#{tid} has {n} rows", got == n, f"got {got}")
    missing = [s for s in ORIGINAL_SECTION_IDS if s not in idx.ids]
    add("index: original sections preserved", not missing, ", ".join(missing))
    add("index: search/filter function preserved", "function filterTable" in css)
    vt = visible_text(index)
    miss = [l for l in REQUIRED_INDEX_LABELS if l not in vt]
    add("index: required status labels visible", not miss, ", ".join(miss))

    tv = visible_text(theory)
    add("theory: 12 references R01–R12", all(f"R{i:02d}" in tv for i in range(1, 13)))
    add("theory: 8 equations E1–E8", all(f"E{i}" in tv for i in range(1, 9)))

    for name, n in [("docs/data/VERSION_METHOD_REGISTER_20261117.csv", 13),
                    ("docs/data/METHOD_VALIDATION_MATRIX_20261117.csv", 20),
                    ("docs/data/ALL_METRICS_WITH_PROVENANCE_20261117.csv", 90),
                    ("docs/data/LITERATURE_METHODS_20261117.csv", 12),
                    ("docs/review/20261117/METRIC_AUDIT_90.csv", 90),
                    ("docs/review/20261117/BIBLIOGRAPHY_VERIFICATION.csv", 12)]:
        p = os.path.join(repo, name)
        got = csv_rows(p) if os.path.exists(p) else None
        add(f"{name}: {n} rows", got == n, f"got {got}")
    miss = [f for f in REVIEW_FILES if not os.path.exists(os.path.join(repo, f))]
    add("review deliverables present", not miss, ", ".join(miss))
    cl = os.path.join(repo, "docs/review/20261117/CORRECTION_LOG.csv")
    if os.path.exists(cl):
        with open(cl, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        need = {"item_id", "original_value", "corrected_value", "evidence", "status"}
        add("correction log: schema + before/after recorded", rows and need <= set(rows[0]) and all(r["original_value"] and r["corrected_value"] for r in rows), f"{len(rows)} rows")

    # Diff-scoped guards (only files changed relative to base).
    changed = [l for l in git(repo, "diff", "--name-only", base, "--").splitlines() if l]
    changed += [l for l in git(repo, "ls-files", "--others", "--exclude-standard").splitlines() if l]
    bad_ext = [f for f in changed if os.path.splitext(f)[1].lower() in FORBIDDEN_ADDED_EXT]
    add("diff: no raw archives/fulltexts/binaries added", not bad_ext, ", ".join(bad_ext))
    big = [f for f in changed if os.path.exists(os.path.join(repo, f)) and os.path.getsize(os.path.join(repo, f)) > 1_000_000]
    add("diff: no file > 1 MB", not big, ", ".join(big))
    leaks = []
    for f in changed:
        p = os.path.join(repo, f)
        if not os.path.isfile(p) or f.startswith("tools/review_20261117/"):
            continue
        txt = read_text(p, errors="replace")
        for label, pat in SECRET_PATTERNS.items():
            if re.search(pat, txt):
                leaks.append(f"{f}: {label}")
    add("diff: no secrets / work email / local user paths", not leaks, "; ".join(leaks[:5]))
    lem = [f for f in changed if re.search(r"(LEM2|drsa|recruit)", f, re.I)]
    add("diff: no LEM2/DRSA/recruitment paths touched", not lem, ", ".join(lem))
    chk = subprocess.run(["git", "-C", repo, "diff", "--check", base, "--"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    out = chk.stdout or ""
    add("git diff --check (whitespace)", chk.returncode == 0 and not out.strip(), out[:300])
    return gates


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", default="origin/main")
    a = ap.parse_args(argv)
    gates = run(os.path.abspath(a.repo), a.base)
    width = max(len(g[0]) for g in gates)
    for name, ok, detail in gates:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  {detail}".rstrip())
    failed = sum(not g[1] for g in gates)
    print(f"\n{len(gates) - failed}/{len(gates)} gates PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
