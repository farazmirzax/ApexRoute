# apex_engine/state.py
from typing import TypedDict, Optional, List, Any

class Shipment(TypedDict):
    """Represents a single truck/vessel in the network."""
    shipment_id: str
    origin: str
    current_location: str
    destination: str
    status: str  # e.g., "ON_TIME", "AT_RISK", "REROUTED"
    risk_score: float
    route_coordinates: Optional[List[Any]]

class NetworkStatus(TypedDict):
    """Tracks global operational health and active bottlenecks."""
    active_disruptions: List[str]
    impacted_shipments: int
    network_health: float  # 0.0 to 1.0 (1.0 = perfect flow)

class SupplyChainState(TypedDict):
    """The central state flowing through the LangGraph agents."""
    fleet: List[Shipment]
    network_status: NetworkStatus
    system_action: Optional[str]  # e.g., "INITIATED MASS REROUTE TO AVOID SUEZ CLOSURE"