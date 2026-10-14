"""Write a readable dump of exactly what a coder sees in one S1b coder workbook (default CODER_1_ZH_TW.xlsx).

Every non-empty cell of every sheet is reproduced in sheet order, plus sheet names, drop-down lists, validation
messages, fill colour of response cells and document properties. Read-only on the workbook.

Usage: python -E -X utf8 -P dump_coder_preview_s1c.py [--file X.xlsx] [--out PREVIEW.md]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys

from openpyxl import load_workbook

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)


def md(v):
    return str(v).replace("|", "\\|").replace("\n", " ")


def dump(path):
    wb = load_workbook(path)
    with open(path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    p = wb.properties
    L = ["# S1C 編碼者視角預覽（CODER_1_ZH_TW.xlsx）", "",
         "研究者目視審閱用。本檔逐格重現編碼者在 `coder_distribution/" + os.path.basename(path) + "` 中看到的全部內容"
         "（工作表名稱、每個非空白儲存格、下拉選單選項、驗證訊息、文件屬性）。作答欄與聲明欄均為空白。"
         "本檔僅供研究團隊使用，不寄給編碼者。", "",
         f"- 檔案 SHA-256：`{h}`",
         f"- 工作表（依序）：{'、'.join(wb.sheetnames)}",
         f"- 文件屬性：作者＝{p.creator}；最後修改者＝{p.lastModifiedBy}；標題＝{p.title}；"
         f"主旨／關鍵字／描述／類別＝空白", ""]
    for ws in wb.worksheets:
        L += [f"## 工作表：{ws.title}", ""]
        rows = list(ws.iter_rows())
        if ws.title in ("填答說明",):
            for r in rows:
                v = r[0].value
                L.append(f"> {md(v)}" if v is not None else ">")
            L.append("")
        elif ws.title.startswith("作答_") or ws.title == "題目資訊":
            head = [c.value for c in rows[0]]
            L += ["欄位（第 1 列）：", ""] + [f"{j + 1}. {md(x)}" for j, x in enumerate(head)] + [""]
            for r in rows[1:]:
                vals = {head[j]: c.value for j, c in enumerate(r)}
                L += [f"### 第 {vals['題序']} 題　{vals['題目編號']}", ""]
                for k in head[2:]:
                    v = vals.get(k)
                    if v is not None:
                        L.append(f"- **{md(k)}**：{md(v)}")
                    elif k.startswith("Q"):
                        L.append(f"- **{md(k)}**：（空白作答欄，淡黃色）")
                L.append("")
        else:
            for r in rows:
                vals = [c.value for c in r]
                if any(v is not None for v in vals):
                    cells = ["（空白作答欄，淡黃色）" if (v is None and c.fill.fill_type == "solid") else
                             ("" if v is None else md(v)) for c, v in zip(r, vals)]
                    L.append("| " + " | ".join(cells) + " |")
                    if r[0].row == (2 if ws.title == "作答聲明" else 1):
                        L.append("|" + "---|" * len(cells))
            L.append("")
        dvs = ws.data_validations.dataValidation
        if dvs:
            L += ["**此工作表的資料驗證（下拉選單）**", ""]
            for d in dvs:
                if d.type == "list":
                    opts = d.formula1.strip('"').split(",")
                    L.append(f"- 範圍 `{d.sqref}`：下拉選單 = {'／'.join(opts)}；錯誤訊息：{d.errorTitle}－{d.error}")
                else:
                    L.append(f"- 範圍 `{d.sqref}`：文字長度 ≤ {d.formula1}；錯誤訊息：{d.errorTitle}－{d.error}")
            L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(OUT, "coder_distribution", "CODER_1_ZH_TW.xlsx"))
    ap.add_argument("--out", default=os.path.join(OUT, "S1C_CODER_FACING_PREVIEW.md"))
    a = ap.parse_args()
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(dump(a.file))
    print("written", a.out)


if __name__ == "__main__":
    sys.exit(main())
