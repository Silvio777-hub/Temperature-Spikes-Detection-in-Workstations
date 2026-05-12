@echo off
setlocal
title TSD Project - Full Demo

echo ======================================================
echo   Temperature Spike Detection - Project Demo
echo ======================================================
echo.

:: 1. Algorithm Comparison
echo [1/4] Running Algorithm Benchmarking (Comparison)...
python src/compare.py
echo.

:: 2. Fast Training
echo [2/4] Training Model (Establishing Baseline)...
python monitor.py train
echo.

:: 3. Simulation & Logic Test
echo [3/4] Running Simulation Test...
echo This will simulate a thermal spike to verify detection logic.
python monitor.py simulate
echo.

:: 4. Report Generation
echo [4/4] Generating Final Thermal Audit Report (PDF)...
python monitor.py report
echo.

echo ======================================================
echo   DEMO COMPLETE! 
echo   Check the 'reports/' folder for the PDF.
echo ======================================================
echo To start real-time monitoring: python monitor.py monitor
echo.
pause
