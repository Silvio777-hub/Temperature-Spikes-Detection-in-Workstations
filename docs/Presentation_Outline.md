# Presentation Outline: Thermal-Guard CPS

*Use this outline to build your PowerPoint slides.*

---

## Slide 1: Title Slide
- **Title**: Thermal-Guard: Machine Learning Driven CPS for Workstation Health
- **Subtitle**: Detecting and Mitigating Thermal Anomalies in Real-Time
- **Presenter**: [Your Name]

## Slide 2: The Problem
- **Bullet Points**:
    - Hardware overheating leads to permanent damage.
    - Standard thresholds are too late or too sensitive.
    - Need for "Intelligent" hardware awareness.
- **Visual**: A picture of a heat map or a "Blue Screen of Death."

## Slide 3: The Solution (Architecture)
- **Diagram Description**: Show the 4 Layers.
    - 1. Sense (Telemetry)
    - 2. Clean (Validation)
    - 3. Think (Isolation Forest ML)
    - 4. Act (Mitigation/Alerts)

## Slide 4: Methodology (PC1 vs PC2)
- **Left Side (PC1)**: Data Collection & Model Training (Baseline).
- **Right Side (PC2)**: Edge Deployment & Live Inference (Detection).
- **Goal**: Demonstrate cross-machine scalability.

## Slide 5: The Machine Learning Core
- **Model**: Isolation Forest.
- **Why**: Unsupervised, fast, and handles multi-dimensional data (Temp, Fan, Power, I/O).
- **Outcome**: Binary classification (Normal vs Anomaly).

## Slide 6: Real-Time Monitoring & Actuation
- **Feature**: Root Cause Analysis (Identifying the process).
- **Feature**: Automated Mitigation (Protecting the hardware).
- **Feature**: Desktop Notifications (User awareness).

## Slide 7: Remote Scalability & Security
- **Feature**: Secure REST API (FastAPI).
- **Security**: X-API-KEY Authentication.
- **Use Case**: Centralized IT health dashboard.

## Slide 8: Demonstration Results
- **Stress Tool**: Prime95.
- **Observation**: Show a chart of Temperature rising vs. the System State switching to CRITICAL.
- **Success**: System successfully killed the stress process.

## Slide 9: Conclusion
- **Summary**: We built a complete closed-loop CPS.
- **Achievement**: Reached >95% accuracy in spike detection.
- **Vision**: Towards predictive maintenance in modern IT infrastructure.

## Slide 10: Q&A
- **Text**: "Thank you for your attention. Any questions?"
