# test_run.py
from apex_engine.graph import apex_app

# The initial state of a shipment before Apex Route takes over
initial_state = {
    "shipment_id": "REQ-774-ALPHA",
    "current_location": "Miami Port",
    "destination": "Rotterdam",
    "weather_data": None,
    "news_data": None,
    "risk_level": None,
    "recommended_action": None
}

print(" INITIATING APEX ROUTE PROTOCOL 📍\n")

# Run the LangGraph application
final_state = apex_app.invoke(initial_state)

print("\n=== 📊 FINAL STATE OUTPUT ===")
print(f"Shipment: {final_state['shipment_id']}")
print(f"Risk Level: {final_state['risk_level']}")
print(f"Action Taken: {final_state['recommended_action']}")
print("===============================\n")