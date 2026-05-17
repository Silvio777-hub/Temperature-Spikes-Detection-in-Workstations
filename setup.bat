@echo off
echo ==================================================
echo   Temperature Spikes Detection: System Setup Wizard
echo ==================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo [1/3] Creating Project Directories...
if not exist "Data\raw" mkdir "Data\raw"
if not exist "Data\validated" mkdir "Data\validated"
if not exist "Data\processed" mkdir "Data\processed"
if not exist "Models" mkdir "Models"
if not exist "Logs" mkdir "Logs"
if not exist "Reports" mkdir "Reports"

echo [2/3] Installing Dependencies...
pip install -r requirements.txt

echo [3/3] Running System Verification...
python -m tests.test_cps_logic

echo.
echo ==================================================
echo   SETUP COMPLETE: Your CPS is ready for action!
echo ==================================================
echo To start PC1 Training: python -m thermal_system.main monitor
echo To start PC2 Monitoring: python -m thermal_system.main monitor --ml
echo To generate health diagnostics report: python -m thermal_system.main diagnose
echo.
pause
