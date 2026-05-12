import argparse
import sys
import os
import datetime
from Code.real_time_detector import RealTimeDetector
from Code.model_training import train_thermal_pipeline
from src.ui.terminal_display import TerminalDisplay # Reusing UI from existing src for now
from src.storage.csv_handler import CSVHandler # Reusing Storage

def start_monitor(args):
    """Initializes and runs the live CPS monitoring dashboard."""
    detector = RealTimeDetector(use_ml=args.ml)
    display = TerminalDisplay()
    csv_handler = CSVHandler("Logs/system_events.csv") # Output to Logs folder

    def ui_update(metrics, state, message):
        # Callback for real-time visualization
        display.console.clear()
        display.console.print(display.create_dashboard(metrics, state, message))

    def log_update(metrics, state, message):
        # Callback for historical data storage
        label = 1 if state in [CPSState.ALERT, CPSState.CRITICAL] else 0
        csv_handler.write_row({
            "timestamp": str(datetime.datetime.now()),
            "Temperature": metrics["temperature"],
            "CPU_Usage": metrics["cpu_usage"],
            "GPU_Temp": metrics.get("gpu_temp", 0) if metrics.get("gpu_temp") is not None else 0,
            "Fan_Speed": metrics.get("fan_speed", 0),
            "Throttling": metrics.get("throttling", "NO"),
            "Disk_IO": metrics.get("disk_io_rate", 0),
            "State": state,
            "Label": label,
            "Message": message
        })

    detector.run(display_callback=ui_update)

def main():
    parser = argparse.ArgumentParser(description="CPS Health Monitoring System")
    subparsers = parser.add_subparsers(dest="command")

    # Monitor Command
    mon = subparsers.add_parser("monitor", help="Start real-time monitoring")
    mon.add_argument("--ml", action="store_true", help="Enable ML-based anomaly detection")

    # Train Command
    train = subparsers.add_parser("train", help="Train ML models")
    train.add_argument("--input", default="logs/history.csv", help="Training data CSV")

    # API Command (New Feature: Scalability)
    subparsers.add_parser("api", help="Start the remote health monitoring API server")

    args = parser.parse_args()

    if args.command == "monitor":
        start_monitor(args)
    elif args.command == "train":
        train_thermal_pipeline(args.input)
    elif args.command == "api":
        from Code.api_server import start_api_server
        start_api_server()
    else:
        parser.print_help()

if __name__ == "__main__":
    # Ensure relative imports work when running from root
    sys.path.append(os.getcwd())
    main()
