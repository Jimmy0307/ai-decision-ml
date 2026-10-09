# AI × Decision × MLP v1.0 — One Package

這包就是本地驗證 + Git 的唯一版本，不要再混用前面的 v0.x 包。

## 本地跑法

Windows 直接：
- 雙擊 `RUN_ALL.bat`
- 或 PowerShell 執行 `.\RUN_ALL.ps1`

最後必須看到：

`FINAL LOCAL VERDICT: PASS`

預期：
- 9/9 scenarios PASS
- 768 domain cases
- 3,121 canonical feasible-state occurrences
- 0 mismatch
- mutation 720/768 detected
- returned-solution constraints PASS

通過後再看 `GIT_PUSH_GUIDE.md`。

所有 numeric values 都是 simulated mathematical-feasibility inputs。
沒有使用 JPC 內部權限資料。
v1.0 freeze 的是數學骨架，不是 empirical calibration。
