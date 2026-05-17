import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
import json
from .feature_engineering import FeatureEngineer
from thermal_system.utils.csv_helper import read_csv_robust

def train_thermal_pipeline(input_csv, model_path="Models/isolation_forest.joblib"):
    """
    Intelligence Layer: Model Training.
    Learns normal workstation behavior using Isolation Forest.
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    if not os.path.exists(input_csv):
        print(f"Error: Training data {input_csv} not found.")
        return
        
    print(f"Training intelligence engine from {input_csv}...")
    df = read_csv_robust(input_csv)
    
    # 1. Feature Engineering (Simulate the real-time pipeline)
    engineer = FeatureEngineer(window_size=5)
    processed_data = []
    
    # We iterate and apply the same engineering as the live detector
    for _, row in df.iterrows():
        # Map CSV columns to internal metrics format
        metrics = {
            "temperature": row["Temperature"],
            "cpu_usage": row["CPU_Usage"],
            "memory_usage": row.get("RAM_Usage", 0)
        }
        features = engineer.extract_features(metrics)
        processed_data.append([
            features["temperature"],
            features["cpu_usage"],
            features["temp_rolling_std"],
            features["temp_gradient"],
            features["load_to_temp_ratio"]
        ])
        
    X = np.array(processed_data)
    
    # 2. Train Isolation Forest
    # contamination=0.01 means we assume 1% of baseline data might be spikes
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(X)
    
    # 3. Save
    joblib.dump(model, model_path)
    
    # Metadata for transparency (XAI)
    meta_path = model_path.replace(".joblib", "_meta.json")
    with open(meta_path, 'w') as f:
        json.dump({
            "features": ["temp", "cpu", "std", "gradient", "efficiency"],
            "samples": len(X),
            "timestamp": str(pd.Timestamp.now())
        }, f)
        
    print(f"✅ Training Complete: Model saved to {model_path}")

if __name__ == "__main__":
    train_thermal_pipeline("Logs/system_events.csv")
