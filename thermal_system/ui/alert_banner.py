from rich.console import Console
from rich.panel import Panel
from rich.align import Align

class AlertBanner:
    """Displays prominent ASCII banners for critical alerts."""
    def __init__(self):
        self.console = Console()

    def show_alert(self, state, message):
        if state in ["EMERGENCY", "SPIKE"]:
            banner_text = f"!!! {state} DETECTED !!!\n{message}"
            panel = Panel(
                Align.center(f"[bold white on red]{banner_text}[/]"),
                border_style="bold red",
                padding=(1, 2)
            )
            self.console.print(panel)
