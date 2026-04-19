# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Import this
from pydantic import BaseModel
from apex_engine.graph import apex_app

app = FastAPI(title="Project Sentinel: Apex Route API")

# --- CORS CONFIGURATION ---
# This tells FastAPI to accept requests from your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Your Next.js port
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (POST, GET, etc.)
    allow_headers=["*"], # Allow all headers
)
# --------------------------

class ShipmentRequest(BaseModel):
    shipment_id: str
    current_location: str
    destination: str

@app.post("/api/analyze_route")
async def analyze_route(request: ShipmentRequest):
    print(f"\n� Incoming Request for Shipment: {request.shipment_id}")
    
    initial_state = {
        "shipment_id": request.shipment_id,
        "current_location": request.current_location,
        "destination": request.destination,
        "weather_data": None,
        "news_data": None,
        "risk_level": None,
        "recommended_action": None,
        "route_coordinates": None
    }
    
    final_state = apex_app.invoke(initial_state)
    
    return {
        "status": "success",
        "data": final_state
    }