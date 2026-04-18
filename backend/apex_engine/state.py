# apex_engine/state.py
from typing import TypedDict, Optional

# The LangGraph State (The Clipboard)
# This dictates exactly what data is passed between your agents.
class SupplyChainState(TypedDict):
    shipment_id: str
    current_location: str
    destination: str
    weather_data: Optional[str]
    news_data: Optional[str]
    risk_level: Optional[float]
    recommended_action: Optional[str]