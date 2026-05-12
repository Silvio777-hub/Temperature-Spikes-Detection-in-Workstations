# System Architecture

The Thermal Spike Detection system is designed as a modular **Cyber-Physical System (CPS)**. It bridges physical hardware sensors with advanced unsupervised machine learning to protect workstation longevity.

## Component Layers

1.  **Collection Layer**: Interface with WMI (Windows) and Sysfs (Linux) to retrieve physical thermal telemetry.
2.  **Processing Layer**: Real-time signal smoothing and feature engineering (calculating thermal gradients).
3.  **Detection Layer**: Hybrid engine combining deterministic safety thresholds with **Isolation Forest** statistical anomaly detection.
4.  **UI Layer**: High-fidelity terminal dashboard for real-time mission control.

## Data Flow
Physical Sensors -> Collector -> Circular Buffer -> Feature Engineer -> Integrator -> UI & Storage
