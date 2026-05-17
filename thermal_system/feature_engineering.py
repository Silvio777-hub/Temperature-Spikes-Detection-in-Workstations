import pandas as pd
import numpy as np

class FeatureEngineer:
    """
    Data Processing Layer: Feature Engineering.
    Transforms raw metrics into meaningful features for the ML model.
    """
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.history = []

    def extract_features(self, current_metrics):
        """
        Calculates time-series features. 
        Renamed to 'extract_features' to match real_time_detector expectation.
        """
        self.history.append(current_metrics)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        df = pd.DataFrame(self.history)
        
        # We start with the validated metrics
        features = current_metrics.copy()
        
        # 1. Temperature Gradient (Slope)
        if len(df) > 1:
            features["temp_gradient"] = df["temperature"].diff().iloc[-1]
        else:
            features["temp_gradient"] = 0.0

        # 2. Temperature Volatility (Standard Deviation)
        features["temp_rolling_std"] = df["temperature"].std() if len(df) > 1 else 0.0

        # 3. Thermal Efficiency (Load to Temperature Ratio)
        cpu_load = max(current_metrics.get("cpu_usage", 1), 1.0)
        features["load_to_temp_ratio"] = current_metrics.get("temperature", 45) / cpu_load

        return features
