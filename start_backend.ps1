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

# Free port 8000 if occupied
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($proc in $processes) {
            Stop-Process -Id $proc.OwningProcess -Force -ErrorAction SilentlyContinue
            Write-Host "Freed port 8000 from PID $($proc.OwningProcess)" -ForegroundColor Yellow
        }
    }
} catch {}

$backendDir = Join-Path $PSScriptRoot "backend"
Set-Location $backendDir

while ($true) {
    Write-Host "`n[INFO] Starting Uvicorn on http://127.0.0.1:8000..." -ForegroundColor Cyan
    & $pythonExe -m uvicorn main:app --host 0.0.0.0 --port 8000
    Write-Host "`n[WARNING] Server stopped. Auto-restarting in 3 seconds... (Press Ctrl+C to stop)" -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}
