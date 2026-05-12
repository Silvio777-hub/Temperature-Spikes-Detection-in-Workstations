import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
import json

def train_thermal_pipeline(input_csv, model_dir="Models"):
    """
    Analytics Layer: Model Training Pipeline.
    Develops and evaluates the Isolation Forest model for anomaly detection.
    """
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Load Collected Data
    print(f"Loading training data from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    # 2. Select Features (Aligned with Real-Time Detector)
    # Mapping CSV columns to model features
    features = ["Temperature", "CPU_Usage", "RAM_Usage", "Freq_MHz"]
    X = df[features].dropna()
    
    # 3. Data Scaling (Normalization)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Anomaly Detection Algorithm (Isolation Forest)
    print("Training Isolation Forest model...")
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05, # Expecting 5% anomalies in baseline
        random_state=42
    )
    model.fit(X_scaled)
    
    # 5. Serialization (Save Deliverables)
    model_path = os.path.join(model_dir, "temperature_spike_model.pkl")
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    meta_path = os.path.join(model_dir, "model_metadata.json")
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    metadata = {
        "features": features,
        "trained_at": str(pd.Timestamp.now()),
        "sample_count": len(X),
        "algorithm": "Isolation Forest"
    }
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Deliverables saved to {model_dir}/")
    return model

if __name__ == "__main__":
    import sys
    csv = sys.argv[1] if len(sys.argv) > 1 else "logs/history.csv"
    train_thermal_pipeline(csv)
