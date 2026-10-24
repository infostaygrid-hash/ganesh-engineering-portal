@echo off
title Push Project to GitHub - Ganesh Engineering Portal
color 0a
echo =========================================================================
echo   PUSHING TO GITHUB: infostaygrid-hash/ganesh-engineering-portal
echo =========================================================================
echo.
cd /d "%~dp0"

echo Running: git push -u origin main
echo (If a browser window pops up, click 'Sign in with your browser')
echo.
git push -u origin main

echo.
echo =========================================================================
if errorlevel 0 (
    echo SUCCESS: Project pushed to GitHub successfully!
) else (
    echo If there was an error with existing files in repo, run: git push -f -u origin main
)
echo =========================================================================
pause
