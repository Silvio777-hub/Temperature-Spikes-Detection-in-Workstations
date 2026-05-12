import wmi
import pythoncom
import threading
import psutil
from .base_collector import BaseCollector

class WindowsCollector(BaseCollector):
    def __init__(self):
        self._thread_local = threading.local()

    def _get_wmi(self, namespace="root\\wmi"):
        attr_name = f"wmi_{namespace.replace('\\', '_')}"
        if not hasattr(self._thread_local, attr_name):
            try:
                pythoncom.CoInitialize()
                setattr(self._thread_local, attr_name, wmi.WMI(namespace=namespace))
            except Exception:
                setattr(self._thread_local, attr_name, None)
        return getattr(self._thread_local, attr_name)

    def get_temperature(self):
        w = self._get_wmi("root\\wmi")
        if w:
            try:
                temps = w.MSAcpi_ThermalZoneTemperature()
                if temps:
                    return (temps[0].CurrentTemperature / 10.0) - 273.15
            except Exception:
                pass
        return None

    def get_system_metrics(self):
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_io": psutil.disk_io_counters().read_bytes + psutil.disk_io_counters().write_bytes if psutil.disk_io_counters() else 0
        }
