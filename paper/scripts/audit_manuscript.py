"""Integrity audit for the manuscript (PaperOrchestra 'data integrity / citation integrity' check, automated).

Checks, for paper/en/*.tex (or paper/zh/*.tex with --zh):
  1. every number in the prose appears in experimental_log.md (or in the allow-list below);
  2. every \\cite key exists in references.bib;
  3. every \\ref / \\label pair resolves, and labels are unique;
  4. every figure file referenced exists; every figure in paper/figures is used;
  5. claim-boundary phrases that must not appear.
Exit code 1 if any check fails.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ALLOW = {
    # structural / definitional numbers that are not results
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "16", "100", "0.05", ".05", "05", "0.01", ".01",
    "1.0", "2.0", "3.0", "0.0", "1.00", "0.00", "95", "50", "25", "20", "30", "40", "60", "80", "1.5", "2,000", "1,000",
    "2010", "2013", "2015", "2017", "2018", "2019", "2023", "2024", "2025", "2026", "1976",
    "1951", "1960", "1973", "1977", "1981", "1985", "1989", "1992", "1993", "1995", "2001", "2002", "2004", "2006",
    "2007", "2013", "2015", "2018", "2019", "2020", "2021", "2022",
}
NUM = re.compile(r"(?<![A-Za-z0-9_.\\{])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![A-Za-z0-9_}])")  # ASCII boundaries so CJK-adjacent numbers are checked
FORBIDDEN = [r"\bresearch gaps?\b(?![^.]{0,80}(not|no evidence|unsupported|NOT))", r"confirmed structural hole(?! at any)",
             r"\bcentrali[sz]ed\b", r"\bfederated\b", r"\bdecentrali[sz]ed\b", r"13 versions"]


def strip_tex(t):
    t = t.replace("{,}", ",")
    t = re.sub(r"(?<!\\)%.*", "", t)                                   # comments
    t = re.sub(r"\\(label|ref|eqref|cite[pt]?|citet|citep|includegraphics|input|url|href)\*?(\[[^\]]*\])?\{[^}]*\}", " ", t)
    t = re.sub(r"\\begin\{[^}]*\}(\{[^}]*\})?|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\[width=[^\]]*\]", " ", t)
    t = re.sub(r"\\(vspace|hspace|setlength|arraystretch)\{[^}]*\}", " ", t)
    return t


def main(zh=False):
    base = HERE / ("zh" if zh else "en")
    files = sorted(base.glob("*.tex"))
    log = (HERE / "raw_materials" / "experimental_log.md").read_text(encoding="utf-8")
    log_extra = (HERE / "raw_materials" / "idea.md").read_text(encoding="utf-8")
    lognums = set(NUM.findall(log)) | set(NUM.findall(log_extra))
    lognorm = {n.replace(",", "") for n in lognums}
    bib = (HERE / "references.bib").read_text(encoding="utf-8")
    bibkeys = set(re.findall(r"@\w+\{([^,]+),", bib))
    fail = 0
    labels, refs, figs = {}, set(), set()
    for f in files:
        raw = f.read_text(encoding="utf-8")
        for k in re.findall(r"\\label\{([^}]*)\}", raw):
            if k in labels:
                print(f"DUPLICATE LABEL {k} in {f.name} and {labels[k]}"); fail = 1
            labels[k] = f.name
        refs |= set(re.findall(r"\\(?:ref|eqref|autoref|cref)\{([^}]*)\}", raw))
        for group in re.findall(r"\\cite[pt]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", raw):
            for k in group.split(","):
                if k.strip() not in bibkeys:
                    print(f"UNKNOWN CITE {k.strip()} in {f.name}"); fail = 1
        figs |= set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", raw))
        body = strip_tex(raw)
        for n in NUM.findall(body):
            if n in ALLOW or n.replace(",", "") in lognorm or n in lognums:
                continue
            ctx = body[max(0, body.find(n) - 50): body.find(n) + 50].replace("\n", " ")
            print(f"NUMBER NOT IN LOG {n!r} in {f.name}: ...{ctx}..."); fail = 1
        flat = re.sub(r"\s+", " ", body)
        for pat in FORBIDDEN:
            for m in re.finditer(pat, flat, flags=re.I):
                before = flat[max(0, m.start() - 60):m.start()].lower()
                if re.search(r"\b(not|no|never|nor|without|neither|rather than|instead of|absence of|fails? to)\b[^.;]*$", before):
                    continue                                        # negated or contrasted use is allowed
                print(f"FORBIDDEN PHRASE {m.group(0)!r} in {f.name}: ...{flat[max(0, m.start()-90):m.end()+40]}..."); fail = 1
    for r in sorted(refs - set(labels)):
        print(f"UNRESOLVED REF {r}"); fail = 1
    have = {p.name for p in (HERE / "figures").glob("*.png")}
    for g in sorted(figs):
        if Path(g).name not in have:
            print(f"MISSING FIGURE FILE {g}"); fail = 1
    for g in sorted(have - {Path(x).name for x in figs}):
        print(f"UNUSED FIGURE {g}"); fail = 1
    print("AUDIT", "FAIL" if fail else "PASS", f"({len(files)} files, {len(labels)} labels, {len(refs)} refs, {len(figs)} figures)")
    return fail


if __name__ == "__main__":
    sys.exit(main("--zh" in sys.argv))
