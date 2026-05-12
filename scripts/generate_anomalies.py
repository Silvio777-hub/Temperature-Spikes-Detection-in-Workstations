import pandas as pd
import numpy as np
import os
import random

def generate_labeled_data(output_path="data/training/labeled_training_data.csv", samples=5000):
    """Generates a synthetic labeled dataset for training validation."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data = []
    for i in range(samples):
        is_anomaly = 1 if random.random() < 0.1 else 0
        
        if is_anomaly:
            # High temp, high usage, high rate
            temp = random.uniform(70, 95)
            cpu = random.uniform(80, 100)
            rate = random.uniform(2, 5)
        else:
            # Normal range
            temp = random.uniform(35, 55)
            cpu = random.uniform(5, 40)
            rate = random.uniform(-0.5, 0.5)
            
        data.append({
            "temperature": temp,
            "cpu_usage": cpu,
            "memory_usage": random.uniform(20, 80),
            "disk_io": random.uniform(1000, 50000),
            "temp_rate": rate,
            "temp_roll_mean": temp + random.uniform(-1, 1),
            "temp_roll_std": random.uniform(0.1, 2.0),
            "anomaly": is_anomaly
        })
        
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated {samples} labeled samples at {output_path}")

if __name__ == "__main__":
    generate_labeled_data()
