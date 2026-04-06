@echo off
title Gramin-Setu Web Kiosk (Test 2)
color 0B
cd /d "%~dp0"
echo ===================================================
echo   Starting Assisted Digital Kiosk Web Server...
echo ===================================================
echo Opening Browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:8000/web

echo Launching FastAPI Brain Engine...
.\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000
pause
