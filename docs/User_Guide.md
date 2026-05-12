# Thermal-Guard: User & Developer Guide

## 1. Navigating the UI
The **Real-Time Monitor** uses color-coding to communicate health:
- **GREEN**: Normal operations.
- **YELLOW (ALERT)**: Temperature > 75°C or ML Anomaly detected.
- **RED (CRITICAL)**: Temperature > 85°C. Immediate action required.
- **CYAN (STABLE)**: Recovery phase. System is cooling down.

## 2. Configuring Thresholds
You can adjust the sensitivity of the system by modifying the parameters in `Code/state_model.py`:
- `critical_temp`: Default 85.
- `alert_temp`: Default 75.

To adjust ML sensitivity, change the `contamination` parameter in `Code/model_training.py` (Default is `0.05` or 5%).

## 3. Using the Remote API
Start the server: `python -m Code.main api`.
Use the following endpoints:
- `GET /health`: Returns the current system state.
- `GET /metrics/latest`: Returns a JSON of the last sensor reading.

**Example Request (Powershell)**:
```powershell
Invoke-RestMethod -Uri http://localhost:8000/health -Headers @{"X-API-KEY"="CPS_SECURE_TOKEN_2026"}
```

## 4. Troubleshooting
- **GPU Temp is N/A**: Ensure you have an NVIDIA GPU and drivers are installed.
- **WMI Errors**: Run your terminal as **Administrator**.
- **Model not loading**: Ensure you have copied the `Models/` folder from PC1 to PC2.

## 5. Interpreting Anomalies
An anomaly (Label 1) occurs when the **Isolation Forest** detects a statistical outlier. This could be caused by:
- A sudden frequency jump.
- High Disk I/O without a corresponding increase in Fan speed.
- A temperature rate of change (slope) that is too steep.
