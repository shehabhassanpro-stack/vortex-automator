@echo off
title Luxury Auto Presser
echo ===================================================
echo     Installing / Verifying Requirements...
echo ===================================================
pip install -r requirements.txt
echo.
echo ===================================================
echo     Launching Luxury Auto Presser & Clicker...
echo ===================================================
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)
