# apex_engine/graph.py
from langgraph.graph import StateGraph, END
from .state import SupplyChainState
from .nodes import intel_gatherer_node, risk_oracle_node, route_planner_node, dispatcher_node

# 1. Initialize the Graph with our specific State
workflow = StateGraph(SupplyChainState)

# 2. Add the Nodes (The Agents)
workflow.add_node("intel", intel_gatherer_node)
workflow.add_node("oracle", risk_oracle_node)
workflow.add_node("route_planner", route_planner_node)  # ALWAYS runs to calculate GPS
workflow.add_node("dispatcher", dispatcher_node)  # ONLY runs on high risk

# 3. Define the Routing Logic (The Conditional Edge)
def check_risk_level(state: SupplyChainState):
    """Checks the risk level to determine the next node."""
    risk = state.get("risk_level", 0.0)
    print(f"🚦 [Router] Oracle reported risk level: {risk}")
    
    if risk >= 0.7:
        print("🚨 [Router] Critical risk detected. Routing to Dispatcher for alternative options.")
        return "dispatcher"
    else:
        print("✅ [Router] Route is safe. Proceeding with standard logistics.")
        return END

# 4. Wire the Edges together
# Always start with gathering intel
workflow.set_entry_point("intel")

# After intel, always go to the Oracle
workflow.add_edge("intel", "oracle")

# After Oracle, ALWAYS go to Route Planner to calculate GPS coordinates
workflow.add_edge("oracle", "route_planner")

# After Route Planner, use conditional logic to decide if we need dispatcher
workflow.add_conditional_edges(
    "route_planner",
    check_risk_level,
    {
        "dispatcher": "dispatcher",
        END: END
    }
)

# After Dispatcher completes its analysis, end the process
workflow.add_edge("dispatcher", END)

# 5. Compile the Engine
apex_app = workflow.compile()