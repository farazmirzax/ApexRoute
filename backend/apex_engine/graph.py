# apex_engine/graph.py
from langgraph.graph import END, StateGraph

from .nodes import dispatcher_node, intel_gatherer_node, risk_oracle_node, route_planner_node
from .state import SupplyChainState

workflow = StateGraph(SupplyChainState)

workflow.add_node("intel", intel_gatherer_node)
workflow.add_node("oracle", risk_oracle_node)
workflow.add_node("route_planner", route_planner_node)
workflow.add_node("dispatcher", dispatcher_node)


def check_risk_level(state: SupplyChainState):
    """Route to dispatcher if ANY shipment in the fleet is at risk."""
    fleet = state.get("fleet", [])
    
    # Check if any single ship triggered the >= 0.7 threshold
    is_network_at_risk = any(s.get("risk_score", 0.0) >= 0.7 for s in fleet)
    
    if is_network_at_risk:
        print("[Router] Network threat detected. Waking up Dispatcher.")
        return "dispatcher"

    print("[Router] Network is secure. Proceeding with standard logistics.")
    return END


workflow.set_entry_point("intel")
workflow.add_edge("intel", "oracle")
workflow.add_edge("oracle", "route_planner")
workflow.add_conditional_edges(
    "route_planner",
    check_risk_level,
    {
        "dispatcher": "dispatcher",
        END: END,
    },
)
workflow.add_edge("dispatcher", END)

apex_app = workflow.compile()