from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

class TerminalDisplay:
    """Manages the real-time Rich dashboard."""
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

    def create_dashboard(self, metrics, state, message):
        table = Table(title="CPS Workstation Thermal Telemetry", border_style="cyan")
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")
        
        table.add_row("CPU Temperature", f"{metrics.get('temperature', 0):.1f}°C")
        
        gpu_temp = metrics.get('gpu_temp')
        gpu_val = f"{gpu_temp:.1f}°C" if gpu_temp is not None else "N/A (Integrated)"
        table.add_row("GPU Temperature", gpu_val)

        table.add_row("CPU Usage", f"{metrics.get('cpu_usage', 0):.1f}%")
        table.add_row("RAM Usage", f"{metrics.get('memory_usage', 0):.1f}%")
        
        # Advanced Metrics
        fan = metrics.get('fan_speed', 0)
        table.add_row("Fan Speed", f"{fan} RPM" if fan > 0 else "N/A")
        
        throttle = metrics.get('throttling', 'NO')
        t_color = "red" if throttle == "YES" else "green"
        table.add_row("Throttling", f"[{t_color}]{throttle}[/]")
        
        table.add_row("Disk I/O", f"{metrics.get('disk_io_rate', 0):.2f} MB/s")
        table.add_row("System State", f"[{self._get_state_color(state)}]{state}[/]")
        
        return Panel(table, title=f"[bold white]CPS Alert: {message}[/]", border_style="blue")

    def _get_state_color(self, state):
        colors = {
            "NORMAL": "green",
            "ALERT": "yellow",
            "CRITICAL": "red",
            "STABLE (RECOVERY)": "cyan",
            "SPIKE": "orange",
            "ANOMALY (ML)": "magenta"
        }
        return colors.get(state, "white")
