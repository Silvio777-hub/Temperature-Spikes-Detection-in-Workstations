import yaml
import os

CONFIG_PATH = "config.yaml"

def load_config():
    """Loads the YAML configuration file."""
    if not os.path.exists(CONFIG_PATH):
        # Return default structure if file missing
        return {
            "monitoring": {"sampling_interval": 5, "history_buffer_size": 30},
            "thresholds": {"critical_temp": 85, "alert_temp": 75, "sustained_temp": 70, "sustained_duration": 300},
            "mitigation": {"enabled": True},
            "security": {"api_key": "default-key", "port": 5000}
        }
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def save_config(config):
    """Saves the configuration dictionary to the YAML file."""
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def update_config(category, key, value):
    """Updates a specific configuration value."""
    config = load_config()
    if category in config and key in config[category]:
        # Try to cast value to appropriate type
        current_val = config[category][key]
        if isinstance(current_val, (int, float, bool)):
            if isinstance(current_val, bool):
                value = str(value).lower() == 'true'
            elif isinstance(current_val, int):
                value = int(value)
            elif isinstance(current_val, float):
                value = float(value)
            
        config[category][key] = value
        save_config(config)
        return True
    return False
