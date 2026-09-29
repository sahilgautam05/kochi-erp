@echo off
title Kochi Metro ERP - Backend Server
echo ===================================================
echo   Starting Kochi Metro Rail ERP Backend Server
echo ===================================================

set PYTHON_EXE=""
if exist "C:\Users\sahil\.antigravity\kochi metro\python_embed\python.exe" (
    set PYTHON_EXE="C:\Users\sahil\.antigravity\kochi metro\python_embed\python.exe"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_EXE=python
    ) else (
        where py >nul 2>nul
        if %ERRORLEVEL% EQU 0 (
            set PYTHON_EXE=py
        )
    )
)

if %PYTHON_EXE%=="" (
    echo [ERROR] Python was not found on your system.
    echo Please ensure Python is installed and accessible in PATH.
    pause
    exit /b 1
)

echo Using Python: %PYTHON_EXE%

:: Free port 8000 if occupied by a zombie process
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Freeing port 8000 from PID %%a...
    taskkill /F /PID %%a >nul 2>nul
)

cd /d "%~dp0backend"

:START_LOOP
echo.
echo [INFO] Starting Uvicorn server on http://127.0.0.1:8000 ...
%PYTHON_EXE% -m uvicorn main:app --host 0.0.0.0 --port 8000
echo.
echo [WARNING] Server stopped. Restarting in 3 seconds... (Press Ctrl+C to cancel)
timeout /t 3 /nobreak >nul
goto START_LOOP
