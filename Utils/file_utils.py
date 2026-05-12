import os
import shutil

def clear_logs(log_dir="Logs"):
    """Safely clears operational logs."""
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir)

def check_requirements():
    """Verifies that critical folders exist."""
    folders = ["Code", "Data", "Models", "Logs", "Reports"]
    for f in folders:
        if not os.path.exists(f):
            print(f"MISSING FOLDER: {f}")
            return False
    return True
