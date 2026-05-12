import psutil
import os
import time

class MitigationEngine:
    """
    Control/Actuation Layer: Automated Mitigation.
    Responsible for taking physical action to protect the workstation hardware.
    """
    def __init__(self, safety_enabled=True):
        self.safety_enabled = safety_enabled

    def mitigate(self, state, top_processes):
        """
        Executes intervention strategies based on the CPS Health State.
        """
        if not self.safety_enabled:
            return "Mitigation disabled by safety switch."

        if state == "CRITICAL":
            # Strategy: Kill the top CPU consumer to immediately drop temperature
            if top_processes:
                target = top_processes[0]
                return self._terminate_process(target['name'])
        
        elif state == "ALERT":
            # Strategy: Informative warning (Passive mitigation)
            return "Alert state: Monitoring for further escalation."
            
        return "No mitigation required."

    def _terminate_process(self, process_name):
        """NEW FEATURE: Actuation - Forcefully stops a dangerous process."""
        try:
            # We avoid killing critical system processes for safety
            protected_processes = ["system", "idle", "explorer.exe", "svchost.exe", "python.exe"]
            if process_name.lower() in protected_processes:
                return f"Mitigation Skipped: {process_name} is a protected system process."

            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process_name:
                    proc.terminate()
                    return f"ACTUATION COMPLETE: Terminated {process_name} to prevent overheating."
        except Exception as e:
            return f"ACTUATION FAILED: Could not terminate {process_name} ({e})"
        return "Process not found for termination."
