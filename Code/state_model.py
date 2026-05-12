import json
import os
import datetime

class CPSState:
    """CPS Health States as defined in Section 5.2 of the Proposal."""
    NORMAL = "NORMAL"         # Stable temperature and performance
    ALERT = "ALERT"           # Elevated temperature or abnormal trends
    CRITICAL = "CRITICAL"     # Sustained overheating or unsafe conditions
    STABLE = "STABLE (RECOVERY)" # System cooling down after intervention

class HealthStateModel:
    """
    Analytics Layer: Health Classification with State Persistence.
    Determines the CPS state and saves it to disk for cross-reboot tracking.
    """
    def __init__(self, critical_temp=85, alert_temp=75, state_file="Models/system_state.json"):
        self.critical_temp = critical_temp
        self.alert_temp = alert_temp
        self.state_file = state_file
        self.current_state = self.load_state()

    def save_state(self):
        """Saves current state to a JSON file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({"last_state": self.current_state, "timestamp": str(datetime.datetime.now())}, f)
        except Exception:
            pass

    def load_state(self):
        """Loads previous state from disk to maintain continuity across restarts."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f).get("last_state", CPSState.NORMAL)
            except Exception:
                return CPSState.NORMAL
        return CPSState.NORMAL

    def classify(self, metrics, anomaly_score):
        """
        Classifies the system state.
        Anomaly Score: -1 (Anomaly), 1 (Normal) from Isolation Forest.
        """
        temp = metrics.get("temperature", 0)
        
        # 1. Critical State: Immediate danger
        if temp >= self.critical_temp:
            self.current_state = CPSState.CRITICAL
            return CPSState.CRITICAL, "URGENT: Sustained overheating detected!"

        # 2. Alert State: Abnormal trends or high heat
        if temp >= self.alert_temp or anomaly_score == -1:
            self.current_state = CPSState.ALERT
            return CPSState.ALERT, "WARNING: Abnormal thermal pattern or elevated temperature."

        # 3. Stable/Recovery Logic
        # If we were in Alert/Critical and temp is now low
        if self.current_state in [CPSState.ALERT, CPSState.CRITICAL] and temp < self.alert_temp:
            self.current_state = CPSState.STABLE
            return CPSState.STABLE, "RECOVERY: System cooling down to safe levels."

        # 4. Default Normal
        self.current_state = CPSState.NORMAL
        return CPSState.NORMAL, "System healthy: Stable temperature and performance."
