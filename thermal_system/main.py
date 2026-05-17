import sys
import os

# Add the project root to sys.path to allow 'thermal_system' package imports when running directly
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import argparse
import datetime
import time
import pandas as pd
from thermal_system.real_time_detector import RealTimeDetector
from thermal_system.model_training import train_thermal_pipeline
from thermal_system.ui.terminal_display import TerminalDisplay
from thermal_system.storage.csv_handler import CSVHandler
from thermal_system.state_model import CPSState
from thermal_system.utils.config_manager import load_config, update_config

def start_monitor(args):
    """Initializes and runs the live CPS monitoring dashboard."""
    config = load_config()
    sampling_interval = config.get("monitoring", {}).get("sampling_interval", 5)
    
    detector = RealTimeDetector(use_ml=args.ml)
    display = TerminalDisplay()
    csv_handler = CSVHandler("Logs/system_events.csv")

    def ui_update(metrics, state, message):
        display.console.clear()
        display.console.print(display.create_dashboard(metrics, state, message))

    def log_update(metrics, state, message):
        label = 1 if state in [CPSState.ALERT, CPSState.CRITICAL, CPSState.SUSTAINED] else 0
        csv_handler.write_row({
            "timestamp": str(datetime.datetime.now()),
            "Temperature": metrics["temperature"],
            "CPU_Usage": metrics["cpu_usage"],
            "RAM_Usage": metrics.get("memory_usage", 0),
            "Freq_MHz": metrics.get("freq_mhz", 0),
            "GPU_Temp": metrics.get("gpu_temp", 0) if metrics.get("gpu_temp") is not None else 0,
            "Fan_Speed": metrics.get("fan_speed", 0),
            "Throttling": metrics.get("throttling", "NO"),
            "Disk_IO": metrics.get("disk_io_rate", 0),
            "State": state,
            "Label": label,
            "Message": message
        })

    # Run with configurable interval
    detector.run(display_callback=ui_update, storage_callback=log_update)

def show_status():
    """One-shot status report (CLI Subcommand: status)."""
    from thermal_system.data_collection import DataCollector
    collector = DataCollector()
    metrics = collector.get_system_metrics()
    metrics["temperature"] = collector.get_temperature()
    
    print("\n--- CPS WORKSTATION STATUS ---")
    print(f"Timestamp: {datetime.datetime.now()}")
    print(f"CPU Temp:  {metrics['temperature']:.1f}°C")
    print(f"CPU Load:  {metrics['cpu_usage']:.1f}%")
    print(f"RAM Usage: {metrics['memory_usage']:.1f}%")
    
    gpu_temp = metrics.get('gpu_temp')
    gpu_temp_str = f"{gpu_temp:.1f}" if gpu_temp is not None else "N/A"
    print(f"GPU Temp:  {gpu_temp_str}°C")
    print(f"Throttling: {metrics['throttling']}")
    print("------------------------------\n")

def show_history(limit=10):
    """Shows recent log entries (CLI Subcommand: history)."""
    log_file = "Logs/system_events.csv"
    if os.path.exists(log_file):
        from thermal_system.utils.csv_helper import read_csv_robust
        df = read_csv_robust(log_file)
        print(f"\n--- LAST {limit} CPS EVENTS ---")
        print(df.tail(limit)[["timestamp", "Temperature", "CPU_Usage", "State", "Message"]])
        print("------------------------------\n")
    else:
        print("No history logs found.")

def manage_config(args):
    """Manages configuration settings (CLI Subcommand: config)."""
    if args.action == "view":
        config = load_config()
        import yaml
        print("\n--- CURRENT CONFIGURATION ---")
        print(yaml.dump(config, default_flow_style=False))
        print("-----------------------------\n")
    elif args.action == "set":
        if update_config(args.category, args.key, args.value):
            print(f"Successfully updated {args.category}.{args.key} to {args.value}")
        else:
            print(f"Failed to update config. Key '{args.key}' in category '{args.category}' not found.")

def main():
    parser = argparse.ArgumentParser(description="CPS Health Monitoring System")
    subparsers = parser.add_subparsers(dest="command")

    # Monitor Command
    mon = subparsers.add_parser("monitor", help="Start real-time monitoring")
    mon.add_argument("--ml", action="store_true", help="Enable ML-based anomaly detection")

    # Status Command (NEW)
    subparsers.add_parser("status", help="Show one-shot system status")

    # History Command (NEW)
    hist = subparsers.add_parser("history", help="Show recent system events")
    hist.add_argument("--limit", type=int, default=10, help="Number of rows to show")

    # Config Command (NEW)
    conf = subparsers.add_parser("config", help="Manage system configuration")
    conf_subs = conf.add_subparsers(dest="action")
    conf_subs.add_parser("view", help="View current settings")
    conf_set = conf_subs.add_parser("set", help="Update a setting")
    conf_set.add_argument("category", help="Config category (e.g., thresholds)")
    conf_set.add_argument("key", help="Config key (e.g., critical_temp)")
    conf_set.add_argument("value", help="New value")

    # Train Command
    # Fixed: Corrected default file to Logs/system_events.csv to prevent FileNotFoundError
    train = subparsers.add_parser("train", help="Train ML models")
    train.add_argument("--input", default="Logs/system_events.csv", help="Training data CSV")

    # Diagnose Command
    diag = subparsers.add_parser("diagnose", help="Generate a health diagnostic report")
    diag.add_argument("--input", default="Logs/system_events.csv", help="Log file to analyze")

    # API Command (NEW)
    # Starts the FastAPI/Uvicorn server for remote CPS monitoring
    subparsers.add_parser("api", help="Start the remote monitoring API server")

    # Aggregator Command (NEW)
    # Starts the multi-node clustering status console heat map
    subparsers.add_parser("aggregator", help="Start the multi-node health aggregator dashboard")

    args = parser.parse_args()

    if args.command == "monitor":
        start_monitor(args)
    elif args.command == "status":
        show_status()
    elif args.command == "history":
        show_history(args.limit)
    elif args.command == "config":
        manage_config(args)
    elif args.command == "train":
        train_thermal_pipeline(args.input)
    elif args.command == "diagnose":
        from thermal_system.system_report import generate_health_report
        generate_health_report(args.input)
    elif args.command == "api":
        # Import and run the FastAPI server dynamically
        from thermal_system.api_server import start_api_server
        start_api_server()
    elif args.command == "aggregator":
        # Import and run the Rich-based multi-node console dashboard dynamically
        from thermal_system.aggregator import run_aggregator
        run_aggregator()
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    main()
