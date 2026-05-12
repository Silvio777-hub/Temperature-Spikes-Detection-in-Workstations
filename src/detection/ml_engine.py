import joblib
import pandas as pd
import os

class MLEngine:
    """Handles anomaly detection using pre-trained Isolation Forest."""
    def __init__(self, model_path="data/models/isolation_forest.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                data = joblib.load(self.model_path)
                self.model = data.get('model')
                self.scaler = data.get('scaler')
            except Exception:
                pass

    def predict(self, feature_dict):
        if self.model is None or self.scaler is None:
            return 0, 0.0 # Not loaded
            
        try:
            df = pd.DataFrame([feature_dict])
            # Ensure columns match training (simplified for demo)
            cols = ['temperature', 'cpu_usage', 'temp_rate', 'temp_roll_mean', 'temp_roll_std']
            X = df[cols]
            X_scaled = self.scaler.transform(X)
            
            prediction = self.model.predict(X_scaled)
            score = self.model.decision_function(X_scaled)
            
            # Isolation Forest: -1 is anomaly, 1 is normal
            is_anomaly = 1 if prediction[0] == -1 else 0
            return is_anomaly, float(score[0])
        except Exception:
            return 0, 0.0
