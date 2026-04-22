# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Project Apex: Resilient Supply Chain Optimizer")

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ REQUEST MODELS ============
class NetworkRequest(BaseModel):
    # The frontend will send one of: "NONE", "SUEZ_BLOCKADE", or "MIAMI_HURRICANE"
    shock_event: str = "NONE"

# ============ ENDPOINTS ============
@app.post("/api/analyze_network")
async def analyze_network(request: NetworkRequest):
    """Analyze the global supply chain network and return optimization recommendations."""
    try:
        from apex_engine.data_simulator import get_initial_network_state
        from apex_engine.graph import apex_app
        
        print(f"\n[Network] Analysis Request. Shock Event: {request.shock_event}")
        
        # 1. Generate the fleet and apply any disaster parameters
        fleet, net_status = get_initial_network_state(request.shock_event)
        
        # 2. Package it into our new SupplyChainState format
        initial_state = {
            "fleet": fleet,
            "network_status": net_status,
            "system_action": None
        }
        
        # 3. Fire the LangGraph Multi-Agent Engine!
        print("[System] Invoking multi-agent network optimization graph...")
        final_state = apex_app.invoke(initial_state)
        
        return {"status": "success", "data": final_state}
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "online", "service": "Apex Supply Chain Optimizer"}