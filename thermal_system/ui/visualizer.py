import pandas as pd
import matplotlib.pyplot as plt
import os
from thermal_system.utils.csv_helper import read_csv_robust

def plot_temperature(csv_path, output_path="plots/temperature_plot.png"):
    """
    Generates a static plot of temperature history.
    Supports casing-resilient column headers (e.g. Temperature/temperature, CPU_Usage/cpu_usage).
    """
    if not os.path.exists(csv_path):
        return False, "Data file not found."
        
    try:
        df = read_csv_robust(csv_path)
        if df.empty:
            return False, "Data file is empty."
            
        # Detect temperature column robustly
        temp_col = None
        for col in ['Temperature', 'temperature', 'TEMP', 'temp']:
            if col in df.columns:
                temp_col = col
                break
                
        # Detect CPU load column robustly
        cpu_col = None
        for col in ['CPU_Usage', 'cpu_usage', 'CPU', 'cpu']:
            if col in df.columns:
                cpu_col = col
                break
                
        if not temp_col:
            return False, "Temperature column not found in log CSV."

        plt.figure(figsize=(10, 6))
        
        # Plot CPU Temperature
        plt.plot(df[temp_col], label='CPU Temp (°C)', color='red')
        
        # Plot CPU Usage if present
        if cpu_col:
            plt.plot(df[cpu_col], label='CPU Usage (%)', color='blue', alpha=0.3)
            
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
