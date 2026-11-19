"""Prose word count per manuscript file (tables, figures, equations and LaTeX commands removed)."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def prose(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{(table|figure|equation|align|tabular|gather|multline)\*?\}.*?\\end\{\1\*?\}", " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " X ", t)
    t = re.sub(r"\\(label|ref|eqref|cite[pt]?|citealp|includegraphics|input)\*?(\[[^\]]*\])*\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}~\[\]]", " ", t)
    return len(re.findall(r"[A-Za-z\u4e00-\u9fff][A-Za-z'\-]*|\d[\d,.]*", t))


def main(lang="en"):
    names = ["abstract", "front", "studies", "back", "appendix"] if lang == "en" else [p.stem for p in sorted((HERE / lang).glob("*.tex"))]
    main_total = 0
    for n in names:
        f = HERE / lang / f"{n}.tex"
        if not f.exists():
            continue
        c = prose(f.read_text(encoding="utf-8"))
        print(f"{n:10s} {c:6d}")
        if n in ("front", "studies", "back"):
            main_total += c
    print(f"main text (front+studies+back) prose words: {main_total}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "en")
