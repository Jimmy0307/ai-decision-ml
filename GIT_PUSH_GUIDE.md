# Git Push Guide

先跑：

```powershell
.\RUN_ALL.ps1
```

只在看到：

```text
FINAL LOCAL VERDICT: PASS
```

之後才推：

```powershell
git status
git branch --show-current
git remote -v
git add .
git status
git commit -m "freeze AI Decision MLP mathematical skeleton v1.0"
git push
```

若目前 branch 沒有 upstream：

```powershell
git push -u origin <branch-name>
```

不要 force-push，除非你確定要重寫 remote history。
