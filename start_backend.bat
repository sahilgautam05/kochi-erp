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
    echo Error: Python was not found on your system.
    echo Please ensure Python is installed and accessible in PATH.
    pause
    exit /b 1
)

echo Using Python: %PYTHON_EXE%
cd /d "%~dp0backend"
%PYTHON_EXE% -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
