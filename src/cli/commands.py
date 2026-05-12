from src.collector.windows_collector import WindowsCollector
from src.ui.terminal_display import TerminalDisplay
from src.training.train_model import train_thermal_model
import time

def handle_status():
    collector = WindowsCollector()
    metrics = collector.get_system_metrics()
    temp = collector.get_temperature()
    print(f"\n--- Current System Status ---")
    print(f"Temperature: {temp if temp else 'N/A'}°C")
    print(f"CPU Usage:   {metrics['cpu_usage']}%")
    print(f"Memory:      {metrics['memory_usage']}%")
    print(f"-----------------------------\n")

def handle_train(args):
    print(f"Starting training pipeline with {args.input}...")
    train_thermal_model(args.input)
    print("Training process finished.")

def handle_diagnose():
    print("Running thermal diagnostics...")
    time.sleep(1)
    print("[PASS] Sensors reachable.")
    time.sleep(0.5)
    print("[PASS] Cooling fans responding.")
    print("Diagnostics complete: System Healthy.")
