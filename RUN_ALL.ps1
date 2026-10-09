$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 .\run_all.py
} else {
    python .\run_all.py
}
if ($LASTEXITCODE -ne 0) {
    throw "Validation failed. Do not push v1.0 as frozen."
}
