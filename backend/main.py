# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from apex_engine.graph import apex_app
from apex_engine.simulation import create_mock_network, create_mock_shipments, trigger_shock_event, update_shipments_for_event

app = FastAPI(title="Project Apex: Resilient Supply Chain Optimizer")

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ REQUEST/RESPONSE MODELS ============

class ShockEventRequest(BaseModel):
    node_id: str
    event_type: str = "port_closure"  # port_closure, customs_delay, weather, carrier_breakdown
    severity: str = "high"

class NetworkAnalysisRequest(BaseModel):
    num_shipments: int = 18
    shock_event: Optional[ShockEventRequest] = None

class NetworkAnalysisResponse(BaseModel):
    status: str
    network_health_score: float
    total_shipments: int
    delayed_shipments: int
    at_risk_shipments: int
    recommended_actions: List[dict]
    active_events: List[dict]
    bottlenecks: List[dict]
    cascading_risks: dict

# ============ ENDPOINTS ============

@app.post("/api/analyze_network")
async def analyze_network(request: NetworkAnalysisRequest):
    """Analyze the supply chain network and return optimization recommendations."""
    
    print(f"\n[Network] Analysis Request: {request.num_shipments} shipments")
    
    # Generate mock network and shipments
    nodes, edges = create_mock_network()
    shipments = create_mock_shipments(request.num_shipments)
    
    # Handle shock event if requested
    active_events = []
    if request.shock_event:
        print(f"[Event] Triggering: {request.shock_event.event_type} at {request.shock_event.node_id}")
        event = trigger_shock_event(
            request.shock_event.node_id,
            request.shock_event.event_type,
            request.shock_event.severity
        )
        shipments, event = update_shipments_for_event(shipments, event)
        active_events.append(event)
    
    # Build initial state
    initial_state = {
        "shipments": shipments,
        "shipment_index": {s.id: s for s in shipments},
        "nodes": nodes,
        "node_index": {n.id: n for n in nodes},
        "edges": edges,
        "active_events": active_events,
        "event_queue": [],
        "bottleneck_predictions": {},
        "risk_propagation_graph": {},
        "recommended_reroutings": [],
        "optimization_summary": {},
        "network_health_score": 100.0,
        "total_delayed_shipments": sum(1 for s in shipments if s.delay_minutes > 0),
        "total_at_risk_shipments": sum(1 for s in shipments if s.status == "at_risk"),
        "timestamp": 0,
    }
    
    # Run the multi-agent graph
    print("[System] Invoking multi-agent network optimization graph...")
    final_state = apex_app.invoke(initial_state)
    
    # Extract bottlenecks for UI
    bottlenecks = [
        {"node_id": k, **v} 
        for k, v in final_state["bottleneck_predictions"].items() 
        if v["severity"] in ["high", "critical"]
    ]
    
    # Format response
    response = {
        "status": "success",
        "network_health_score": round(final_state["network_health_score"], 1),
        "total_shipments": len(shipments),
        "delayed_shipments": final_state["total_delayed_shipments"],
        "at_risk_shipments": final_state["total_at_risk_shipments"],
        "recommended_actions": final_state["recommended_reroutings"][:5],
        "active_events": [
            {
                "id": e.event_id,
                "type": e.event_type,
                "node": e.affected_node,
                "severity": e.severity,
                "affected_shipments": len(e.affected_shipments),
            }
            for e in active_events
        ],
        "bottlenecks": bottlenecks,
        "cascading_risks": final_state["risk_propagation_graph"],
    }
    
    return response

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "online", "service": "Apex Supply Chain Optimizer"}
