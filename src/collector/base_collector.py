from abc import ABC, abstractmethod

class BaseCollector(ABC):
    """Abstract base class for all hardware data collectors."""
    
    @abstractmethod
    def get_temperature(self):
        """Should return CPU temperature in Celsius."""
        pass

    @abstractmethod
    def get_system_metrics(self):
        """Should return a dict with cpu_usage, memory_usage, etc."""
        pass
