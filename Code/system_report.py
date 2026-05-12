import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_health_report(log_csv="logs/history.csv", output_dir="Reports"):
    """
    NEW FEATURE: Automated Health Analytics.
    Generates a summary report of thermal trends and health state distribution.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(log_csv):
        print(f"Error: Log file {log_csv} not found.")
        return

    print(f"Generating CPS Health Report from {log_csv}...")
    df = pd.read_csv(log_csv)
    
    # 1. Summary Statistics
    summary = df.describe()
    summary.to_csv(os.path.join(output_dir, "statistical_summary.csv"))
    
    # 2. State Distribution
    if "State" in df.columns:
        state_counts = df["State"].value_counts()
        plt.figure(figsize=(10, 6))
        state_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title("CPS Health State Distribution")
        plt.savefig(os.path.join(output_dir, "health_states_pie.png"))
        print(f"Report saved: {output_dir}/health_states_pie.png")

    # 3. Thermal Trend Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df["Temperature"], label="CPU Temp (°C)", color='red')
    plt.axhline(y=80, color='orange', linestyle='--', label="Alert Threshold")
    plt.title("Workstation Thermal Trends")
    plt.xlabel("Samples")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "thermal_trends.png"))
    
    print(f"All reports generated in {output_dir}/")

if __name__ == "__main__":
    generate_health_report()
