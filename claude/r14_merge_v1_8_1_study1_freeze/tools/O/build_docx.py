"""Build DOCX from canonical Markdown via pandoc (LaTeX math -> native OMML) and verify structure.

Usage: <venv python> build_docx.py <in.md> <out.docx> <report.json> [resource_path]

The canonical Markdown is never modified. One render-only transform is applied to a temporary copy:
a $$ display block whose top level contains a TeX line break (two backslashes) and no environment
is wrapped in \\begin{aligned} ... \\end{aligned}, because pandoc cannot emit OMML for a bare line
break. The math tokens inside the block are unchanged; every wrapped block is logged in the report.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

import pypandoc

LINEBREAK = "\\\\"
BEGIN = "\\begin{"


def wrap_linebreak_blocks(md, log):
    def _wrap(m):
        inner = m.group(1)
        if LINEBREAK in inner and BEGIN not in inner:
            log.append(inner.strip()[:160])
            return "$$\n\\begin{aligned}" + inner + "\\end{aligned}\n$$"
        return m.group(0)
    return re.sub(r"\$\$(.+?)\$\$", _wrap, md, flags=re.S)


def md_counts(md):
    body = re.sub(r"```.*?```", "", md, flags=re.S)
    display = len(re.findall(r"\$\$.+?\$\$", body, flags=re.S)) + len(re.findall(r"\\\[.+?\\\]", body, flags=re.S))
    nodisp = re.sub(r"\$\$.+?\$\$", "", body, flags=re.S)
    inline = len(re.findall(r"(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$(?!\d)", nodisp))
    return dict(md_display_math=display, md_inline_math_est=inline,
                md_headings=len(re.findall(r"^#{1,6} ", md, flags=re.M)),
                md_tables=len(re.findall(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", md, flags=re.M)),
                md_images=len(re.findall(r"!\[[^\]]*\]\(", md)))


def docx_counts(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return dict(docx_oMathPara=x.count("<m:oMathPara>"), docx_oMath_total=len(re.findall(r"<m:oMath>", x)),
                docx_tables=x.count("<w:tbl>"),
                docx_headings=len(re.findall(r'<w:pStyle w:val="Heading[1-6]" ?/>', x)),
                docx_images=x.count("<pic:pic"),
                docx_leftover_dollar_text_runs=len(re.findall(r"<w:t[^>]*>[^<]*\$\$", x)))


def main():
    src, dst, rep = sys.argv[1:4]
    res_path = sys.argv[4] if len(sys.argv) > 4 else "."
    md = open(src, encoding="utf-8").read()
    wrapped = []
    tmp = os.path.join(os.path.dirname(os.path.abspath(dst)), "_render_tmp.md")
    open(tmp, "w", encoding="utf-8").write(wrap_linebreak_blocks(md, wrapped))
    pandoc = pypandoc.get_pandoc_path()
    proc = subprocess.run([pandoc, tmp, "--resource-path", res_path,
                           "-f", "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+grid_tables",
                           "-t", "docx", "-o", dst, "--verbose"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    os.remove(tmp)
    warnings = [l for l in (proc.stderr or "").splitlines() if "WARNING" in l.upper() or "could not" in l.lower()]
    report = dict(pandoc=pypandoc.get_pandoc_version(), returncode=proc.returncode, warnings=warnings,
                  render_wrapped_blocks=wrapped, **md_counts(md), **docx_counts(dst),
                  md_sha256=hashlib.sha256(md.encode("utf-8")).hexdigest(),
                  docx_sha256=hashlib.sha256(open(dst, "rb").read()).hexdigest())
    json.dump(report, open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in report.items()}, indent=1))
    for w in warnings[:15]:
        print("W:", w[:200])


if __name__ == "__main__":
    main()
