# Final Video Script: The Thermal-Guard Demonstration

---

## 🎥 Introduction (0:00 - 0:30)
**Visual**: Show the project title on screen.
**Audio**: "Hello. Today I am demonstrating Thermal-Guard, a Cyber-Physical System that uses Machine Learning to protect workstations from thermal anomalies. This system doesn't just monitor—it thinks and acts."

---

## 🏗️ Part 1: The Training Node (PC1) (0:30 - 1:30)
**Visual**: Screen recording of PC1.
**Audio**: "We start on PC1, our Training Node. I am currently running the monitor to capture 5 minutes of 'Normal' system activity. Notice how the system tracks CPU temperature, GPU status, and even Fan speeds."
**Action**: Run `python -m Code.main monitor`.
**Audio**: "Now that our baseline is captured, I will train the Isolation Forest model. This model learns the unique thermal fingerprint of this hardware."
**Action**: Run `python -m Code.main train`. Show the `.pkl` files in the `Models/` folder.

---

## 📂 Part 2: Deployment (1:30 - 2:00)
**Visual**: Show copying the `Models/` folder from PC1 to PC2.
**Audio**: "Scalability is key. I am now deploying the trained models to PC2, our Edge Monitoring Node. This machine is now 'Armed' with the knowledge from our training session."

---

## 🔥 Part 3: The Stress Test (PC2) (2:00 - 3:30)
**Visual**: Screen recording of PC2.
**Action**: Run `python -m Code.main monitor --ml`.
**Audio**: "On PC2, the system is in 'Live Guard' mode. To simulate a real-world anomaly, I will use **Prime95**, a powerful stress-testing tool that pushes the CPU to its thermal limit."
**Action**: Start Prime95 "Small FFTs" test on PC2.
**Visual**: The temperature on the monitor climbs rapidly (60... 70... 85°C).
**Audio**: "Watch the dashboard. As Prime95 generates extreme heat, the system state transitions from NORMAL to ALERT, and finally to CRITICAL."
**Action**: The Mitigation logic triggers. Show the notification.
**Audio**: "Anomaly detected! The system identifies Prime95 as the root cause and executes automated mitigation to terminate the process and save the hardware."

---

## 📡 Part 4: API & Reports (3:30 - 4:15)
**Visual**: Show the browser health check and the generated report PDF.
**Audio**: "Beyond local monitoring, the system provides a Secure REST API for remote health audits and generates automated statistical reports for administrative review."

---

## 🏁 Conclusion (4:15 - 4:45)
**Visual**: Final chart of the thermal trend.
**Audio**: "Thermal-Guard successfully bridges the gap between hardware sensors and intelligent automation. A complete, closed-loop solution for modern workstation safety. Thank you."
