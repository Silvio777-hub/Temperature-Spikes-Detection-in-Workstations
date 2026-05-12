class RuleEngine:
    """Implements threshold-based detection logic."""
    def __init__(self, warning_temp=75, critical_temp=85):
        self.warning_temp = warning_temp
        self.critical_temp = critical_temp

    def analyze(self, metrics):
        temp = metrics.get('temperature', 0)
        
        if temp >= self.critical_temp:
            return "EMERGENCY", f"Critical temperature exceeded: {temp:.1f}°C"
        elif temp >= self.warning_temp:
            return "WARNING", f"Warning temperature reached: {temp:.1f}°C"
        
        # Check for rapid rise (if temp_rate is available)
        if metrics.get('temp_rate', 0) > 2.0:
            return "SPIKE", "Rapid temperature rise detected"
            
        return "NORMAL", "System temperature within safe bounds"
