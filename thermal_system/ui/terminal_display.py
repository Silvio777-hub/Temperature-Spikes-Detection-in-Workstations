import sys

# Reconfigure stdout and stderr to UTF-8 to prevent UnicodeEncodeError on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

class TerminalDisplay:
    """
    Premium Dashboard Layer: Visualizes CPS telemetry with a professional ASCII interface.
    Updated Header with Panel Lining: TSD in Workstations
    """
    def __init__(self):
        self.console = Console()
        self.banner_text = r"""
  _______   _____   _____  
 |__   __| / ____| |  __ \ 
    | |   | (___   | |  | |
    | |    \___ \  | |  | |
    | |    ____) | | |__| |
    |_|   |_____/  |_____/ 
                           
    TSD IN WORKSTATIONS
 >>> Insightful Anomaly Detection <<<
        """

    def create_dashboard(self, metrics, state, message):
        # 1. Header (ASCII Banner wrapped in a Panel for "Good Lining")
        banner_content = Text(self.banner_text, style="cyan bold")
        header_panel = Panel(
            Align.center(banner_content),
            border_style="bright_blue",
            box=box.DOUBLE # Using DOUBLE box for a more premium lining
        )
        
        # 2. Telemetry Table
        table = Table(box=None, expand=True)
        table.add_column("METRIC", style="bold white", width=25)
        table.add_column("VALUE", justify="left", width=25)
        table.add_column("STATUS", justify="center", width=20)

        # CPU Row
        cpu_temp = metrics.get('temperature', 0)
        cpu_color = "red" if cpu_temp > 85 else "yellow" if cpu_temp > 70 else "green"
        table.add_row("CPU Temperature", f"{cpu_temp:.1f}°C", f"[{cpu_color}]●[/]")

        # GPU Row
        gpu_temp = metrics.get('gpu_temp')
        gpu_val = f"{gpu_temp:.1f}°C" if gpu_temp is not None else "N/A"
        gpu_color = "red" if gpu_temp and gpu_temp > 85 else ("yellow" if gpu_temp and gpu_temp > 70 else ("green" if gpu_temp is not None else "grey50"))
        gpu_dot = f"[{gpu_color}]●[/]" if gpu_temp is not None else "[grey50]●[/]"
        table.add_row("GPU Temperature", gpu_val, gpu_dot)

        # Usage Row
        table.add_row("System Load", f"{metrics.get('cpu_usage', 0):.1f}%", "")
        table.add_row("Memory Usage", f"{metrics.get('memory_usage', 0):.1f}%", "")
        
        # Fan & Throttling
        fan = metrics.get('fan_speed', 0)
        import platform
        if fan > 0:
            fan_label = f"~{fan} RPM (est.)" if platform.system() == "Windows" else f"{fan} RPM"
        else:
            fan_label = "N/A"
        table.add_row("Fan Speed", fan_label, "")
        
        throttle = metrics.get('throttling', 'NO')
        t_color = "red" if throttle == "YES" else "green"
        table.add_row("Thermal Throttling", f"[{t_color}]{throttle}[/]", "")

        # 3. State & Message Panel
        state_color = self._get_state_color(state)
        state_display = Panel(
            Align.center(f"[bold {state_color}]{state}[/]\n[white]{message}[/]"),
            title="System Health State",
            border_style=state_color
        )

        # 4. Final Assembly: Use Group instead of Layout to dynamically size panels
        # without strict height limitations or truncation in smaller consoles.
        return Group(
            header_panel,
            Panel(table, title="Live Telemetry", border_style="cyan"),
            state_display
        )

    def _get_state_color(self, state):
        colors = {
            "NORMAL": "green",
            "ALERT": "yellow",
            "CRITICAL": "red",
            "SUSTAINED HIGH": "bright_red",
            "STABLE (RECOVERY)": "cyan",
        }
        return colors.get(state, "white")
