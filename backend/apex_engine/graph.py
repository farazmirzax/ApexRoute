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
    """Route only high-risk shipments through the dispatcher."""
    risk = state.get("risk_level", 0.0) or 0.0
    print(f"[Router] Oracle reported risk level: {risk}")

    if risk >= 0.7:
        print("[Router] Critical risk detected. Routing to dispatcher for alternatives.")
        return "dispatcher"

    print("[Router] Route is safe. Proceeding with standard logistics.")
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
