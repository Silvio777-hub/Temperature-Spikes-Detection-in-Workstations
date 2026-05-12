import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import joblib
import os
import yaml

def load_config(path="config/config.yaml"):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def train_thermal_model(input_csv, model_dir="data/models"):
    config = load_config()
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Load Data
    df = pd.read_csv(input_csv)
    
    # 2. Select Features (As per blueprint 'Best Feature Set')
    # 2. Select Features based on actual CSV column names
    # Map expected feature names to CSV columns
    column_map = {
        "temperature": "Temperature",
        "cpu_usage": "CPU_Usage",
        "memory_usage": "RAM_Usage",
        "disk_io": "Freq_MHz"  # Use CPU frequency as a proxy for disk I/O if needed
    }
    features = []
    for key, col in column_map.items():
        if col in df.columns:
            features.append(col)
    # Add engineered features if they exist
    for col in ["temp_rate", "temp_roll_mean", "temp_roll_std", "thermal_efficiency"]:
        if col in df.columns:
            features.append(col)
    
    # Add engineered features if they exist
    for col in ['temp_rate', 'temp_roll_mean', 'temp_roll_std', 'thermal_efficiency']:
        if col in df.columns:
            features.append(col)
            
    X = df[features].dropna()
    
    # 3. Scaling
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Training
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(X_scaled)
    
    # 5. Saving (Blueprint Requirements)
    joblib.dump(model, os.path.join(model_dir, "isolation_forest.pkl"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
    joblib.dump(features, os.path.join(model_dir, "feature_columns.pkl"))
    
    print(f"Model, Scaler, and Features saved to {model_dir}")
    return model, scaler, features

if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "logs/history.csv"
    train_thermal_model(csv_path)
