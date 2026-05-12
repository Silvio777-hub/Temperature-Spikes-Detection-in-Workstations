import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_temperature(csv_path, output_path="plots/temperature_plot.png"):
    """Generates a static plot of temperature history."""
    if not os.path.exists(csv_path):
        return False, "Data file not found."
        
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            return False, "Data file is empty."
            
        plt.figure(figsize=(10, 6))
        plt.plot(df['temperature'], label='CPU Temp (°C)', color='red')
        if 'cpu_usage' in df.columns:
            plt.plot(df['cpu_usage'], label='CPU Usage (%)', color='blue', alpha=0.3)
            
        plt.title("Workstation Thermal History")
        plt.xlabel("Samples")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        return True, output_path
    except Exception as e:
        return False, str(e)
