"""One-off harmonisation of the Chinese translation (chapter/section units, plan numbering, suite name)."""
import re
from pathlib import Path

ZH = Path(__file__).resolve().parents[1] / "zh"
# labels that sit on \chapter in the Chinese build -> unit 章; everything else -> 節
CHAPTER_LABELS = {"zh:sec:intro", "zh:sec:theory", "zh:sec:design", "zh:ch:results", "zh:ch:discussion",
                  "zh:sec:conclusion", "zh:app:prereg", "zh:app:sens", "zh:app:mlp"}
changes = 0
for f in sorted(ZH.glob("*.tex")):
    t = f.read_text(encoding="utf-8")
    orig = t
    # the Discussion chapter overview should point at the chapter, not its first section
    t = t.replace(r"第~\ref{zh:sec:discussion}~章", r"第~\ref{zh:ch:discussion}~章")

    def unit(m):
        lab, u = m.group(1), m.group(2)
        want = "章" if lab in CHAPTER_LABELS else "節"
        return f"第~\\ref{{{lab}}}~{want}"
    t = re.sub(r"第~\\ref\{([^}]+)\}~(章|節)", unit, t)
    for a, b in (("計畫一", "計畫 1"), ("計畫二", "計畫 2"), ("計畫三", "計畫 3"), ("計畫四", "計畫 4"),
                 ("完整複製檢定組", "完整重現套組"), ("複製檢定組", "重現套組")):
        t = t.replace(a, b)
    if t != orig:
        changes += 1
        f.write_text(t, encoding="utf-8")
        print("updated", f.name)
print("files changed:", changes)
