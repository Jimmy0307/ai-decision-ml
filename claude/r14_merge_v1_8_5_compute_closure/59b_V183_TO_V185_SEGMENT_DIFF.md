# 59b — v1.8.3 → v1.8.5 segment diff (sub-agent U)

Source sha256 `0da8cec1521dbeff900ffa1fa9a1de0a31b0cdfa34b82c03531eba2111d7f740` → output sha256 `1812da36c8f045b8d5645a4241f8db138a00fc0b9a77522ac7f3c5c6fed01c35`. One block per patch, in application order. `old` = exact v1.8.3 text (asserted to occur once); `new` = v1.8.5 text. ⏎ in the inline diff marks an inserted line break.

## U01 — 稿件狀態 (v1.8.3 line 5) — version label

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); Appendix D row U25

```diff
- 合併碩士論文 v1.8.3 V5 PROVENANCE CANDIDATE（由 v1.8.2 修訂；v1.0–v1.8.2 保留、未覆寫；
+ 合併碩士論文 v1.8.5 COMPUTE CLOSURE CANDIDATE（由 v1.8.3 修訂；v1.8.4 為基準重現階段，未另出稿件；v1.0–v1.8.3 保留、未覆寫；
```

Inline: 合併碩士論文 v1.8.[-3 V-]5 {+COM+}P{+UTE CLOSU+}R[-OVENANC-]E CANDIDATE（由 v1.8.[-2-]{+3+} 修訂{+；v1.8.4 為基準重現階段，未另出稿件+}；v1.0–v1.8.[-2-]{+3+} 保留、未覆寫；

## U02 — 稿件狀態 (v1.8.3 line 5) — scope sentence (no new analysis -> one labelled sensitivity analysis)

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 本版不新增任何分析，也不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；
+ 本版不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；除 v1.8.5 新增並明確標示為敏感度分析的稽核標籤替代結果外，不新增任何分析；
```

Inline: 本版[-不新增任何分析，也-]不改變任何方程、模型元素、R14 數值或 G01–G16 凍結值；{+除 v1.8.5 新增並明確標示為敏感度分析的稽核標籤替代結果外，不新增任何分析；+}

## U03 — 稿件狀態 (v1.8.3 line 5) — v1.8.5 compute-closure summary

Source: OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 43 §1–§5; OUT 44; OUT 45; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 只強化其來源（V1.8.3 檔案 39–40）。(1)
+ 只強化其來源（V1.8.3 檔案 39–40）。v1.8.5 只更新計算驗證的狀態並新增一項敏感度結果，不改變任何主要分析數值、G 清單、G→M 對應、V1 設計或企業模型：V5 來源已確認；以僅修改路徑的程式複本重跑 V5 第 10–13 階段，13 個雜湊釘定的正式輸出 13/13 逐位元組相同（基準模式下所有閘門常數未改；V1.8.5 檔案 46–50）；研究者核准的有界稽核標籤替代規則（BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1）已於執行前以雜湊事先登記（V1.8.5 檔案 43–45），並據以完成稽核標籤替代敏感度分析（V1.8.5 檔案 51–58；第 3.7.4、4.5.5 節）；主要分析維持預先凍結之 V5/R14 基準（PRIMARY_BASELINE_REPLACED = NO）。COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY；CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED（人工標籤只涵蓋 50 筆目標稽核記錄）。(1)
```

Inline: 只強化其來源（V1.8.3 檔案 39–40）。{+v1.8.5 只更新計算驗證的狀態並新增一項敏感度結果，不改變任何主要分析數值、G 清單、G→M 對應、V1 設計或企業模型：V5 來源已確認；以僅修改路徑的程式複本重跑 V5 第 10–13 階段，13 個雜湊釘定的正式輸出 13/13 逐位元組相同（基準模式下所有閘門常數未改；V1.8.5 檔案 46–50）；研究者核准的有界稽核標籤替代規則（BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1）已於執行前以雜湊事先登記（V1.8.5 檔案 43–45），並據以完成稽核標籤替代敏感度分析（V1.8.5 檔案 51–58；第 3.7.4、4.5.5 節）；主要分析維持預先凍結之 V5/R14 基準（PRIMARY_BASELINE_REPLACED = NO）。COMPUTATIONAL_VALIDATION_STATUS = CLOSED_WITH_BOUNDED_HUMAN_VALIDITY；CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED（人工標籤只涵蓋 50 筆目標稽核記錄）。+}(1)

## U04 — 稿件狀態 (v1.8.3 line 5) — full-reanalysis status -> executed as sensitivity analysis

Source: OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 此替換只重算 50 筆受稽核記錄的標籤（局部附屬重算，不是完整重分析）；V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）在方法上列為開放的驗證行動（REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION），其執行條件尚待滿足（EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION：37 項受保護輸入已全數以完整 SHA-256 確認，但須先由研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本重現 13 個雜湊釘定的正式輸出，並依 V9 經研究者核准），在 V1 人類構念效度驗證之前不建議優先執行（NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）；
+ V9 側車的此項替換只重算 50 筆受稽核記錄的標籤（局部附屬重算）；V9 套件標記的完整重分析（FULL_REANALYSIS_REQUIRED）已於 V1.8.5 經研究者核准，以稽核標籤替代敏感度分析執行：主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性（FULL_REANALYSIS_METHOD_STATUS = SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS；FULL_REANALYSIS_EXECUTED = YES（AUDITED_LABEL_SENSITIVITY_ANALYSIS）；PRIMARY_BASELINE_REPLACED = NO）；敏感度分析的結果與 V9 側車結果完全一致，G01–G16 移除 0 組、方向改變 0 組（第 4.5.5 節；附錄 E40）；
```

Inline: {+V9 側車的+}此{+項+}替換只重算 50 筆受稽核記錄的標籤（局部附屬重算[-，不是完整重分析-]）；V9 套件標記的完整重分析（FU…ANALYSIS_REQUIRED）[-在方法上列為開放-]{+已於 V1.8.5 經研究者核准，以稽核標籤替代敏感度分析執行：主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂+}的[-驗證行動-]{+敏感性+}（{+FULL_+}RE[-Q-]{+ANALYSIS_METHOD_STAT+}U{+S = SAT+}I[-R-]{+SFI+}ED[-_BY_V9-]_AS_[-OP-]{+AUDITED_LABEL_S+}EN{+SITIVITY+}_[-V-]{+AN+}AL{+YS+}I[-D-]{+S；FULL_RE+}A[-T-]{+NALYS+}I[-ON-]{+S+}_[-ACTION），其執行條件尚待滿足（-]EXECUT{+ED = YES（AUDITED_L+}AB{+E+}L[-E-]_[-P-]{+S+}EN[-D-]{+S+}I[-NG_PROPAGA-]TI[-ON_RULE-]{+VITY+}_AN[-D-]{+ALYSIS）；PRIMARY+}_BASELINE_REP[-R-]{+LACED = N+}O[-DUCTION：37 項受保護輸入已全數以完整 SHA-256 確認，但須先由研究者事先登記並以雜湊承諾標籤傳播規則、在新-]{+）；敏感度分析+}的[-日期目錄中以僅修改路徑的程式複本重現 13 個雜湊釘定的正式輸出，並依-]{+結果與+} V9 [-經研究者核准）-]{+側車結果完全一致+}，[-在-]{+G01–G16+} [-V1-]{+移除+} [-人類構念效度驗證之前不建議優先執行-]{+0 組、方向改變 0 組+}（[-NOT_RECOMMENDED）-]{+第 4.5.5 節+}；[-日後是否重跑仍由研究者決定（-]附錄 E40）；

## U05 — 摘要 (v1.8.3 line 13) — full-reanalysis status -> executed as sensitivity analysis

Source: OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4

```diff
- ；此替換只重算 50 筆受稽核記錄的標籤，屬局部敏感度，不是完整重分析，也不表示人工稽核確認了 32 組的成員；凍結的 32 組仍為正式推論基準；完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定。
+ ；此替換只重算 50 筆受稽核記錄的標籤，屬局部敏感度，也不表示人工稽核確認了 32 組的成員；凍結的 32 組仍為正式推論基準。完整重分析其後以稽核標籤替代敏感度分析執行：主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性（20 筆採調和後最終標籤、30 筆採第一位編碼者標籤，其餘記錄維持模型標籤；規則於執行前以雜湊登記，且正式基準先經 13/13 逐位元組重現）。在此敏感度分析中，穩健集合仍為 32 格（15 過度、17 不足），成員變動與上述局部替換完全相同，G01–G16 無一移除、無方向改變；此分析只涉及 50 筆目標稽核記錄，不建立全語料的人類效度。
```

Inline: ；此替換只重算 50 筆受稽核記錄的標籤，屬局部敏感度[-，不是完整重分析-]，也不表示人工稽核確認了 32 組的成員；凍結的 32 組仍為正式推論基準[-；-]{+。+}完整重分析[-列為開放-]{+其後以稽核標籤替代敏感度分析執行：主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂+}的[-驗證行動-]{+敏感性（20 筆採調和後最終標籤、30 筆採第一位編碼者標籤+}，其{+餘記錄維持模型標籤；規則於+}執行[-條件尚待滿足（須先事先-]{+前以雜湊+}登記[-標籤傳播規則並重現-]{+，且+}正式基準{+先經 13/13 逐位元組重現）。在此敏感度分析中，穩健集合仍為 32 格（15 過度、17 不足+}），[-在-]{+成員變動與上述局部替換完全相同，G01–G16+} [-V1-]{+無一移除、無方向改變；此分析只涉及+} {+50 筆目標稽核記錄，不建立全語料的+}人類[-構念-]效度[-驗證之前不建議優先執行，日後是否重跑仍由研究者決定-]。

## U06 — Abstract (v1.8.3 line 29) — full-reanalysis status -> executed as sensitivity analysis (English)

Source: OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4

```diff
- This substitution relabelled only the 50 audited records; it is a local sensitivity check, not a full reanalysis, and it does not show that human validation confirmed the 32-pairing membership. The frozen 32-pairing core remains the official inferential baseline, and the full reanalysis flagged by the validation package remains an open validation action: its execution is pending researcher predeclaration and hash commitment of the label-propagation rule, byte-for-byte reproduction of the pinned official baseline in the current workspace, and researcher approval (all 37 protected inputs are now hash-confirmed), it is not recommended as a priority before the V1 human construct validation, and whether to rerun it later remains a researcher decision.
+ This substitution relabelled only the 50 audited records and does not show that human validation confirmed the 32-pairing membership. The frozen 32-pairing core remains the primary analysis and the official inferential baseline. The full reanalysis flagged by the validation package was subsequently executed as an audited-label sensitivity analysis: the primary analysis keeps the prefrozen V5/R14 baseline, while a researcher-approved, hash-preregistered bounded substitution of the 50 targeted human audit labels (20 reconciled final labels and 30 first-coder labels; all other records keep their model labels) was followed by a complete rerun of all label-dependent analyses, after the pinned official baseline had been reproduced byte for byte (13 of 13 outputs). In this sensitivity analysis the robust set again comprised 32 pairings (15 enrichments and 17 depletions), with exactly the same membership change as the local substitution, and none of G01–G16 was removed or changed direction. Because it covers only 50 targeted records, it does not establish corpus-wide human validity.
```

Inline: This substitution …50 audited records[-; it is a local sensitivity check, not a full reanalysis,-] and[- it-] does not show tha… core remains the {+primary analysis and the +}official inferential baseline[-,-]{+.+} [-and t-]{+T+}he full reanalysis…alidation package [-rem-]{+w+}a[-in-]s [-an op-]{+subsequ+}en[- va-]{+t+}l[-idation action: its-]{+y+} execut[-io-]{+ed as a+}n {+audited-label sensitivity analysis: the primary analys+}is {+kee+}p{+s the prefroz+}en[-d-]{+ V5/R14 basel+}in[-g-]{+e, while a+} researcher[- -]{+-ap+}pr{+ov+}ed[-eclaration and-]{+,+} hash{+-preregistered+} [-c-]{+b+}o[-mm-]{+unded subst+}it[-me-]{+utio+}n[-t-] of the {+50 targeted human audit labels (20 reconciled final labels and 30 first-coder labels; all other records keep their model labels) was followed by a complete rerun of all +}label-{+de+}p[-rop-]{+endent +}a[-g-]{+n+}a[-tion ru-]l{+ys+}e{+s+}, [-by-]{+af+}te[--fo-]r[--byte reproduction of-] the pinned official baseline {+had been reproduced byte for byte (13 of 13 outputs). In th+}i{+s se+}n{+sitivity analysis+} the {+robust set again +}c[-u-]{+omp+}r{+ised 32 pai+}r{+ings (15 enrichm+}ent[- work-]s[-pace,-] and [-researcher approval (all 3-]{+1+}7 {+de+}p[-ro-]{+le+}t[-ected -]i[-nputs are now hash-c-]on[-firmed-]{+s+}), {+w+}it{+h+} [-is no-]{+exac+}t[- recommended as a priorit-]{+l+}y[- before-] the [-V1-]{+same+} {+members+}h[-um-]{+ip ch+}an{+ge+} {+as the lo+}c[-on-]{+al sub+}st[-r-]{+it+}u[-ct valida-]tion, and {+none of G01–G16 +}w[-hether to-]{+as+} re{+moved o+}r{+ changed direction. Beca+}u[-n-]{+se+} it {+covers on+}l{+y 50 t+}a{+rge+}te[-r-]{+d+} re{+cords, it does not establish corpus-wide hu+}ma{+n val+}i[-ns a researcher -]d[-ec-]i[-sion-]{+ty+}.

## U07 — 1.4 (v1.8.3 line 122) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55

```diff
- 完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）。研究問題三
+ 完整重分析已於 V1.8.5 以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的人類效度（第 4.5.5 節；附錄 E40）。研究問題三
```

Inline: 完整重分析[-列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在-]{+已於+} V1{+.8.5+} {+以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的+}人類[-構念-]效度[-驗證之前不建議優先執行，日後是否重跑仍由研究者決定-]（第 4.5.5 節；附錄 E40）。研究問題三

## U08 — 1.4 表 (v1.8.3 line 147) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 58 §1–§4

```diff
- 人工標籤替換：局部成員變動；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），V1 前不建議優先執行（附錄 E40） |
+ 人工標籤替換：局部成員變動；完整重分析已以稽核標籤替代敏感度分析執行（V1.8.5；結果相同；不取代主要分析；附錄 E40） |
```

Inline: 人工標籤替換：局部成員變動；完整重分析[-為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），V1 前不建議優先-]{+已以稽核標籤替代敏感度分析+}執行（{+V1.8.5；結果相同；不取代主要分析；+}附錄 E40） |

## U09 — 1.5 (v1.8.3 line 158) — full-reanalysis status

Source: OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 此替換只重算受稽核記錄的標籤，完整重分析是否執行仍待研究者決定（第 4.5.5 節）
+ 此替換只重算受稽核記錄的標籤；V1.8.5 另依事先登記的有界規則完整重跑所有標籤相依分析（稽核標籤替代敏感度分析），結果與此完全一致，主要分析仍維持凍結基準（第 4.5.5 節）
```

Inline: 此替換只重算受稽核記錄的標籤[-，-]{+；V1.8.5 另依事先登記的有界規則+}完整重{+跑所有標籤相依+}分析[-是否執行-]{+（稽核標籤替代敏感度分析），結果與此完全一致，主要分析+}仍[-待研究者決定-]{+維持凍結基準+}（第 4.5.5 節）

## U10 — 1.5 (v1.8.3 line 158) — full-reanalysis status (source note)

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 完整重分析的現行狀態（開放驗證行動、執行條件待滿足、V1 前不建議優先執行）見附錄 E40
+ 完整重分析的現行狀態（已以稽核標籤替代敏感度分析執行；不取代主要分析；不建立全語料的人類效度）見附錄 E40
```

Inline: 完整重分析的現行狀態（[-開放驗證行動、-]{+已以稽核標籤替代敏感度分析+}執行[-條件待滿足、V1 前-]{+；不取代主要分析；+}不建[-議優先執行-]{+立全語料的人類效度+}）見附錄 E40

## U11 — 1.6 (v1.8.3 line 168) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55

```diff
- 完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 4.5.5 節；附錄 E40）；逐格解讀
+ 完整重分析已於 V1.8.5 以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的人類效度（第 4.5.5 節；附錄 E40）；逐格解讀
```

Inline: 完整重分析[-列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在-]{+已於+} V1{+.8.5+} {+以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的+}人類[-構念-]效度[-驗證之前不建議優先執行，日後是否重跑仍由研究者決定-]（第 4.5.5 節；附錄 E40）；逐格解讀

## U12 — 3.1.1 (v1.8.3 line 405) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 55

```diff
- 完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（第 3.7.4、4.5.5 節；附錄 E40）。第二層
+ 完整重分析已於 V1.8.5 以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的人類效度（第 3.7.4、4.5.5 節；附錄 E40）。第二層
```

Inline: 完整重分析[-列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準），在-]{+已於+} V1{+.8.5+} {+以稽核標籤替代敏感度分析執行（主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析），敏感度分析中穩健集合的格數不變、G01–G16 無一移除，但此結果不建立全語料的+}人類[-構念-]效度[-驗證之前不建議優先執行，日後是否重跑仍由研究者決定-]（第 3.7.4、4.5.5 節；附錄 E40）。第二層

## U13 — 3.1.1 流程 (v1.8.3 line 412) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line); OUT 58 §1–§4

```diff
- 完整重分析為開放驗證行動，執行條件待滿足）
+ 完整重分析已以稽核標籤替代敏感度分析執行，結果相同）
```

Inline: 完整重分析[-為開放驗證行動，-]{+已以稽核標籤替代敏感度分析+}執行[-條件待滿足-]{+，結果相同+}）

## U14 — 3.7.4 (v1.8.3 line 605) — propagation rule preregistered + V1.8.5 procedure (new paragraph)

Source: OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; REVISED_GUARD_POLICY; REVISED_GUARD_SELF_AUDIT; REVISED_GUARD_DIFF.csv; OUT 49b; OUT 57

```diff
- 此規則屬事後尋回，不是事前登記，若執行完整重分析，仍須由研究者事先登記並以雜湊承諾 `[AUTHOR TO CONFIRM：是否採用尋回的傳播規則並事先登記；附錄 E48]`。
+ 此規則屬事後尋回；研究者其後核准採用，並在任何重跑之前以 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 之名逐欄登記、以雜湊承諾（V1.8.5 檔案 43–45；附錄 E48）。
+ 
+ V1.8.5 依此登記的規則執行稽核標籤替代敏感度分析。主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。規則的內容為：20 筆調和記錄採調和後的最終標籤，其餘 30 筆目標稽核記錄採第一位編碼者標籤，其他所有記錄維持原模型標籤；優先順序為調和後最終標籤 > 第一位編碼者標籤 > 原模型標籤，只有以記錄代碼明確對應到人工稽核的記錄才能覆寫模型標籤；不推論其他記錄的修正、不外推錯誤率、不做全語料或分類架構層級的調整，也不做機率式修正、插補或規則式重標。執行前有兩道前置條件：第一，以僅修改路徑的程式複本重跑 V5 第 10–13 階段，13 個雜湊釘定的正式輸出 13/13 逐位元組相同，基準模式下所有雜湊、筆數、種子與重複次數的閘門常數皆未改（V1.8.5 檔案 46–50）；第二，替代規則、50 筆記錄清單與套用程式皆於執行前以雜湊登記（V1.8.5 檔案 43–45）。替代後的重跑採雙模式閘門政策：結構不變量（10 × 12 分類、120 格、種子與重複次數、統計方法）維持原樣，違反即中止；只有階段間的承接閘門（上游雜湊與承接筆數）依前一階段的實際輸出重新釘定，且須與不匯入管線程式的獨立重算一致；待觀察的科學結果（例如穩健集合的格數）只記錄，從不作為中止常數（V1.8.5 REVISED_GUARD_POLICY、REVISED_GUARD_SELF_AUDIT）。另一個不匯入管線程式的獨立驗證程式由輸出檔重算計數、精確檢定、BH 校正與穩健判定，全部通過（V1.8.5 檔案 57）。結果見第 4.5.5 節。
```

Inline: 此規則屬事後尋回[-，不是事前登記，若執行完整重分析，仍須由-]{+；+}研究者[-事先-]{+其後核准採用，並在任何重跑之前以 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 之名逐欄+}登記[-並-]{+、+}以雜湊承諾{+（V1.8.5+} [-`[AUTHOR-]{+檔案+} [-TO CONFIRM：是否採用尋回的傳播規則並事先登記-]{+43–45+}；附錄 E48[-]`-]{+）+}。{+⏎⏎V1.8.5 依此登記的規則執行稽核標籤替代敏感度分析。主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。規則的內容為：20 筆調和記錄採調和後的最終標籤，其餘 30 筆目標稽核記錄採第一位編碼者標籤，其他所有記錄維持原模型標籤；優先順序為調和後最終標籤 > 第一位編碼者標籤 > 原模型標籤，只有以記錄代碼明確對應到人工稽核的記錄才能覆寫模型標籤；不推論其他記錄的修正、不外推錯誤率、不做全語料或分類架構層級的調整，也不做機率式修正、插補或規則式重標。執行前有兩道前置條件：第一，以僅修改路徑的程式複本重跑 V5 第 10–13 階段，13 個雜湊釘定的正式輸出 13/13 逐位元組相同，基準模式下所有雜湊、筆數、種子與重複次數的閘門常數皆未改（V1.8.5 檔案 46–50）；第二，替代規則、50 筆記錄清單與套用程式皆於執行前以雜湊登記（V1.8.5 檔案 43–45）。替代後的重跑採雙模式閘門政策：結構不變量（10 × 12 分類、120 格、種子與重複次數、統計方法）維持原樣，違反即中止；只有階段間的承接閘門（上游雜湊與承接筆數）依前一階段的實際輸出重新釘定，且須與不匯入管線程式的獨立重算一致；待觀察的科學結果（例如穩健集合的格數）只記錄，從不作為中止常數（V1.8.5 REVISED_GUARD_POLICY、REVISED_GUARD_SELF_AUDIT）。另一個不匯入管線程式的獨立驗證程式由輸出檔重算計數、精確檢定、BH 校正與穩健判定，全部通過（V1.8.5 檔案 57）。結果見第 4.5.5 節。+}

## U15 — 3.7.4 (v1.8.3 line 609) — full-reanalysis status + corpus-wide limitation

Source: OUT 43 §1–§5; OUT 44; OUT 45; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 依該檔，完整重分析須經研究者核准；其現行狀態為：方法上列為 V9 的開放驗證行動，其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認；須先事先登記標籤傳播規則並重現正式基準），在 V1 人類構念效度驗證之前不建議優先執行，日後是否重跑仍由研究者決定（附錄 E40）。替換結果不表示人工稽核確認了 32 組的成員。
+ 依該檔，完整重分析須經研究者核准；研究者已核准，並於 V1.8.5 以稽核標籤替代敏感度分析執行（FULL_REANALYSIS_EXECUTED = YES，屬 AUDITED_LABEL_SENSITIVITY_ANALYSIS；PRIMARY_BASELINE_REPLACED = NO；附錄 E40）。替換結果與此敏感度分析都不表示人工稽核確認了 32 組的成員；人工標籤只涵蓋 50 筆目標稽核記錄，全語料的人類效度未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）。
```

Inline: 依該檔，完整重分析須經研究者核准；[-其現行狀態為：方法上列為 V9 的開放驗證行動-]{+研究者已核准+}，[-其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認；須先事先登記標籤傳播規則-]並[-重現正式基準），在-]{+於+} V1{+.8.5+} [-人類構念效-]{+以稽核標籤替代敏感+}度[-驗證之前不建議優先-]{+分析+}執行{+（FULL_REANALYSIS_EXECUTED = YES+}，[-日後是否重跑仍由研究者決定（-]{+屬 AUDITED_LABEL_SENSITIVITY_ANALYSIS；PRIMARY_BASELINE_REPLACED = NO；+}附錄 E40）。替換結果{+與此敏感度分析都+}不表示人工稽核確認了 32 組的成員{+；人工標籤只涵蓋 50 筆目標稽核記錄，全語料的人類效度未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）+}。

## U16 — 3.8.1 (v1.8.3 line 619) — L2' provenance

Source: OUT 58 §1–§4

```diff
- L2′ 取自 V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv（已逐列核對；屬局部附屬重算，不是完整重分析）。
+ L2′ 取自 V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv（已逐列核對；屬局部附屬重算），並經 V1.8.5 稽核標籤替代敏感度分析以完整重跑重現，結果完全一致（第 4.5.5 節）。
```

Inline: L2′ 取自 V9 套件 ROBUS….csv（已逐列核對；屬局部附屬重算{+）+}，[-不是-]{+並經 V1.8.5 稽核標籤替代敏感度分析以+}完整重[-分析-]{+跑重現，結果完全一致（第 4.5.5 節+}）。

## U17 — 3.8.1 表 (v1.8.3 line 630) — L2' role column

Source: OUT 53 (table + gained/lost + flips); OUT 58 §1–§4

```diff
- 局部成員敏感度；不取代 L2；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），V1 前不建議優先執行（附錄 E40）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕 |
+ 局部成員敏感度；不取代 L2；V1.8.5 以稽核標籤替代敏感度分析完整重跑，結果完全一致（表 4-9B；附錄 E40）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對；V1.8.5 檔案 53、58〕 |
```

Inline: 局部成員敏感度；不取代 L2；{+V1.8.5 以稽核標籤替代敏感度分析+}完整重[-分析為開放驗證行動-]{+跑+}，[-執行條件待滿足-]{+結果完全一致+}（[-須先登記傳播規則並重現基準），V1-]{+表+} [-前不建議優先執行（-]{+4-9B；+}附錄 E40）〔V9 套件 ROBU…SITIVITY.csv，已逐列核對{+；V1.8.5 檔案 53、58+}〕 |

## U18 — 3.8.2 規則 6 (v1.8.3 line 645) — handoff rule 6 (G list unchanged)

Source: OUT 55

```diff
- 在完整重分析完成前，交接清單維持凍結的 G01–G16，不增列這一組（附錄 E40）
+ V1.8.5 的稽核標籤替代敏感度分析得到相同結果（G01–G16 移除 0 組、方向改變 0 組）。由於此分析不取代主要分析，交接清單維持凍結的 G01–G16，不增列這一組；是否增列屬另一項研究者治理決定，不在本稿範圍（附錄 E40）
```

Inline: [-在完整重-]{+V1.8.5 的稽核標籤替代敏感度+}分析[-完成前-]{+得到相同結果（G01–G16 移除 0 組、方向改變 0 組）。由於此分析不取代主要分析+}，交接清單維持凍結的 G01–G16，不增列這一組{+；是否增列屬另一項研究者治理決定，不在本稿範圍+}（附錄 E40）

## U19 — 3.8.3 (v1.8.3 line 653) — baseline reproduction

Source: OUT 47 §2–§5; OUT 48; OUT 49; OUT 50

```diff
- 執行時間、服務呼叫量等屬工程效能紀錄，不作為本研究的分析再現性判定。
+ 執行時間、服務呼叫量等屬工程效能紀錄，不作為本研究的分析再現性判定。主要分析的第 10–13 階段已於 V1.8.5 以僅修改路徑的程式複本重跑，沿用原種子與重複次數，13 個雜湊釘定的正式輸出 13/13 逐位元組相同（V1.8.5 檔案 46–50）。
```

Inline: 執行時間、服務呼叫量等屬工程效能紀錄，不作為本研究的分析再現性判定。{+主要分析的第 10–13 階段已於 V1.8.5 以僅修改路徑的程式複本重跑，沿用原種子與重複次數，13 個雜湊釘定的正式輸出 13/13 逐位元組相同（V1.8.5 檔案 46–50）。+}

## U20 — 第四章引言 (v1.8.3 line 1374) — chapter scope

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 第 4.1–4.6 節報告文獻分析的凍結主要結果與人工稽核的局部敏感度；
+ 第 4.1–4.6 節報告文獻分析的凍結主要結果與人工稽核的局部敏感度（含 V1.8.5 稽核標籤替代敏感度分析，第 4.5.5 節）；
```

Inline: 第 4.1–4.6 節報告文獻分析的凍結主要結果與人工稽核的局部敏感度{+（含 V1.8.5 稽核標籤替代敏感度分析，第 4.5.5 節）+}；

## U21 — 4.5.5 (v1.8.3 line 1629) — full-reanalysis status

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 其現行狀態為：方法上列為 V9 的開放驗證行動（FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION）；其執行條件尚待滿足（37 項受保護輸入已全數以完整 SHA-256 確認，但須先事先登記標籤傳播規則並重現正式基準，且經研究者核准；FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION）；在 V1 人類構念效度驗證之前不建議優先執行（FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED）；日後是否重跑仍由研究者決定（附錄 E40）。本節的替換只重算受稽核記錄的標籤，其餘記錄維持模型標籤，屬局部附屬重算，不是完整重分析。
+ 研究者其後核准，完整重分析已於 V1.8.5 以稽核標籤替代敏感度分析執行（FULL_REANALYSIS_METHOD_STATUS = SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS；FULL_REANALYSIS_EXECUTED = YES（AUDITED_LABEL_SENSITIVITY_ANALYSIS）；PRIMARY_BASELINE_REPLACED = NO；附錄 E40），結果見本節後半與表 4-9B。表 4-9A 的 V9 替換只重算受稽核記錄的標籤，其餘記錄維持模型標籤，屬局部附屬重算。
```

Inline: {+研究者+}其[-現行狀態為：方法上列為-]{+後核准，完整重分析已於+} V[-9-]{+1.8.5+} [-的開放驗證-]{+以稽核標籤替代敏感度分析執+}行[-動-]（FULL_REANALYSIS_METHOD_STATUS = [-REQU-]{+SAT+}I[-R-]{+SFI+}ED[-_BY_V9-]_AS_[-OP-]{+AUDITED_LABEL_S+}EN{+SITIVITY+}_[-V-]{+AN+}AL{+YS+}I[-DATION_ACTION）；其執行條件尚待滿足（37 項受保護輸入已全數以完整 -]S[-HA-256 確認，但須先事先登記標籤傳播規則並重現正式基準，且經研究者核准-]；FULL_REANALYSIS_EXECUT[-ION_STATUS-]{+ED+} = {+Y+}E[-X-]{+S（AUDIT+}E[-CUT-]{+D_L+}AB{+E+}L[-E-]_[-P-]{+S+}EN[-D-]{+S+}I[-NG_PROPAGA-]TI[-ON_RULE-]{+VITY+}_AN[-D-]{+ALYSIS）；PRIMARY+}_BASELINE_REP[-RO-]{+LACE+}D[-UCTION）；在 V1 人類構念效度驗證之前不建議優先執行（FULL_REANALYSIS_PRIORITY_BEFORE_V1-] = NO[-T_RECOMMENDED）-]；[-日後是否重跑仍由研究者決定（-]附錄 E40）[-。-]{+，結果見+}本節{+後半與表 4-9B。表 4-9A +}的{+ V9 +}替換只重算受稽核記錄的標籤，其餘記錄維持模型標籤，屬局部附屬重算[-，不是完整重分析-]。

## U22 — 4.5.5 表註 (v1.8.3 line 1638) — handoff note

Source: OUT 55

```diff
- 新增的不足呈現不屬於 G01–G16，在完整重分析前不納入交接（第 3.8.2 節規則 6）。
+ 新增的不足呈現不屬於 G01–G16，不納入交接（第 3.8.2 節規則 6）。
```

Inline: 新增的不足呈現不屬於 G01–G16，[-在完整重分析前-]不納入交接（第 3.8.2 節規則 6）。

## U23 — 4.5.5 (v1.8.3 line 1640) — pointer to V1.8.5 values

Source: OUT 53 (table + gained/lost + flips)

```diff
- V9 敏感度表顯示兩格的成員變動都是該零模型在 .05 判定門檻上的跨越，本稿不另引入其數值。
+ V9 敏感度表顯示兩格的成員變動都是該零模型在 .05 判定門檻上的跨越；其數值見下方的 V1.8.5 稽核標籤替代敏感度分析，並與主要分析的數值分開陳述。
```

Inline: V9 敏感度表顯示兩格的成員變動都是該零模型在 .05 判定門檻上的跨越[-，本稿不另引入-]{+；+}其數值{+見下方的 V1.8.5 稽核標籤替代敏感度分析，並與主要分析的數值分開陳述+}。

## U24 — 4.5.5 (v1.8.3 line 1640) — interpretation sentence + NEW sensitivity block and Table 4-9B

Source: OUT 53 (table + gained/lost + flips); OUT 54; OUT 55; OUT 57; OUT 58 §1–§4; OUT 52; OUT 44; OUT 51; OUT 47

```diff
- 第三，這個結果不構成對 32 組配對的人工驗證：目標式稽核只涵蓋穩健核心相關分層的受稽核記錄，且替換改變了成員。在以一致的標籤完成完整重分析之前，逐格解讀對這兩個配對採最保守的語氣。
+ 第三，這個結果不構成對 32 組配對的人工驗證：目標式稽核只涵蓋穩健核心相關分層的受稽核記錄，且替換改變了成員。由於全語料的人類效度尚未建立，逐格解讀對這兩個配對採最保守的語氣。
+ 
+ **V1.8.5 稽核標籤替代敏感度分析。** 主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。規則與執行程序見第 3.7.4 節。替代規則套用於 50 筆目標記錄（50 筆皆以記錄代碼唯一對應，未授權的覆寫 0 筆），其中 37 筆的管線欄位實際改變（V1.8.5 檔案 44、51）。表 4-9B 將主要分析與敏感度分析的數值分欄並列：兩欄是兩組不同的結果，不合併為單一集合；敏感度欄不回寫第 4.4 節或表 4-10 的任何數值。
+ 
+ **表 4-9B：主要分析（凍結基準）與稽核標籤替代敏感度分析的比較**
+ 
+ | 項目 | 主要分析（預先凍結之 V5/R14 基準；正式推論基準） | 稽核標籤替代敏感度分析（V1.8.5；不取代主要分析） |
+ |---|---|---|
+ | 嚴格分析記錄 | 6,499 | 6,499 |
+ | 兩端皆完成分類的記錄 | 3,125 | 3,107 |
+ | 涵蓋文獻數 | 783 | 781 |
+ | 文獻層級邊 | 2,180 | 2,181 |
+ | 主要固定度數零模型 p_BH ≤ .05 | 47 | 47 |
+ | 精確超幾何檢定 p_BH ≤ .05 | 46 | 47 |
+ | 文獻內部結構保持零模型 p_BH ≤ .05 | 32 | 32 |
+ | 未去重分析 p_BH ≤ .05 | 54 | 55 |
+ | 穩健集合（過度／不足） | 32（16／16） | 32（15／17） |
+ | 穩健集合中的 G01–G16（皆為不足呈現） | 16／16 | 16／16（移除 0、方向改變 0） |
+ 
+ 表註：主要分析欄為 V5 正式輸出的凍結值（第 4.1–4.4 節），V1.8.5 以僅修改路徑的程式複本重現，13/13 逐位元組相同（V1.8.5 檔案 47）。敏感度分析欄取自 V1.8.5 檔案 53 與 55，並由獨立驗證程式重算（檔案 57）；兩欄使用相同的統計程序、種子與重複次數（主要零模型 10,000 次、文獻內部結構保持零模型 5,000 次）。
+ 
+ 在 120 格層次，敏感度分析使 24 格的主要（去重）觀察次數與 28 格的未去重計數改變；主要零模型的方向改變 3 格（評估與審核 × 資訊統整、生成與合成 × 配置與規劃、推薦與最佳化 × 執行與協調），三格皆不在穩健集合內（V1.8.5 檔案 52–53）。穩健集合的 31 組成員與方向皆不變；新增人機增能 × 風險評估（不足呈現；文獻內部結構保持零模型 p_BH 由主要分析的 .0567 變為敏感度分析的 .0325，該格觀察次數 1 未變），移出協調與執行 × 一般決策流程（過度呈現；同一 p_BH 由 .0434 變為 .0610，觀察次數 19 未變）；共有成員沒有方向改變（V1.8.5 檔案 53、54）。這與表 4-9A 的 V9 側車結果完全一致：120 格 × 4 種分析的觀察次數、方向與 p_BH 皆相同（最大絕對差 0），替代後的穩健集合檔雜湊亦相同（V1.8.5 檔案 58）。因此，先前只由側車執行的局部替換結果，已由完整管線在事先登記的規則下重現；作為敏感度證據，本節以此完整重跑取代先前的側車結果，但兩者都不取代主要分析。
+ 
+ G01–G16 在敏感度分析中全部留在穩健集合且皆為不足呈現（移除 0 組、方向改變 0 組；STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS；V1.8.5 檔案 55）。在敏感度分析中最接近 .05 判定門檻的是 G07（文獻內部結構保持零模型 p_BH = .0405）、G14（.0298）與 G16（.0223）；這些數值只屬敏感度分析，不取代表 4-4 與表 4-10 的凍結值。
+ 
+ 此敏感度分析的範圍有明確界限。人工標籤只涵蓋 50 筆目標稽核記錄，且集中於穩健核心相關分層，其餘記錄全部維持模型標籤；因此它回答的是「這 50 筆經人工判定的標籤修訂是否改變結論」，不回答全語料以人工標準重新編碼後的結果，也不改變第 4.5.1 節所報告的編碼者間低度一致。全語料的人類效度仍未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）。
```

Inline: 第三，這個結果不構成對 32 組配對…分層的受稽核記錄，且替換改變了成員。[-在以一致-]{+由於全語料+}的[-標籤完成完整重分析之前-]{+人類效度尚未建立+}，逐格解讀對這兩個配對採最保守的語氣。{+⏎⏎**V1.8.5 稽核標籤替代敏感度分析。** 主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。規則與執行程序見第 3.7.4 節。替代規則套用於 50 筆目標記錄（50 筆皆以記錄代碼唯一對應，未授權的覆寫 0 筆），其中 37 筆的管線欄位實際改變（V1.8.5 檔案 44、51）。表 4-9B 將主要分析與敏感度分析的數值分欄並列：兩欄是兩組不同的結果，不合併為單一集合；敏感度欄不回寫第 4.4 節或表 4-10 的任何數值。⏎⏎**表 4-9B：主要分析（凍結基準）與稽核標籤替代敏感度分析的比較**⏎⏎| 項目 | 主要分析（預先凍結之 V5/R14 基準；正式推論基準） | 稽核標籤替代敏感度分析（V1.8.5；不取代主要分析） |⏎|---|---|---|⏎| 嚴格分析記錄 | 6,499 | 6,499 |⏎| 兩端皆完成分類的記錄 | 3,125 | 3,107 |⏎| 涵蓋文獻數 | 783 | 781 |⏎| 文獻層級邊 | 2,180 | 2,181 |⏎| 主要固定度數零模型 p_BH ≤ .05 | 47 | 47 |⏎| 精確超幾何檢定 p_BH ≤ .05 | 46 | 47 |⏎| 文獻內部結構保持零模型 p_BH ≤ .05 | 32 | 32 |⏎| 未去重分析 p_BH ≤ .05 | 54 | 55 |⏎| 穩健集合（過度／不足） | 32（16／16） | 32（15／17） |⏎| 穩健集合中的 G01–G16（皆為不足呈現） | 16／16 | 16／16（移除 0、方向改變 0） |⏎⏎表註：主要分析欄為 V5 正式輸出的凍結值（第 4.1–4.4 節），V1.8.5 以僅修改路徑的程式複本重現，13/13 逐位元組相同（V1.8.5 檔案 47）。敏感度分析欄取自 V1.8.5 檔案 53 與 55，並由獨立驗證程式重算（檔案 57）；兩欄使用相同的統計程序、種子與重複次數（主要零模型 10,000 次、文獻內部結構保持零模型 5,000 次）。⏎⏎在 120 格層次，敏感度分析使 24 格的主要（去重）觀察次數與 28 格的未去重計數改變；主要零模型的方向改變 3 格（評估與審核 × 資訊統整、生成與合成 × 配置與規劃、推薦與最佳化 × 執行與協調），三格皆不在穩健集合內（V1.8.5 檔案 52–53）。穩健集合的 31 組成員與方向皆不變；新增人機增能 × 風險評估（不足呈現；文獻內部結構保持零模型 p_BH 由主要分析的 .0567 變為敏感度分析的 .0325，該格觀察次數 1 未變），移出協調與執行 × 一般決策流程（過度呈現；同一 p_BH 由 .0434 變為 .0610，觀察次數 19 未變）；共有成員沒有方向改變（V1.8.5 檔案 53、54）。這與表 4-9A 的 V9 側車結果完全一致：120 格 × 4 種分析的觀察次數、方向與 p_BH 皆相同（最大絕對差 0），替代後的穩健集合檔雜湊亦相同（V1.8.5 檔案 58）。因此，先前只由側車執行的局部替換結果，已由完整管線在事先登記的規則下重現；作為敏感度證據，本節以此完整重跑取代先前的側車結果，但兩者都不取代主要分析。⏎⏎G01–G16 在敏感度分析中全部留在穩健集合且皆為不足呈現（移除 0 組、方向改變 0 組；STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS；V1.8.5 檔案 55）。在敏感度分析中最接近 .05 判定門檻的是 G07（文獻內部結構保持零模型 p_BH = .0405）、G14（.0298）與 G16（.0223）；這些數值只屬敏感度分析，不取代表 4-4 與表 4-10 的凍結值。⏎⏎此敏感度分析的範圍有明確界限。人工標籤只涵蓋 50 筆目標稽核記錄，且集中於穩健核心相關分層，其餘記錄全部維持模型標籤；因此它回答的是「這 50 筆經人工判定的標籤修訂是否改變結論」，不回答全語料以人工標準重新編碼後的結果，也不改變第 4.5.1 節所報告的編碼者間低度一致。全語料的人類效度仍未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）。+}

## U26 — 4.11 表 (v1.8.3 line 2185) — full-reanalysis status

Source: OUT 53 (table + gained/lost + flips); OUT 55; OUT 58 §1–§4

```diff
- ；凍結的 32 組仍為推論基準；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），V1 前不建議優先執行（附錄 E40）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對〕 | 已完成
+ ；凍結的 32 組仍為推論基準；完整重分析已以稽核標籤替代敏感度分析執行（V1.8.5），結果與上述替換完全一致、G01–G16 無一移除，不取代主要分析（附錄 E40）〔V9 套件 ROBUST_CORE_LOCAL_SENSITIVITY.csv，已逐列核對；V1.8.5 檔案 53、55、58〕 | 已完成
```

Inline: ；凍結的 32 組仍為推論基準；完整重分析[-為開放驗證行動，-]{+已以稽核標籤替代敏感度分析+}執行[-條件待滿足-]（[-須先登記傳播規則並重現基準-]{+V1.8.5+}），[-V-]{+結果與上述替換完全一致、G0+}1{+–G16+} [-前-]{+無一移除，+}不[-建議優先執行-]{+取代主要分析+}（附錄 E40）〔V9 套件 ROB…SITIVITY.csv，已逐列核對{+；V1.8.5 檔案 53、55、58+}〕 | 已完成

## U27 — 4.11 (v1.8.3 line 2192) — full-reanalysis status

Source: OUT 58 §1–§4

```diff
- （人工標籤替換顯示局部成員敏感；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準），見附錄 E40）
+ （人工標籤替換顯示局部成員敏感；完整重分析已以稽核標籤替代敏感度分析執行，結果相同，不取代主要分析，見附錄 E40）
```

Inline: （人工標籤替換顯示局部成員敏感；完整重分析[-為開放驗證行動，-]{+已以稽核標籤替代敏感度分析+}執行[-條件待滿足（須先登記傳播規則並重現基準）-]{+，結果相同，不取代主要分析+}，見附錄 E40）

## U28 — 5.3.2 表 (v1.8.3 line 2240) — full-reanalysis status

Source: OUT 55

```diff
- ；完整重分析為開放驗證行動，執行條件待滿足（須先登記傳播規則並重現基準）（附錄 E40） |
+ ；V1.8.5 稽核標籤替代敏感度分析的結果相同（G01–G16 移除 0 組、方向改變 0 組；不取代主要分析）（附錄 E40） |
```

Inline: ；[-完整重-]{+V1.8.5 稽核標籤替代敏感度+}分析[-為開放驗證行動，執行條件待滿足-]{+的結果相同+}（[-須先登記傳播規則並重現基準-]{+G01–G16 移除 0 組、方向改變 0 組；不取代主要分析+}）（附錄 E40） |

## U29 — 5.4.2 (v1.8.3 line 2270) — full-reanalysis status

Source: OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 在以一致的標籤完成完整重分析之前，本研究不以替換後的集合取代凍結結果。
+ V1.8.5 以事先登記的有界規則完整重跑所有標籤相依分析後，得到與此完全相同的敏感度結果（第 4.5.5 節，表 4-9B）；這是稽核標籤替代敏感度分析，本研究仍不以替換後的集合取代凍結結果，且此分析只涉及 50 筆目標稽核記錄，不能用來說明編碼者間的低度一致已被解決。
```

Inline: [-在-]{+V1.8.5 +}以[-一致-]{+事先登記+}的[-標籤完成-]{+有界規則+}完整重{+跑所有標籤相依+}分析[-之前-]{+後，得到與此完全相同的敏感度結果（第 4.5.5 節，表 4-9B）；這是稽核標籤替代敏感度分析+}，本研究{+仍+}不以替換後的集合取代凍結結果{+，且此分析只涉及 50 筆目標稽核記錄，不能用來說明編碼者間的低度一致已被解決+}。

## U30 — 5.8.9 (v1.8.3 line 2364) — full-reanalysis triplet + corpus-wide limitation

Source: OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 第二，局部敏感度的存在使完整重分析成為必要的後續步驟（V9 套件標記為 FULL_REANALYSIS_REQUIRED；現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION，FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION，FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED；日後是否及何時重跑仍由研究者決定，附錄 E40）：在以一致的標籤或重新校準的映射程序重建矩陣並重跑四項統計／計數分析之前，
+ 第二，局部敏感度的存在使完整重分析成為必要的後續步驟（V9 套件標記為 FULL_REANALYSIS_REQUIRED）；此步驟已於 V1.8.5 以稽核標籤替代敏感度分析執行（FULL_REANALYSIS_METHOD_STATUS = SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS；FULL_REANALYSIS_EXECUTED = YES（AUDITED_LABEL_SENSITIVITY_ANALYSIS）；PRIMARY_BASELINE_REPLACED = NO；附錄 E40）：主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。其結果與局部替換完全一致（第 4.5.5 節）。但此分析只替代 50 筆目標記錄的標籤，其餘記錄維持模型標籤，因此全語料的人類效度仍未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）：在以全語料一致的人工標籤或重新校準的映射程序重建矩陣並重跑四項統計／計數分析之前，
```

Inline: 第二，局部敏感度的存在使完整重分析成…EANALYSIS_REQUIRED{+）+}；[-現-]{+此步驟已於 V1.8.5 以稽核標籤替代敏感度分析執+}行[-狀態：-]{+（+}FULL_REANALYSIS_METHOD_STATUS = [-REQU-]{+SAT+}I[-R-]{+SFI+}ED[-_BY_V9-]_AS_[-OP-]{+AUDITED_LABEL_S+}EN{+SITIVITY+}_[-V-]{+AN+}AL{+YS+}I[-DATION_ACTION，-]{+S；+}FULL_REANALYSIS_EXECUT[-ION_STATUS-]{+ED+} = {+Y+}E[-X-]{+S（AUDIT+}E[-CUT-]{+D_L+}AB{+E+}L[-E-]_[-P-]{+S+}EN[-D-]{+S+}I[-NG_PROPAGA-]TI[-ON_RULE-]{+VITY+}_AN[-D-]{+ALYSIS）；PRIMARY+}_BASELINE_REP[-RO-]{+LACE+}D[-UCTION，FULL_REANALYSIS_PRIORITY_BEFORE_V1-] = NO[-T_RECOMMENDED-]；[-日後是否及何時重跑仍由研究者決定，-]附錄 E40）：{+主要分析維持預先凍結之 V5/R14 基準；另以 50 筆目標人工稽核標籤進行有界替代，完整重跑所有標籤相依分析，以評估結論對語意標籤修訂的敏感性。其結果與局部替換完全一致（第 4.5.5 節）。但此分析只替代 50 筆目標記錄的標籤，其餘記錄維持模型標籤，因此全語料的人類效度仍未建立（CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED）：+}在以{+全語料+}一致的{+人工+}標籤或重新校準的映射程序重建矩陣並重跑四項統計／計數分析之前，

## U31 — 5.9 (v1.8.3 line 2368) — next-step wording

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 後續研究的第一個優先方向，是以一致的標籤完成文獻層的完整重分析（第 5.8.9 節；受保護輸入已全數尋回，執行前須先事先登記標籤傳播規則並在現行工作環境重現正式基準，時程排在 V1 人類構念效度驗證之後，見附錄 E40）
+ 後續研究的第一個優先方向，是以跨分層、全語料一致的標籤（人工標籤或重新校準的映射程序）進行文獻層的重分析（第 5.8.9 節；V1.8.5 已完成的是只替代 50 筆目標稽核標籤的敏感度分析，不建立全語料的人類效度，見附錄 E40）
```

Inline: 後續研究的第一個優先方向，是以{+跨分層、全語料+}一致的標籤[-完成-]{+（人工標籤或重新校準的映射程序）進行+}文獻層的[-完整-]重分析（第 5.8.9 節；[-受保護輸入-]{+V1.8.5 +}已[-全數尋回，執行前須先事先登記-]{+完成的是只替代 50 筆目標稽核+}標籤[-傳播規則並在現行工作環境重現正式基準-]{+的敏感度分析+}，[-時程排在 V1 -]{+不建立全語料的+}人類[-構念-]效度[-驗證之後-]，見附錄 E40）

## U32 — 5.10 (v1.8.3 line 2380) — full-reanalysis status

Source: OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 完整重分析列為開放的驗證行動，其執行條件尚待滿足（須先事先登記標籤傳播規則並重現正式基準）（附錄 E40）。
+ 完整重分析已於 V1.8.5 以稽核標籤替代敏感度分析執行，結果與局部替換完全一致，但只涉及 50 筆目標稽核記錄，不建立全語料的人類效度（附錄 E40）。
```

Inline: 完整重分析[-列為開放的驗證行動，其-]{+已於 V1.8.5 以稽核標籤替代敏感度分析+}執行[-條件尚待滿足（須先事先登-]{+，結果與局部替換完全一致，但只涉及 50 筆目標稽核+}記[-標籤傳播規則並重現正式基準）-]{+錄，不建立全語料的人類效度+}（附錄 E40）。

## U25 — 附錄 D (v1.8.3 line 3038) — Appendix D rows 43–61

Source: RPT file list 43–58 (56 not written per OUT 55); this round (59); 60–61 reserved

```diff
- | v1.8.3／41 | — | `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` | 合併論文 v1.8.3（V5 來源版；只更新來源與狀態描述） | 本稿 |
+ | v1.8.3／41 | — | `41_MERGED_MASTER_THESIS_v1_8_3_V5_PROVENANCE_CANDIDATE.md` | 合併論文 v1.8.3（V5 來源版；只更新來源與狀態描述） | v1.8.5 的修訂底稿（已保存；未覆寫） |
+ | v1.8.5／43–45 | — | `43_PROPAGATION_RULE_PREREGISTRATION.md`、`44_PROPAGATION_RECORD_MANIFEST.csv`、`45_PROPAGATION_RULE_HASHES.csv` | 有界稽核標籤替代規則（BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1）的執行前登記、50 筆記錄清單與雜湊 | 第 3.7.4 節；附錄 E48 |
+ | v1.8.5／46–50 | — | `46_OFFICIAL_13_OUTPUT_MANIFEST.csv`、`47_BASELINE_REPRODUCTION_REPORT.md`、`48_BASELINE_REPRODUCTION_DIFF.csv`、`49_BASELINE_ENVIRONMENT_LOCK.json`、`50_BASELINE_CODE_DIFF.md` | V5 正式基準的重現（13/13 逐位元組相同；僅修改路徑）及其環境鎖定與程式差異 | 稿件狀態；第 3.7.4、3.8.3 節；附錄 E40 |
+ | v1.8.5／49b | — | `49b_REVISED_ENVIRONMENT_LOCK.json`、`REVISED_GUARD_POLICY.md`、`REVISED_GUARD_DIFF.csv`、`REVISED_GUARD_SELF_AUDIT.md` | 敏感度重跑的環境鎖定、雙模式閘門政策、閘門差異與自我稽核 | 第 3.7.4 節 |
+ | v1.8.5／51–54 | — | `51_PROPAGATION_APPLICATION_AUDIT.csv`、`52_ALL_120_CELLS_BASELINE_VS_REVISED.csv`、`53_GLOBAL_PIPELINE_DIFF.md`、`54_ROBUST_CORE_MEMBERSHIP_DIFF.csv` | 替代規則的套用稽核；主要分析與敏感度分析的 120 格、整體與穩健集合成員比較 | 第 4.5.5 節；表 4-9B |
+ | v1.8.5／55 | — | `55_G01_G16_REVISED_STABILITY_AUDIT.md` | G01–G16 在敏感度分析下的穩定性稽核（移除 0、方向改變 0） | 第 3.8.2、4.5.5 節；附錄 E40 |
+ | v1.8.5／56 | — | （未產生） | G01–G16 無移除、無方向改變，依規則不需研究者決策備忘 | — |
+ | v1.8.5／57–58 | — | `57_INDEPENDENT_COMPUTE_VERIFICATION.md`、`58_LOCAL_SIDECAR_VS_FULL_REANALYSIS.md` | 獨立計算驗證（通過）；V9 側車與完整重跑的比較（完全一致） | 第 4.5.5 節；附錄 E39、E40 |
+ | v1.8.5／59 | — | `59_MERGED_MASTER_THESIS_v1_8_5_COMPUTE_CLOSURE_CANDIDATE.md`（另有 `59_PATCH_LOG_v1_8_5.md`、`59b_V183_TO_V185_SEGMENT_DIFF.md`） | 合併論文 v1.8.5（計算收斂版；只更新計算驗證狀態並新增標示為敏感度分析的結果） | 本稿 |
+ | v1.8.5／60–61 | — | （保留給本輪後續的狀態文件；本稿產生時尚未存在） | 本輪的凍結與最終狀態紀錄 | 稿件狀態 |
```

Inline: | v1.8.3／41 | — | …來源版；只更新來源與狀態描述） | {+v1.8.5 的修訂底稿（已保存；未覆寫） |⏎| v1.8.5／43–45 | — | `43_PROPAGATION_RULE_PREREGISTRATION.md`、`44_PROPAGATION_RECORD_MANIFEST.csv`、`45_PROPAGATION_RULE_HASHES.csv` | 有界稽核標籤替代規則（BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1）的執行前登記、50 筆記錄清單與雜湊 | 第 3.7.4 節；附錄 E48 |⏎| v1.8.5／46–50 | — | `46_OFFICIAL_13_OUTPUT_MANIFEST.csv`、`47_BASELINE_REPRODUCTION_REPORT.md`、`48_BASELINE_REPRODUCTION_DIFF.csv`、`49_BASELINE_ENVIRONMENT_LOCK.json`、`50_BASELINE_CODE_DIFF.md` | V5 正式基準的重現（13/13 逐位元組相同；僅修改路徑）及其環境鎖定與程式差異 | 稿件狀態；第 3.7.4、3.8.3 節；附錄 E40 |⏎| v1.8.5／49b | — | `49b_REVISED_ENVIRONMENT_LOCK.json`、`REVISED_GUARD_POLICY.md`、`REVISED_GUARD_DIFF.csv`、`REVISED_GUARD_SELF_AUDIT.md` | 敏感度重跑的環境鎖定、雙模式閘門政策、閘門差異與自我稽核 | 第 3.7.4 節 |⏎| v1.8.5／51–54 | — | `51_PROPAGATION_APPLICATION_AUDIT.csv`、`52_ALL_120_CELLS_BASELINE_VS_REVISED.csv`、`53_GLOBAL_PIPELINE_DIFF.md`、`54_ROBUST_CORE_MEMBERSHIP_DIFF.csv` | 替代規則的套用稽核；主要分析與敏感度分析的 120 格、整體與穩健集合成員比較 | 第 4.5.5 節；表 4-9B |⏎| v1.8.5／55 | — | `55_G01_G16_REVISED_STABILITY_AUDIT.md` | G01–G16 在敏感度分析下的穩定性稽核（移除 0、方向改變 0） | 第 3.8.2、4.5.5 節；附錄 E40 |⏎| v1.8.5／56 | — | （未產生） | G01–G16 無移除、無方向改變，依規則不需研究者決策備忘 | — |⏎| v1.8.5／57–58 | — | `57_INDEPENDENT_COMPUTE_VERIFICATION.md`、`58_LOCAL_SIDECAR_VS_FULL_REANALYSIS.md` | 獨立計算驗證（通過）；V9 側車與完整重跑的比較（完全一致） | 第 4.5.5 節；附錄 E39、E40 |⏎| v1.8.5／59 | — | `59_MERGED_MASTER_THESIS_v1_8_5_COMPUTE_CLOSURE_CANDIDATE.md`（另有 `59_PATCH_LOG_v1_8_5.md`、`59b_V183_TO_V185_SEGMENT_DIFF.md`） | 合併論文 v1.8.5（計算收斂版；只更新計算驗證狀態並新增標示為敏感度分析的結果） | +}本稿 |{+⏎| v1.8.5／60–61 | — | （保留給本輪後續的狀態文件；本稿產生時尚未存在） | 本輪的凍結與最終狀態紀錄 | 稿件狀態 |+}

## U33 — 附錄 E39 (v1.8.3 line 3082) — residual limit (c) — sidecar reproduced

Source: OUT 58 §1–§4

```diff
- 產生敏感度表本身的程式仍未尋回，替換後成員係由敏感度表逐列重現，並與尋回的替換後核心檔一致；
+ 產生敏感度表本身的程式仍未尋回，替換後成員係由敏感度表逐列重現，並與尋回的替換後核心檔一致；v1.8.5 已以完整管線在事先登記的規則下獨立重現側車結果，替換後核心檔的雜湊相同（V1.8.5 檔案 58）；
```

Inline: 產生敏感度表本身的程式仍未尋回，替換…列重現，並與尋回的替換後核心檔一致；{+v1.8.5 已以完整管線在事先登記的規則下獨立重現側車結果，替換後核心檔的雜湊相同（V1.8.5 檔案 58）；+}

## U34 — 附錄 E40 (v1.8.3 line 3083) — full-reanalysis triplet (executed as sensitivity analysis)

Source: OUT 43 §1–§5; OUT 44; OUT 45; OUT 47 §2–§5; OUT 48; OUT 49; OUT 50; REVISED_GUARD_POLICY; REVISED_GUARD_SELF_AUDIT; REVISED_GUARD_DIFF.csv; OUT 49b; OUT 53 (table + gained/lost + flips); OUT 55; OUT 57; OUT 58 §1–§4; orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 現行狀態：FULL_REANALYSIS_METHOD_STATUS = REQUIRED_BY_V9_AS_OPEN_VALIDATION_ACTION；FULL_REANALYSIS_EXECUTION_STATUS = EXECUTABLE_PENDING_PROPAGATION_RULE_AND_BASELINE_REPRODUCTION（v1.8.3：37 項受保護輸入已全數以完整 SHA-256 確認，E39（b）；尚待三項前置條件：研究者事先登記並以雜湊承諾標籤傳播規則、在新的日期目錄中以僅修改路徑的程式複本逐位元組重現 13 個雜湊釘定的正式輸出、依 V9 經研究者核准；V1.8.3 檔案 38）；FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED（V1.8 檔案 07 §8；V1.8.1 檔案 15、17；屬研究者決定。原理由 1「受保護輸入缺件」已不成立，理由 2–5 仍成立；已請研究者重新檢視此優先順序的理由：PRIORITY_RATIONALE_REVIEW_REQUESTED）。V9 套件記為須經研究者核准；日後是否及何時重跑仍由研究者決定；重跑時的標籤輸入只能取自 V1.8 檔案 04 表 T4（V1.8.1 檔案 15）；重跑前須先事先登記並以雜湊承諾標籤傳播規則（E48），並在現行工作環境重現正式基準；若重分析改變 L2，須依凍結程序重新產生 G 清單並重跑 V1 封包，不得只增修單一格 |
+ 已執行（v1.8.5），屬敏感度分析：FULL_REANALYSIS_METHOD_STATUS = SATISFIED_AS_AUDITED_LABEL_SENSITIVITY_ANALYSIS；FULL_REANALYSIS_EXECUTED = YES（AUDITED_LABEL_SENSITIVITY_ANALYSIS）；PRIMARY_BASELINE_REPLACED = NO；CORPUS_WIDE_HUMAN_VALIDITY = NOT_ESTABLISHED。研究者核准後，先以僅修改路徑的程式複本重現正式基準（13/13 逐位元組相同；V1.8.5 檔案 46–50），再依事先登記的 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1（E48）完整重跑第 10–13 階段（雙模式閘門政策；獨立驗證通過；V1.8.5 檔案 51–57）。敏感度分析的結果（不取代主要分析）：兩端皆完成分類的記錄 3,107、文獻 781、文獻層級邊 2,181、主要零模型 p_BH ≤ .05 共 47 格、穩健集合 32 格（15／17），與 V9 側車結果完全一致（V1.8.5 檔案 53、58）；G01–G16 移除 0 組、方向改變 0 組（STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS；V1.8.5 檔案 55）。主要分析與 G 清單維持凍結，L2 未被取代，因此不需重新產生 G 清單或重跑 V1 封包。新增的不足呈現（人機增能 × 風險評估）不屬於 G01–G16，是否增列屬另一項研究者治理決定，本稿不增列。原 FULL_REANALYSIS_PRIORITY_BEFORE_V1 = NOT_RECOMMENDED 為 v1.8.3 以前的優先順序判定；研究者其後核准在 V1 之前執行此有界的敏感度分析。全語料的人類效度仍待跨分層的獨立人工樣本（第 5.9 節） |
```

Inline: [-現-]{+已執+}行[-狀態-]{+（v1.8.5），屬敏感度分析+}：FULL_REANALYSIS_METHOD_STATUS = [-REQU-]{+SAT+}I[-R-]{+SFI+}ED[-_BY_V9-]_AS_[-OP-]{+AUDITED_LABEL_S+}EN{+SITIVITY+}_[-V-]{+AN+}AL{+YS+}I[-DATION_ACTION-]{+S+}；FULL_REANALYSIS_EXECUT[-ION_STATUS-]{+ED+} = {+Y+}E[-X-]{+S（AUDIT+}E[-CUT-]{+D_L+}AB{+E+}L[-E-]_[-P-]{+S+}EN[-D-]{+S+}I[-NG_PROPAGA-]TI[-ON_RULE-]{+VITY+}_AN[-D-]{+ALYSIS）；PRIMARY+}_BASELINE_REP{+LACED = NO；CO+}R{+PUS_WIDE_HUMAN_VALIDITY = N+}O[-DUC-]T{+_ESTABL+}I[-ON（v1.8.3：37 項受保護輸入已全數以完整 -]SH[-A-256 確認，-]E[-39（b）；尚待三項前置條件：-]{+D。+}研究者[-事-]{+核准後，+}先[-登記並以雜湊承諾標籤傳播規則、在新的日期目錄中-]以僅修改路徑的程式複本{+重現正式基準（13/13 +}逐位元組[-重現 13 個雜湊釘定的正式輸出、依 V9 經研究者核准-]{+相同+}；V1.8.[-3-]{+5+} 檔案 {+46–50），再依事先登記的 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1（E48）完整重跑第 10–1+}3{+ 階段（雙模式閘門政策；獨立驗證通過；V1.8.5 檔案 51–57）。敏感度分析的結果（不取代主要分析）：兩端皆完成分類的記錄 3,107、文獻 781、文獻層級邊 2,181、主要零模型 p_BH ≤ .05 共 47 格、穩健集合 32 格（15／17），與 V9 側車結果完全一致（V1.8.5 檔案 53、5+}8）；{+G01–G16 移除 0 組、方向改變 0 組（STABLE_UNDER_FULL_AUDITED_LABEL_REANALYSIS；V1.8.5 檔案 55）。主要分析與 G 清單維持凍結，L2 未被取代，因此不需重新產生 G 清單或重跑 V1 封包。新增的不足呈現（人機增能 × 風險評估）不屬於 G01–G16，是否增列屬另一項研究者治理決定，本稿不增列。原 +}FULL_REANALYSIS_PR… = NOT_RECOMMENDED[-（V1.8-] [-檔案-]{+為+} [-07 §8；V-]{+v+}1.8.[-1-]{+3+} [-檔案 15、17；屬研究者決定。原理由 1「受保護輸入缺件」已不成立，理由 2–5 仍成立；已請研究者重新檢視此-]{+以前的+}優先順序[-的理由：PRIORITY_RATIONALE_REVIEW_REQUESTED）。V9 套件記為須經-]{+判定；+}研究者{+其後+}核准[-；日後是否及何時重跑仍由研究者決定；重跑時的標籤輸入只能取自 V1.8 檔案 04 表 T4（V1.8.1 檔案 15）；重跑前須先事先登記並以雜湊承諾標籤傳播規則（E48），並-]在[-現行工作環境重現正式基準；若重分析改變 L2，須依凍結程序重新產生 G 清單並重跑-] V1 [-封包，不得只增修單一格-]{+之前執行此有界的敏感度分析。全語料的人類效度仍待跨分層的獨立人工樣本（第 5.9 節）+} |

## U35 — 附錄 E44 (v1.8.3 line 3087) — submission-readiness reason

Source: orchestrator v1.8.5 allowed-edit list (semantics / triplet / status line)

```diff
- 完整重分析為開放驗證行動且執行條件待滿足（E40）、
+ 全語料人類效度未建立（完整重分析已以稽核標籤替代敏感度分析執行，E40）、
```

Inline: {+全語料人類效度未建立（+}完整重分析[-為開放驗證行動且-]{+已以稽核標籤替代敏感度分析+}執行[-條件待滿足（-]{+，+}E40）、

## U36 — 附錄 E48 (v1.8.3 line 3091) — propagation rule status (resolved)

Source: OUT 43 §1–§5; OUT 44; OUT 45

```diff
- 以獨立程式重算可重現側車的逐筆處理與配對資格變動，但屬事後尋回、非事前登記；
+ 以獨立程式重算可重現側車的逐筆處理與配對資格變動，屬事後尋回；v1.8.5 已解決：研究者核准採用此規則，並在敏感度重跑之前以 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 之名逐欄登記與雜湊承諾（V1.8.5 檔案 43–45）；
```

Inline: 以獨立程式重算可重現側車的逐筆處理與配對資格變動，[-但-]屬事後尋回[-、非事-]{+；v1.8.5 已解決：研究者核准採用此規則，並在敏感度重跑之+}前{+以 BOUNDED_AUDITED_LABEL_SUBSTITUTION_V1 之名逐欄+}登記{+與雜湊承諾（V1.8.5 檔案 43–45）+}；

## U37 — 附錄 E48 (v1.8.3 line 3091) — propagation rule action (resolved)

Source: OUT 43 §1–§5; OUT 44; OUT 45

```diff
- 由研究者決定是否採用尋回的傳播規則（或另訂規則），事先登記並以雜湊承諾後，移除第 3.7.4 節的 `[AUTHOR TO CONFIRM]`；若執行完整重分析（E40），須以此登記的規則執行 |
+ 已解決（v1.8.5）：規則已經研究者核准並事先登記，第 3.7.4 節的 `[AUTHOR TO CONFIRM]` 已移除；敏感度重跑即以此登記的規則執行（E40） |
```

Inline: [-由-]{+已解決（v1.8.5）：規則已經+}研究者[-決定是否採用尋回的傳播規則（或另訂規則），-]{+核准並+}事先登記[-並以雜湊承諾後-]，[-移除-]第 3.7.4 節的 `[AUTHOR TO CONFIRM]`{+ 已移除+}；[-若執行完整-]{+敏感度+}重[-分析（E40），須-]{+跑即+}以此登記的規則執行{+（E40）+} |
