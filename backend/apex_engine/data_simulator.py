# apex_engine/data_simulator.py
import random

def generate_global_fleet():
    """Generates a mock fleet of 10 active global shipments."""
    return [
        {"shipment_id": "REQ-101", "origin": "Lucknow", "current_location": "Lucknow", "destination": "Gaza", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-102", "origin": "Mumbai", "current_location": "Mumbai", "destination": "Gaza", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-103", "origin": "Dubai", "current_location": "Dubai", "destination": "Rotterdam", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-104", "origin": "Singapore", "current_location": "Singapore", "destination": "Rotterdam", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-105", "origin": "Miami Port", "current_location": "Miami Port", "destination": "Rotterdam", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-106", "origin": "New York", "current_location": "New York", "destination": "London", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-107", "origin": "Istanbul", "current_location": "Istanbul", "destination": "Gaza", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-108", "origin": "Shanghai", "current_location": "Shanghai", "destination": "Los Angeles", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-109", "origin": "Shenzhen", "current_location": "Shenzhen", "destination": "Seattle", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
        {"shipment_id": "REQ-110", "origin": "Kyiv", "current_location": "Kyiv", "destination": "Warsaw", "status": "ON_TIME", "risk_score": 0.0, "route_coordinates": []},
    ]

def get_initial_network_state(shock_event: str):
    """Builds the initial state, injecting the shock event if triggered."""
    fleet = generate_global_fleet()

    # The Hackathon "Money" Triggers
    if shock_event == "SUEZ_BLOCKADE":
        news = "URGENT THREAT: Suez Canal completely blocked by grounded ultra-large vessel. All Middle East and Mediterranean transit halted."
        health = 0.4
    elif shock_event == "MIAMI_HURRICANE":
        news = "URGENT THREAT: Category 5 Hurricane approaching Florida coast. Port of Miami suspending all operations immediately."
        health = 0.6
    else:
        news = "Global logistics network operating at standard capacity. No major disruptions."
        health = 1.0

    network_status = {
        "active_disruptions": [news] if shock_event != "NONE" else [],
        "impacted_shipments": 0,
        "network_health": health
    }

    return fleet, network_status