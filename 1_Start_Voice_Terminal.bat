@echo off
title Gramin-Setu AI-PCO Terminal (Test 1)
color 0A
cd /d "%~dp0"
echo ===================================================
echo   Starting AI Voice Box (Smart Speaker Mode)
echo ===================================================
.\.venv\Scripts\python.exe ai_pco_terminal.py
pause
