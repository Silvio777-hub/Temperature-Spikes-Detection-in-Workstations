import time
import datetime
import os
import joblib
import numpy as np
from rich.live import Live
from plyer import notification  # New Feature: Desktop Notifications

# Import Modular CPS Layers
from .data_collection import DataCollector
from .data_validation import DataValidator
from .feature_engineering import FeatureEngineer
from .state_model import HealthStateModel, CPSState
from .mitigation import MitigationEngine # NEW: Actuation Layer

class RealTimeDetector:
    """
    Pipeline Integration Layer: Orchestrates the complete closed-loop monitoring system.
    NEW: Actuation (Mitigation) and Intelligence (Drift Detection)
    """
    def __init__(self, use_ml=True):
        self.collector = DataCollector()
        self.validator = DataValidator()
        self.engineer = FeatureEngineer()
        self.state_model = HealthStateModel()
        self.mitigation = MitigationEngine()
        self.use_ml = use_ml
        
        # Drift Tracking
        self.anomaly_history = []
        self.drift_threshold = 0.2 # If >20% anomalies consistently, model is drifting
        self.model = None
        self.scaler = None
        self.features_list = None
        if self.use_ml:
            self._load_models()

    def _load_models(self):
        """Loads trained Isolation Forest and Scaler from the Models directory."""
        m_path = "Models/temperature_spike_model.pkl"
        s_path = "Models/scaler.pkl"
        f_path = "Models/model_metadata.json"
        
        if os.path.exists(m_path):
            try:
                self.model = joblib.load(m_path)
                self.scaler = joblib.load(s_path)
                # In a real system, we'd load features from metadata.json
                print(f"DEBUG: ML Model loaded successfully from {m_path}")
            except Exception as e:
                print(f"ERROR: Failed to load ML model: {e}")

    def notify(self, state, message):
        """NEW FEATURE: Desktop Notifications for critical CPS events."""
        if state in [CPSState.ALERT, CPSState.CRITICAL]:
            try:
                notification.notify(
                    title=f"CPS {state} EVENT",
                    message=message,
                    app_name="ThermalDetector",
                    timeout=5
                )
            except Exception:
                pass

    def run(self, display_callback=None, storage_callback=None):
        """Main execution loop of the CPS Monitoring System."""
        try:
            while True:
                # 1. DATA COLLECTION
                raw_metrics = self.collector.get_system_metrics()
                raw_metrics["temperature"] = self.collector.get_temperature()
                
                # 2. DATA VALIDATION
                valid_metrics = self.validator.validate_metrics(raw_metrics)
                
                # 3. FEATURE ENGINEERING
                engineered_features = self.engineer.transform(valid_metrics)
                
                # 4. ML ANALYSIS (Anomaly Detection)
                anomaly_score = 1 # Default Normal
                if self.model and self.scaler:
                    try:
                        # Prepare input for model (Temperature, CPU, RAM, Freq)
                        input_data = np.array([[
                            engineered_features["temperature"],
                            engineered_features["cpu_usage"],
                            engineered_features["memory_usage"],
                            engineered_features["freq_mhz"]
                        ]])
                        X_scaled = self.scaler.transform(input_data)
                        anomaly_score = self.model.predict(X_scaled)[0]
                    except Exception:
                        pass

                # 5. HEALTH CLASSIFICATION
                state, message = self.state_model.classify(valid_metrics, anomaly_score)
                self.state_model.save_state() # PERSISTENCE: Save state to Models/system_state.json
                
                # 6. DRIFT DETECTION (Intelligence Layer)
                if self.use_ml:
                    self.anomaly_history.append(1 if anomaly_score == -1 else 0)
                    if len(self.anomaly_history) > 50: # Check last 50 samples
                        self.anomaly_history.pop(0)
                        drift_rate = sum(self.anomaly_history) / len(self.anomaly_history)
                        if drift_rate > self.drift_threshold:
                            message += " | [DRIFT] Model baseline may be outdated."

                # 7. ROOT CAUSE ANALYSIS
                top_procs = []
                if state != CPSState.NORMAL:
                    top_procs = self.collector.get_top_processes()
                    proc_names = ", ".join([p['name'] for p in top_procs])
                    message += f" | Likely causes: {proc_names}"

                # 8. AUTOMATED MITIGATION (Actuation Layer)
                mitigation_result = self.mitigation.mitigate(state, top_procs)
                if "COMPLETE" in mitigation_result:
                    message += f" | {mitigation_result}"

                # 9. NOTIFICATION & CALLBACKS
                self.notify(state, message)
                
                if display_callback:
                    display_callback(engineered_features, state, message)
                
                if storage_callback:
                    storage_callback(engineered_features, state, message)

                time.sleep(2)
        except KeyboardInterrupt:
            print("\nMonitoring suspended by user.")

if __name__ == "__main__":
    detector = RealTimeDetector()
    detector.run()
