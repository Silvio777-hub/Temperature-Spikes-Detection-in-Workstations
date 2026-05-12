# Project Methodology

## Feature Selection
Our research identified **Temperature Rate of Change (°C/sec)** as the most critical predictor of thermal runaway. By correlating this with **Thermal Efficiency** (CPU Load vs Heat Output), the system can distinguish between normal intense workloads and cooling failures.

## Algorithm Selection
We evaluated several unsupervised models:
- **Isolation Forest**: Selected for its speed and effectiveness in high-dimensional feature spaces.
- **One-Class SVM**: Used as a baseline for comparison.

## Anomaly Injection
Evaluation was performed by intentionally inducing thermal stress using `scripts/cpu_stress_test.py`, creating a ground-truth dataset for precision/recall analysis.
