# apex_engine/graph.py
from langgraph.graph import StateGraph, END
from .state import SupplyChainState
from .nodes import intel_gatherer_node, risk_oracle_node, dispatcher_node

# 1. Initialize the Graph with our specific State
workflow = StateGraph(SupplyChainState)

# 2. Add the Nodes (The Agents)
workflow.add_node("intel", intel_gatherer_node)
workflow.add_node("oracle", risk_oracle_node)
workflow.add_node("dispatcher", dispatcher_node)

# 3. Define the Routing Logic (The Conditional Edge)
def check_risk_level(state: SupplyChainState):
    """Checks the risk level to determine the next node."""
    risk = state.get("risk_level", 0.0)
    print(f"🚦 [Router] Oracle reported risk level: {risk}")
    
    if risk >= 0.7:
        print("🚨 [Router] Critical risk detected. Routing to Dispatcher.")
        return "dispatcher"
    else:
        print("✅ [Router] Route is safe. Ending analysis.")
        return END

# 4. Wire the Edges together
# Always start with gathering intel
workflow.set_entry_point("intel")

# After intel, always go to the Oracle
workflow.add_edge("intel", "oracle")

# After Oracle, use our conditional logic to decide what to do
workflow.add_conditional_edges(
    "oracle",
    check_risk_level,
    {
        "dispatcher": "dispatcher",
        END: END
    }
)

# After Dispatcher completes its reroute, end the process
workflow.add_edge("dispatcher", END)

# 5. Compile the Engine
apex_app = workflow.compile()