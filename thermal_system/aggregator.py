import requests
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
import os
from dotenv import load_dotenv

load_dotenv()
CONSOLE = Console()
API_KEY = os.getenv("API_KEY", "CPS_SECURE_TOKEN_2026")

# Global static node lists are deprecated in favor of dynamic configuration

def fetch_node_status(node):
    """Fetches health status from a specific node API."""
    try:
        headers = {"X-API-KEY": API_KEY}
        response = requests.get(f"{node['url']}/health", headers=headers, timeout=2)
        if response.status_code == 200:
            return response.json()
        return {"last_state": "AUTH_ERROR", "message": "Invalid API Key"}
    except Exception:
        return {"last_state": "OFFLINE", "message": "Connection failed"}

def generate_heatmap():
    """Generates a rich table representing the cluster status."""
    table = Table(title="CPS Multi-Node Health Aggregator (Heat Map)")
    table.add_column("Node Name", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Last Message", style="dim")
    table.add_column("Latency", justify="right")

    # Dynamically load the correct port from configuration
    try:
        from .utils.config_manager import load_config
        config = load_config()
        port = config.get("security", {}).get("port", 5000)
    except Exception:
        port = 5000

    dynamic_nodes = [
        {"name": "Local Workstation", "url": f"http://localhost:{port}"},
        # Add other dynamic nodes here
    ]

    for node in dynamic_nodes:
        start_time = time.time()
        status = fetch_node_status(node)
        latency = f"{(time.time() - start_time)*1000:.0f}ms"
        
        state = status.get("last_state", "UNKNOWN")
        
        # Color coding based on CPS state
        style = "green"
        if state == "CRITICAL": style = "bold red"
        elif state == "ALERT": style = "yellow"
        elif state == "OFFLINE": style = "dim red"

        table.add_row(
            node["name"],
            f"[{style}]{state}[/{style}]",
            status.get("message", "N/A"),
            latency
        )
    
    return table

def run_aggregator():
    """Main loop for the multi-node monitor."""
    CONSOLE.clear()
    with Live(generate_heatmap(), refresh_per_second=1) as live:
        while True:
            time.sleep(5)
            live.update(generate_heatmap())

if __name__ == "__main__":
    try:
        run_aggregator()
    except KeyboardInterrupt:
        CONSOLE.print("\n[bold blue]Aggregator stopped.[/bold blue]")
