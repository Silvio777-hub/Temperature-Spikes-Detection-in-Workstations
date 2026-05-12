import pandas as pd
import numpy as np

class FeatureEngineer:
    """
    Data Processing Layer: Feature Engineering.
    Transforms raw metrics into meaningful features like rate of change and thermal efficiency.
    """
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.history = []

    def transform(self, current_metrics):
        """
        Calculates time-series features based on a rolling window of history.
        """
        self.history.append(current_metrics)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        df = pd.DataFrame(self.history)
        
        features = current_metrics.copy()
        
        # 1. Temperature Rate of Change (Spike Intensity)
        if len(df) > 1:
            features["temp_rate"] = df["temperature"].diff().iloc[-1]
        else:
            features["temp_rate"] = 0.0

        # 2. Rolling Mean (Baseline Comparison)
        features["temp_roll_mean"] = df["temperature"].mean()

        # 3. Rolling Std (Volatility/Instability)
        features["temp_roll_std"] = df["temperature"].std() if len(df) > 1 else 0.0

        # 4. Thermal Efficiency (Ratio of Temperature to CPU Usage)
        # Low efficiency means high temp with low load (possible cooling failure)
        cpu_load = max(current_metrics["cpu_usage"], 1.0)
        features["thermal_efficiency"] = current_metrics["temperature"] / cpu_load

        return features
