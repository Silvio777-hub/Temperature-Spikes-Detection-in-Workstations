import time
import datetime
from src.collector.windows_collector import WindowsCollector
from src.ui.terminal_display import TerminalDisplay
from src.storage.csv_handler import CSVHandler
from src.utils.config_manager import ConfigManager
from rich.live import Live
import os
import joblib
import numpy as np

def run_monitoring_loop(use_ml=False):
    config = ConfigManager()
    collector = WindowsCollector()
    display = TerminalDisplay()
    
    log_path = config.get_nested("logging", "path", default="logs/history.csv")
    csv_handler = CSVHandler(log_path)
    
    interval = config.get_nested("monitoring", "interval", default=2)
    
    # Load ML model if requested
    model = None
    scaler = None
    features = None
    if use_ml:
        model_path = "data/models/isolation_forest.pkl"
        scaler_path = "data/models/scaler.pkl"
        features_path = "data/models/feature_columns.pkl"
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                model = joblib.load(model_path)
                scaler = joblib.load(scaler_path)
                features = joblib.load(features_path)
                print(f"Loaded ML model from {model_path}")
            except Exception as e:
                print(f"Failed to load ML model: {e}")
        else:
            print("ML model files not found. Run 'python -m src.main train' first.")

    with Live(display.create_dashboard({}, "STARTING", "Initializing..."), console=display.console, refresh_per_second=1) as live:
        try:
            while True:
                temp = collector.get_temperature()
                system_metrics = collector.get_system_metrics()
                
                metrics = {
                    "temperature": temp or 0,
                    "cpu_usage": system_metrics.get("cpu_usage", 0),
                    "memory_usage": system_metrics.get("memory_usage", 0),
                    "disk_io": system_metrics.get("disk_io", 0)
                }
                
                state = "NORMAL"
                message = "System healthy."
                
                # ML Prediction
                if model and scaler and features:
                    try:
                        # Map metrics to expected features
                        column_map = {
                            "Temperature": metrics["temperature"],
                            "CPU_Usage": metrics["cpu_usage"],
                            "RAM_Usage": metrics["memory_usage"],
                            "Freq_MHz": 2500 # Default/Proxy if not available
                        }
                        
                        input_data = []
                        for col in features:
                            input_data.append(column_map.get(col, 0))
                        
                        X = np.array([input_data])
                        X_scaled = scaler.transform(X)
                        pred = model.predict(X_scaled)
                        
                        if pred[0] == -1:
                            state = "ANOMALY (ML)"
                            message = "ML Detection: Unusual thermal pattern observed."
                    except Exception:
                        pass

                # Update UI
                live.update(display.create_dashboard(metrics, state, message))
                
                # Save to CSV (Mapping to CSV format)
                row = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Temperature": f"{metrics['temperature']:.2f}",
                    "GPU_Temp": "0.00",
                    "CPU_Usage": f"{metrics['cpu_usage']:.1f}",
                    "Freq_MHz": "2500",
                    "Throttling": "NO",
                    "RAM_Usage": f"{metrics['memory_usage']:.1f}",
                    "State": state,
                    "Message": message
                }
                csv_handler.write_row(row)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    run_monitoring_loop()
