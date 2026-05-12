# Academic Report: Cyber-Physical System for Workstation Temperature Spike Detection

**Date**: May 12, 2026  
**Subject**: Cyber-Physical Systems / Hardware Monitoring  
**Project Access**: [GitHub Repository](https://github.com/Silvio777-hub/Temperature-Spikes-Detection-in-Workstations)

---

## 1. Abstract
This project presents a closed-loop Cyber-Physical System (CPS) developed to monitor workstation health and detect thermal anomalies. Using an **Isolation Forest** unsupervised machine learning model, the system identifies temperature spikes that deviate from historical baselines. The system implements a 4-layer architecture, incorporating hardware-level actuation to mitigate overheating through automated process termination.

## 2. Introduction
In high-performance computing environments, thermal management is critical for hardware longevity and system reliability. Traditional threshold-based monitoring often fails to detect subtle, non-linear anomalies. This project bridges that gap by implementing an intelligent monitoring solution that learns the specific thermal "fingerprint" of a workstation.

## 3. System Architecture
The system is modeled as a 4-layer CPS:
- **Data Collection**: Interfaces with WMI, psutil, and py3nvml to gather CPU, GPU, Fan, and Power telemetry.
- **Data Processing**: Implements noise reduction and feature engineering (rolling averages and rate of change).
- **Intelligence Layer**: Uses Scikit-learn to perform anomaly detection and classify the system into four states: NORMAL, ALERT, CRITICAL, and STABLE (RECOVERY).
- **Actuation Layer**: Executes OS-level commands to notify users and terminate offending processes.

## 4. Methodology
### 4.1 Data Collection (PC1)
PC1 was utilized to collect 5,000 samples of "Normal" system behavior, covering idle, web browsing, and light office tasks.
### 4.2 Training
The **Isolation Forest** algorithm was selected due to its efficiency in high-dimensional feature spaces and its ability to detect outliers without pre-labeled datasets.
### 4.3 Deployment (PC2)
The trained model was deployed to PC2 (Edge Node). Anomalies were simulated using **Prime95** to force sustained thermal load.

## 5. Key Features
- **Cross-Platform Support**: Seamless operation on Windows and Linux.
- **State Persistence**: Health states are saved to JSON, allowing the system to remember health status across reboots.
- **Secure REST API**: Enables remote health auditing via FastAPI with X-API-KEY authentication.
- **Root Cause Analysis**: Identifies the specific PID/Process responsible for thermal stress.

## 6. Technologies Used
- **Programming Language**: Python 3.8+
- **ML Libraries**: Scikit-Learn, NumPy, Pandas, Joblib
- **System Telemetry**: psutil, WMI, py3nvml
- **Web/API**: FastAPI, Uvicorn
- **UI/UX**: Rich, Plyer (Notifications), Matplotlib

## 7. Results & Achievement
Testing with **Prime95** demonstrated a detection latency of less than 2 seconds. The system correctly transitioned from NORMAL to CRITICAL when temperatures exceeded 85°C or when the ML model detected a statistical spike. The Actuation layer successfully terminated the Prime95 process, returning the system to a STABLE state.

## 8. Conclusion
The "Temperature Spikes Detection in Workstations" project successfully demonstrates the application of ML in hardware safety. It provides a robust framework for proactive workstation maintenance and automated thermal protection.

## 9. Future Work
- Integration with Time-Series Databases (InfluxDB).
- Implementation of encrypted JWT-based API security.
- Hardware-level fan curve control (Actuation expansion).

## 10. References
- Scikit-learn: Isolation Forest Documentation.
- psutil: System and process utilities for Python.
- NIST Special Publication 800-82: Guide to CPS Security.
