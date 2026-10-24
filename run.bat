@echo off
title Ganesh Engineering Industries - Production Logging Portal
color 0b
echo =========================================================================
echo   GANESH ENGINEERING INDUSTRIES - PRODUCTION & LOGGING PORTAL
echo   Developed by: Tushar (B.Tech CSE Core)
echo   Supervisor: Mr. Manish Saini (IT & Systems)
echo =========================================================================
echo.
cd /d "%~dp0"

set "PY_EXE=python"
if exist "C:\Users\Tushar\AppData\Local\Python\bin\python.exe" (
    set "PY_EXE=C:\Users\Tushar\AppData\Local\Python\bin\python.exe"
)

echo Starting Portal with: %PY_EXE%
echo Application running at: http://127.0.0.1:5000
echo.
"%PY_EXE%" app.py
pause
