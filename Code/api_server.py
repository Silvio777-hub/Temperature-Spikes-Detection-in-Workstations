from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import uvicorn
import json
import os

# NEW: Security Layer
API_KEY = "CPS_SECURE_TOKEN_2026" # This should be in a .env file in production
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(header_val: str = Depends(api_key_header)):
    if header_val == API_KEY:
        return header_val
    raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")

app = FastAPI(title="CPS Workstation Health API")

# Path to the persistent state file
STATE_FILE = "Models/system_state.json"
HISTORY_FILE = "Logs/system_events.csv"

@app.get("/health", dependencies=[Depends(get_api_key)])
def get_health():
    """Returns the current persistent health state of the workstation."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_state": "UNKNOWN", "message": "No state data available."}

@app.get("/metrics/latest")
def get_latest_metrics():
    """Retrieves the most recent telemetry from the log file."""
    if os.path.exists(HISTORY_FILE):
        import pandas as pd
        df = pd.read_csv(HISTORY_FILE)
        if not df.empty:
            return df.iloc[-1].to_dict()
    return {"error": "No metrics logged yet."}

def start_api_server(port=8000):
    """Launches the production-grade FastAPI server."""
    print(f"Starting Multi-Machine Scalability API on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_api_server()
