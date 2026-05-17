@echo off
echo Starting Temperature Spikes Detection in Workstations...
python -m thermal_system.main monitor --ml
pause
