# Video Script: Advanced Thermal Anomaly Detection in Workstations

## Scene 1: Introduction & Project Overview
**Visual**: Show the project root folder.
**Action**: Scroll through the `Code/`, `Data/`, and `Models/` folders.
**Audio**: "Welcome. This project implements a comprehensive Cyber-Physical System (CPS) for workstation health monitoring. Our goal is to detect thermal anomalies and execute automated mitigation using unsupervised machine learning."

---

## Scene 2: Part 1 - Training Node (PC1)
**Visual**: Terminal on PC1.
**Action**: Run `python -m Code.main monitor`.
**Audio**: "We start on PC1. Here, we are collecting 'Normal' baseline telemetry. The system captures temperature, CPU load, and RAM usage to understand the workstation's healthy state."
**Action**: Run `python -m Code.main train`.
**Audio**: "Now, we invoke the Analytics Layer. We are training an Isolation Forest model on the collected data. This creates the 'intelligence' that will be used to protect our edge nodes."

---

## Scene 3: Deployment & Scalability (The Transfer)
**Visual**: Show copying the `Models/` folder.
**Audio**: "To demonstrate scalability, we transfer the trained models from the Server (PC1) to the Edge Node (PC2). This proves the system can be deployed across a heterogeneous network."

---

## Scene 4: Part 2 - Monitoring & Detection (PC2)
**Visual**: Terminal on PC2.
**Action**: Run `python -m Code.main monitor --ml`.
**Audio**: "On PC2, we are running the real-time detector using the PC1 model. The system is currently in a NORMAL state."
**Action**: Open a new terminal and run `python -m Code.main stress --duration 60`.
**Audio**: "I am now initiating a synthetic stress test. Watch as the temperature spikes."
**Visual**: The dashboard state changes to ALERT then CRITICAL.
**Audio**: "The ML model has identified the anomaly. It triggers the Actuation Layer, which performs Root Cause Analysis to identify the offending process and sends a desktop notification."

---

## Scene 5: Advanced Features (API & Reports)
**Visual**: Browser window at `localhost:8000/health`.
**Audio**: "For remote management, our Secure API allows administrators to check workstation health over the network using an X-API-KEY."
**Action**: Run `python -m Code.system_report`.
**Audio**: "Finally, we generate an automated health report, providing statistical evidence and trend visualizations for academic and professional review."

---

## Scene 6: Conclusion
**Visual**: Show the final charts in the `Reports/` folder.
**Audio**: "This project successfully bridges hardware telemetry with machine learning to create a secure, responsive, and autonomous monitoring solution. Thank you."
