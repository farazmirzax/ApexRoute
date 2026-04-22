# apex_engine/nodes.py
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from .state import SupplyChainState
from .tools import get_optimized_route, get_route_preview

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

def intel_gatherer_node(state: SupplyChainState):
    """Scan the global network status injected by the data simulator."""
    fleet_size = len(state.get("fleet", []))
    print(f"[Intel Node] Scanning global network for {fleet_size} active shipments...")
    return {} # Passes the simulated network_status straight to the Oracle

def risk_oracle_node(state: SupplyChainState):
    """Analyze all shipments simultaneously against the global shock event."""
    print("[Oracle Node] Gemini is analyzing network-wide risk propagation...")

    fleet = state["fleet"]
    disruptions = ", ".join(state["network_status"]["active_disruptions"]) or "No current disruptions."
    
    fleet_summary = "\n".join([f"- {s['shipment_id']}: {s['origin']} to {s['destination']}" for s in fleet])

    prompt = f"""
    You are Project Sentinel, an elite supply chain AI.
    Active Global Disruption: {disruptions}

    Analyze this fleet of shipments:
    {fleet_summary}

    Determine the risk of delay for each shipment (0.0 to 1.0). 
    If a shipment's destination or origin is caught in the active disruption, assign a high risk (>= 0.7).
    If it is unaffected, assign a low risk (< 0.3).

    Output EXACTLY one line per shipment in this format:
    [SHIPMENT_ID]: [RISK_SCORE]
    """

    response = llm.invoke(prompt)
    
    # Parse the LLM output and assign risk scores to the individual ships
    for line in response.content.split("\n"):
        if ":" in line and "REQ-" in line:
            parts = line.split(":")
            s_id = parts[0].strip()
            try:
                score = float(parts[1].strip())
                for s in fleet:
                    if s["shipment_id"] == s_id:
                        s["risk_score"] = score
                        s["status"] = "AT_RISK" if score >= 0.7 else "ON_TIME"
            except ValueError:
                pass

    return {"fleet": fleet}

def route_planner_node(state: SupplyChainState):
    """Draw the standard straight-line flight paths for the entire fleet."""
    print("[Route Planner] Plotting standard transit geometries...")
    fleet = state["fleet"]
    
    for s in fleet:
        # Only fetch standard routes if evasive coordinates haven't been applied yet
        if not s.get("route_coordinates"):
            s["route_coordinates"] = get_route_preview(s["current_location"], s["destination"])
            
    return {"fleet": fleet}

def dispatcher_node(state: SupplyChainState):
    """Calculate heavy OSRM evasive maneuvers ONLY for at-risk shipments."""
    print("[Dispatcher] Critical bottlenecks detected. Re-routing affected shipments...")
    fleet = state["fleet"]
    actions = []
    
    for s in fleet:
        if s["risk_score"] >= 0.7:
            print(f"   -> Rerouting {s['shipment_id']} away from danger zone...")
            action, coords = get_optimized_route(s["current_location"], s["destination"])
            
            s["route_coordinates"] = coords
            s["status"] = "REROUTED"
            actions.append(f"{s['shipment_id']}: {action.split('.')[0]}") # Keep it brief

    sys_action = " | ".join(actions) if actions else "Network fully optimized."
    return {"fleet": fleet, "system_action": sys_action}