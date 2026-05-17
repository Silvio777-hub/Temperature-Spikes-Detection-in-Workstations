import psutil
import os
import time
from .utils.config_manager import load_config
from .state_model import CPSState

class MitigationEngine:
    """
    Control/Actuation Layer: Automated Mitigation.
    Responsible for taking physical action to protect the workstation hardware.
    """
    def __init__(self):
        self.config = load_config()
        self.whitelist = ["system", "idle", "explorer.exe", "svchost.exe", "python.exe", "winlogon.exe"]

    def enforce_policy(self, state, metrics):
        """
        Main entry point for the actuation layer.
        Implements different strategies based on state and config.
        """
        if not self.config.get("mitigation", {}).get("enabled", True):
            return "Mitigation layer disabled via config."

        # Fetch top processes for decision making
        from .data_collection import DataCollector
        collector = DataCollector()
        top_procs = collector.get_top_processes(count=1)
        
        if not top_procs:
            return None

        target = top_procs[0]
        pname = target.get('name', 'Unknown')
        
        # Security Check: Whitelist protection
        if pname.lower() in self.whitelist:
            return f"Actuation inhibited: {pname} is a protected system process."

        if state == CPSState.CRITICAL:
            # HARD MITIGATION: Terminate all instances
            return self._hard_mitigation(pname)
        elif state in [CPSState.ALERT, CPSState.SUSTAINED]:
            # SOFT MITIGATION: Reduce Priority of all instances
            return self._soft_mitigation(pname)
            
        return None

    def _soft_mitigation(self, process_name):
        """Reduces process priority of all matching processes to 'Below Normal' to decrease thermal load."""
        try:
            count = 0
            for proc in psutil.process_iter(['name']):
                try:
                    # Access process name safely, catching access denied / no such process exceptions
                    if proc.info['name'] == process_name:
                        if os.name == 'nt':
                            proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                        else:
                            proc.nice(10)
                        count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            if count > 0:
                return f"Soft Mitigation: Reduced priority of {count} instance(s) of {process_name}."
        except Exception as e:
            return f"Soft Mitigation Failed: {e}"
        return None

    def _hard_mitigation(self, process_name):
        """Forcefully terminates all instances of the process to protect the hardware."""
        try:
            count = 0
            for proc in psutil.process_iter(['name']):
                try:
                    # Access process name safely, catching access denied / no such process exceptions
                    if proc.info['name'] == process_name:
                        proc.terminate()
                        count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            if count > 0:
                return f"Hard Mitigation: Terminated {count} instance(s) of {process_name}."
        except Exception as e:
            return f"Hard Mitigation Failed: {e}"
        return "Process not found for hard mitigation."
