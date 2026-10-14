"""Minimal boundary patch v1.8.5 -> v1.8.5a: name the sensitivity-emergent cell as a future-research
candidate in §5.9 (researcher decision 62). Usage: python -I patch_v185a.py <in.md> <out.md>"""
import hashlib, sys
src, dst = sys.argv[1:3]
text = open(src, encoding="utf-8").read()
assert hashlib.sha256(text.encode("utf-8")).hexdigest() == "1812da36c8f045b8d5645a4241f8db138a00fc0b9a77522ac7f3c5c6fed01c35"
OLD = "以檢驗低整合位置是否具有一致的決策編排特徵。\n\n在文獻之外"
NEW = ("以檢驗低整合位置是否具有一致的決策編排特徵。"
       "此外，V1.8.5 稽核標籤替代敏感度分析中新進入穩健集合的「人機增能 × 風險評估」（不足呈現）屬敏感度浮現格"
       "（SENSITIVITY_EMERGENT_DEPLETED_CELL）：它在凍結的主要分析中未通過穩健判定，因此不加入正式的 G01–G16，"
       "也不重新編號 G 清單（附錄 E40）；本研究只把它列為後續研究的候選線索，待在跨分層、全語料一致的標籤下重新檢驗其成員資格後，"
       "再判斷人機增能功能與風險評估決策之間是否存在穩定的低整合。"
       "\n\n在文獻之外")
assert text.count(OLD) == 1
out = text.replace(OLD, NEW)
STATUS_OLD = "合併碩士論文 v1.8.5 COMPUTE CLOSURE CANDIDATE（由 v1.8.3 修訂；"
STATUS_NEW = "合併碩士論文 v1.8.5 COMPUTE CLOSURE CANDIDATE（v1.8.5a：只在第 5.9 節補記敏感度浮現格為後續研究候選線索；由 v1.8.3 修訂；"
assert out.count(STATUS_OLD) == 1
out = out.replace(STATUS_OLD, STATUS_NEW)
open(dst, "w", encoding="utf-8", newline="\n").write(out)
print(hashlib.sha256(out.encode("utf-8")).hexdigest())
