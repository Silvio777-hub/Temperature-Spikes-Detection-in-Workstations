import json
import os
import datetime
import time
from .utils.config_manager import load_config

class CPSState:
    """CPS Health States as defined in Section 5.2 of the Proposal."""
    NORMAL = "NORMAL"         # Stable temperature and performance
    ALERT = "ALERT"           # Elevated temperature or abnormal trends
    CRITICAL = "CRITICAL"     # Sustained overheating or unsafe conditions
    STABLE = "STABLE (RECOVERY)" # System cooling down after intervention
    SUSTAINED = "SUSTAINED HIGH" # NEW: Rule 3.3.iv compliance

class HealthStateModel:
    """
    Analytics Layer: Health Classification with State Persistence.
    Determines the CPS state based on rules, ML, and temporal patterns.
    """
    def __init__(self, state_file="Models/system_state.json"):
        config = load_config()
        self.thresholds = config.get("thresholds", {})
        self.critical_temp = self.thresholds.get("critical_temp", 85)
        self.alert_temp = self.thresholds.get("alert_temp", 75)
        self.sustained_temp = self.thresholds.get("sustained_temp", 70)
        self.sustained_duration = self.thresholds.get("sustained_duration", 300)
        
        self.state_file = state_file
        self.current_state = self.load_state()
        self.last_metrics = None
        
        # Sustained High tracking
        self.high_temp_start_time = None

    def save_state(self):
        """Saves current state to a JSON file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({"last_state": self.current_state, "timestamp": str(datetime.datetime.now())}, f)
        except Exception:
            pass

    def load_state(self):
        """Loads previous state from disk to maintain continuity."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f).get("last_state", CPSState.NORMAL)
            except Exception:
                return CPSState.NORMAL
        return CPSState.NORMAL

    def classify(self, metrics, anomaly_score):
        """
        Classifies the system state using rule-based and ML inputs.
        Implements Rule 3.3.iv: Sustained high temp detection.
        """
        temp = metrics.get("temperature", 0)
        now = time.time()

        # 0. Sustained High Tracking (Rule 3.3.iv)
        if temp >= self.sustained_temp:
            if self.high_temp_start_time is None:
                self.high_temp_start_time = now
            elif now - self.high_temp_start_time >= self.sustained_duration:
                self.current_state = CPSState.SUSTAINED
                return CPSState.SUSTAINED, f"RULE VIOLATION: Temperature sustained >{self.sustained_temp}°C for >{self.sustained_duration//60} minutes!"
        else:
            self.high_temp_start_time = None

        # 1. Thermal Inertia Check
        temp_delta = 0
        if self.last_metrics and "temperature" in self.last_metrics:
            temp_delta = temp - self.last_metrics["temperature"]
        self.last_metrics = metrics

        if temp_delta >= self.thresholds.get("rapid_rise_threshold", 5):
            self.current_state = CPSState.ALERT
            return CPSState.ALERT, f"PRE-EMPTIVE ALERT: Rapid Temperature Spike detected (+{temp_delta:.1f}°C)!"

        # 2. Critical State
        if temp >= self.critical_temp:
            self.current_state = CPSState.CRITICAL
            return CPSState.CRITICAL, "URGENT: Critical overheating threshold reached!"

        # 3. Alert State (Thresholds, ML, or Throttling)
        is_throttling = metrics.get("throttling", "NO") == "YES"
        if temp >= self.alert_temp or anomaly_score == -1 or is_throttling:
            self.current_state = CPSState.ALERT
            reason = "Anomaly detected by ML engine."
            if temp >= self.alert_temp:
                reason = f"Temperature ({temp}°C) exceeds Alert Threshold ({self.alert_temp}°C)."
            if is_throttling:
                reason = "Hardware is actively THROTTLING."
            return CPSState.ALERT, f"WARNING: {reason}"

        # 4. Stable/Recovery Logic
        if self.current_state in [CPSState.ALERT, CPSState.CRITICAL, CPSState.SUSTAINED] and temp < self.alert_temp:
            self.current_state = CPSState.STABLE
            return CPSState.STABLE, "RECOVERY: System cooling down to safe levels."

        self.current_state = CPSState.NORMAL
        return CPSState.NORMAL, "System healthy: Stable temperature and performance."
