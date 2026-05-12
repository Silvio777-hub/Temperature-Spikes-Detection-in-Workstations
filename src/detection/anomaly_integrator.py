class AnomalyIntegrator:
    """Combines rule-based and ML outputs."""
    
    @staticmethod
    def integrate(rule_state, rule_msg, ml_anomaly, ml_score):
        """
        Determines final system state.
        ML is used as a high-confidence confirmation.
        """
        final_state = rule_state
        final_msg = rule_msg
        
        # If ML detects an anomaly but rules are normal, escalate to WARNING
        if ml_anomaly and rule_state == "NORMAL":
            final_state = "ANOMALY (ML)"
            final_msg = f"Statistical anomaly detected (Score: {ml_score:.2f})"
            
        # If both agree on emergency/spike, keep the high severity
        return final_state, final_msg
