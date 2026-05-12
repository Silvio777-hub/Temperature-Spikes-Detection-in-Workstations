import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="tempmon - Workstation Thermal Monitoring")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status
    subparsers.add_parser("status", help="Show current thermal snapshot")
    
    # Monitor
    monitor_parser = subparsers.add_parser("monitor", help="Start real-time monitoring dashboard")
    monitor_parser.add_argument("--record", help="Record data to specified CSV path")
    monitor_parser.add_argument("--use-ml", action="store_true", help="Enable ML-based anomaly detection")
    
    # Train
    train_parser = subparsers.add_parser("train", help="Train the anomaly detection model")
    train_parser.add_argument("--input", default="logs/history.csv", help="Input CSV data")
    
    # History
    subparsers.add_parser("history", help="Show past thermal alerts")
    
    # Diagnose
    subparsers.add_parser("diagnose", help="Run a quick thermal health check")

    # Stress
    stress_parser = subparsers.add_parser("stress", help="Generate synthetic thermal load")
    stress_parser.add_argument("--duration", type=int, default=60, help="Stress duration in seconds")
    stress_parser.add_argument("--cores", type=int, default=None, help="Number of cores to stress")
    
    return parser
