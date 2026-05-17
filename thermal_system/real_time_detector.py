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
    def __init__(self, model_path='Models/isolation_forest.joblib', use_ml=True):
        self.collector = DataCollector()
        self.validator = DataValidator()
        self.engineer = FeatureEngineer()
        self.model = HealthStateModel()
        self.mitigation = MitigationEngine() # NEW: Actuator
        
        self.use_ml = use_ml
        self.ml_model = None
        if use_ml:
            if os.path.exists(model_path):
                try:
                    self.ml_model = joblib.load(model_path)
                except Exception as e:
                    print(f"Warning: Could not load ML model: {e}")
                    self.use_ml = False
            else:
                # User-friendly warning: Provide guidance on how to train the model if it is missing
                print(f"Notice: ML model file '{model_path}' not found.")
                print("To enable Machine Learning anomaly detection, please train the model first using:")
                print("  python -m thermal_system.main train")
                print("Falling back to Rule-Based Anomaly Detection...")
                self.use_ml = False

    def notify(self, state, message):
        """Triggers desktop notifications for critical states."""
        if state in [CPSState.ALERT, CPSState.CRITICAL, CPSState.SUSTAINED]:
            try:
                notification.notify(
                    title=f"CPS {state} ALERT",
                    message=message,
                    app_name="ThermalMonitor",
                    timeout=5
                )
            except Exception:
                pass

    def run(self, display_callback=None, storage_callback=None):
        """
        The Main Monitoring Loop (1Hz).
        Implements the complete CPS loop: Sense -> Analyze -> Decide -> Actuate.
        """
        print("Starting Real-Time Thermal Anomaly Detection...")
        try:
            while True:
                # 1. SENSE: Hardware Metrology
                raw_metrics = self.collector.get_system_metrics()
                raw_temp = self.collector.get_temperature()
                raw_metrics['temperature'] = raw_temp

                # 2. VALIDATE: Data Integrity Layer
                validated_metrics = self.validator.validate(raw_metrics)

                # 3. FEATURE ENGINEERING: Extract Temporal Patterns
                engineered_features = self.engineer.extract_features(validated_metrics)
                
                # 4. INTELLIGENCE: Inference Layer
                anomaly_score = 0
                if self.use_ml and self.ml_model and engineered_features is not None:
                    # Prepare feature vector for ML
                    feature_vector = [
                        engineered_features['temperature'],
                        engineered_features['cpu_usage'],
                        engineered_features['temp_rolling_std'],
                        engineered_features['temp_gradient'],
                        engineered_features['load_to_temp_ratio']
                    ]
                    # IF returns -1 for anomalies
                    anomaly_score = self.ml_model.predict([feature_vector])[0]

                # 5. DECIDE: Health State Classification
                state, message = self.model.classify(validated_metrics, anomaly_score)

                # 6. ACTUATE: Automated Mitigation
                # If in CRITICAL/ALERT, let the mitigation engine decide if action is needed
                if state in [CPSState.ALERT, CPSState.CRITICAL, CPSState.SUSTAINED]:
                    mitigation_msg = self.mitigation.enforce_policy(state, validated_metrics)
                    if mitigation_msg:
                        message += f" | {mitigation_msg}"

                # 7. PREDICTION: Time to Critical (TTC)
                if 'temp_gradient' in engineered_features and engineered_features['temp_gradient'] > 0:
                    from .utils.config_manager import load_config
                    # Fetch sampling interval to convert change-per-sample to change-per-second
                    interval = load_config().get("monitoring", {}).get("sampling_interval", 5)
                    temp_rise_per_sec = engineered_features['temp_gradient'] / interval
                    
                    # Calculate accurate Time to Critical (TTC) in seconds
                    ttc = (85 - validated_metrics['temperature']) / temp_rise_per_sec
                    if ttc > 0 and ttc < 60:
                        message += f" | TTC: {ttc:.0f}s!"

                # 8. NOTIFICATION & CALLBACKS
                self.notify(state, message)
                
                if display_callback:
                    display_callback(engineered_features, state, message)
                
                if storage_callback:
                    storage_callback(engineered_features, state, message)

                from .utils.config_manager import load_config
                interval = load_config().get("monitoring", {}).get("sampling_interval", 5)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring suspended by user.")

if __name__ == "__main__":
    detector = RealTimeDetector()
    detector.run()
