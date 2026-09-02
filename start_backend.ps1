# Kochi Metro ERP Backend Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting Kochi Metro Rail ERP Backend Server" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$pythonPaths = @(
    "C:\Users\sahil\.antigravity\kochi metro\python_embed\python.exe",
    "python.exe",
    "python3.exe",
    "py.exe"
)

$pythonExe = $null
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonExe = $path
        break
    } else {
        $cmd = Get-Command $path -ErrorAction SilentlyContinue
        if ($cmd) {
            $pythonExe = $cmd.Source
            break
        }
    }
}

if (-not $pythonExe) {
    Write-Error "Python executable not found. Please install Python 3.9+."
    Exit 1
}

Write-Host "Using Python: $pythonExe" -ForegroundColor Green
$backendDir = Join-Path $PSScriptRoot "backend"
Set-Location $backendDir

& $pythonExe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
