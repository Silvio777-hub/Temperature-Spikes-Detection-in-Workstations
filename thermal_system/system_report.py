import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from thermal_system.utils.csv_helper import read_csv_robust

def generate_health_report(log_csv="Logs/system_events.csv", output_dir="Reports"):
    """
    Automated Health Analytics: Generates a professional summary report of thermal trends.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(log_csv):
        print(f"Error: Log file {log_csv} not found.")
        return

    print(f"Generating CPS Health Report from {log_csv}...")
    try:
        df = read_csv_robust(log_csv)
        if df.empty:
            print("Notice: Log file is empty. Skipping report generation.")
            return
    except Exception as e:
        print(f"Error reading log file: {e}")
        return
        
    # Set style
    sns.set_theme(style="darkgrid")
    
    # 1. Statistical Summary
    summary = df.describe()
    summary.to_csv(os.path.join(output_dir, "statistical_summary.csv"))
    
    # 2. State Distribution (Pie Chart)
    if "State" in df.columns:
        plt.figure(figsize=(8, 8))
        state_counts = df["State"].value_counts()
        plt.pie(state_counts, labels=state_counts.index, autopct='%1.1f%%', colors=sns.color_palette("viridis"))
        plt.title("Workstation Health State Distribution")
        plt.savefig(os.path.join(output_dir, "health_states_pie.png"))
        plt.close()

    # 3. Combined Telemetry Plot (Temperature vs Load)
    plt.figure(figsize=(14, 7))
    ax = sns.lineplot(data=df, x=df.index, y="Temperature", color='red', label="Temperature (°C)")
    sns.lineplot(data=df, x=df.index, y="CPU_Usage", color='blue', alpha=0.3, label="CPU Load (%)")
    
    plt.axhline(y=75, color='orange', linestyle='--', label="Alert Limit (75°C)")
    plt.axhline(y=85, color='darkred', linestyle='--', label="Critical Limit (85°C)")
    
    plt.title("Workstation Thermal & Load Correlation")
    plt.xlabel("Time (Samples)")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "thermal_trends_detailed.png"))
    plt.close()
    
    # 4. Anomaly Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Metric Correlation Heatmap")
    plt.savefig(os.path.join(output_dir, "metric_correlation.png"))
    plt.close()

    print(f"✅ All forensic reports generated successfully in {output_dir}/")

if __name__ == "__main__":
    generate_health_report()
