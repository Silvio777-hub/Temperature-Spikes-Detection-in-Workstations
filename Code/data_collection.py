import wmi
import pythoncom
import threading
import psutil
import os
import platform

class DataCollector:
    """
    Data Collection Layer: Physical sensors and Software metrics.
    NEW: OS Portability - Automatically detects platform and uses appropriate sensors.
    """
    def __init__(self):
        self.os_type = platform.system()
        self._thread_local = threading.local()

    def _get_wmi(self, namespace="root\\wmi"):
        """Initializes WMI connection for the current thread."""
        attr_name = f"wmi_{namespace.replace('\\', '_')}"
        if not hasattr(self._thread_local, attr_name):
            try:
                import pythoncom
                import wmi
                pythoncom.CoInitialize()
                setattr(self._thread_local, attr_name, wmi.WMI(namespace=namespace))
            except Exception:
                setattr(self._thread_local, attr_name, None)
        return getattr(self._thread_local, attr_name)

    def get_temperature(self):
        """Cross-platform temperature retrieval."""
        if self.os_type == "Windows":
            return self._get_windows_temp()
        else:
            return self._get_linux_temp()

    def _get_windows_temp(self):
        """Retrieves CPU temperature via WMI for Windows systems."""
        w = self._get_wmi("root\\wmi")
        if w:
            try:
                temps = w.MSAcpi_ThermalZoneTemperature()
                if temps:
                    return (temps[0].CurrentTemperature / 10.0) - 273.15
            except Exception:
                pass
        return None

    def _get_linux_temp(self):
        """Retrieves CPU temperature via psutil sensors for Linux systems."""
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return temps['coretemp'][0].current
            elif 'cpu_thermal' in temps:
                return temps['cpu_thermal'][0].current
        except Exception:
            pass
        return None

    def get_gpu_temperature(self):
        """Retrieves NVIDIA GPU temperature using py3nvml."""
        try:
            from py3nvml import py3nvml as nvml
            nvml.nvmlInit()
            handle = nvml.nvmlDeviceGetHandleByIndex(0)
            temp = nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU)
            nvml.nvmlShutdown()
            return temp
        except Exception:
            return None

    def get_core_temperatures(self):
        """Retrieves individual CPU core temperatures if supported by the OS/Drivers."""
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return [t.current for t in temps['coretemp']]
            return []
        except Exception:
            return []

    def get_fan_speed(self):
        """Retrieves fan speeds in RPM if sensors are available."""
        try:
            fans = psutil.sensors_fans()
            if fans:
                # Return the first active fan speed
                for name, entries in fans.items():
                    return entries[0].current
            return 0
        except Exception:
            return 0

    def get_power_consumption(self):
        """Best-effort CPU power estimation in Watts."""
        try:
            # On some systems, WMI Win32_PerfFormattedData_Counters_ThermalZoneInformation 
            # or custom hardware monitors provide this.
            # Defaulting to 0 if hardware-specific API is not found.
            return 0.0 
        except Exception:
            return 0.0

    def check_throttling(self):
        """Detects if CPU frequency is being limited due to thermal conditions."""
        try:
            freq = psutil.cpu_freq()
            if freq and freq.max > 0:
                # If current frequency is < 50% of max while usage is > 80%, it's likely throttling
                if (freq.current / freq.max) < 0.5 and psutil.cpu_percent() > 80:
                    return "YES"
            return "NO"
        except Exception:
            return "UNKNOWN"

    def get_system_metrics(self):
        """Collects granular software and hardware metrics including Power and Fans."""
        try:
            core_temps = self.get_core_temperatures()
            disk_io = psutil.disk_io_counters()
            return {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                "disk_usage": psutil.disk_usage('/').percent,
                "gpu_temp": self.get_gpu_temperature(),
                "core_temps": core_temps,
                "avg_core_temp": sum(core_temps)/len(core_temps) if core_temps else 0,
                "fan_speed": self.get_fan_speed(),
                "power_watts": self.get_power_consumption(),
                "throttling": self.check_throttling(),
                "disk_io_rate": (disk_io.read_bytes + disk_io.write_bytes) / 1024 / 1024 if disk_io else 0
            }
        except Exception:
            return {"cpu_usage": 0, "memory_usage": 0, "freq_mhz": 0, "disk_usage": 0, "gpu_temp": None, "core_temps": [], "throttling": "UNKNOWN"}

    def get_top_processes(self, count=3):
        """NEW FEATURE: Root Cause Analysis - Identify processes with high CPU usage."""
        processes = []
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage and return top N
        sorted_procs = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
        return sorted_procs[:count]
