@echo off
title Deploy to Vercel - Ganesh Engineering Portal
color 0a
echo =========================================================================
echo   DEPLOYING GANESH ENGINEERING PORTAL TO VERCEL
echo =========================================================================
echo.
cd /d "%~dp0"

echo Running Vercel CLI...
echo (If prompted, press 'y' to install vercel and log in with your browser)
echo.
npx -y vercel

echo.
echo =========================================================================
echo If this is a production deployment, run: npx vercel --prod
echo =========================================================================
pause
