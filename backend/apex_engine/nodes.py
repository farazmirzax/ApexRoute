# apex_engine/nodes.py
import os
from dotenv import load_dotenv  # <-- 1. Import the dotenv library

# 2. Load the environment variables BEFORE initializing Gemini
load_dotenv() 

from .state import SupplyChainState
from .tools import get_weather, get_news, get_optimized_route

# Use mock LLM for development (free tier quota exhausted)
class MockLLM:
    """Mock LLM for testing without API quota limits"""
    def invoke(self, prompt):
        """Return mock oracle response"""
        class Response:
            content = "RISK_LEVEL: 0.85\nREASON: High risk due to hurricane and port strike."
        return Response()

#llm = MockLLM()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

# --- AGENT 1: The Intel Gatherer ---
def intel_gatherer_node(state: SupplyChainState):
    print("🕵️‍♂️ [Intel Node] Gathering live data...")
    # Call our mock tools
    weather = get_weather(state["destination"])
    news = get_news(state["destination"])
    
    # Return ONLY the parts of the state we want to update
    return {"weather_data": weather, "news_data": news}


# --- AGENT 2: The Risk Oracle (Supervisor) ---
def risk_oracle_node(state: SupplyChainState):
    print("🧠 [Oracle Node] Gemini is analyzing the risk...")
    
    prompt = f"""
    You are Project Sentinel, an elite supply chain AI.
    Analyze the following shipment data:
    - Shipment ID: {state['shipment_id']}
    - Weather: {state['weather_data']}
    - News: {state['news_data']}
    
    Task: Calculate the risk of delay. 
    Output EXACTLY two lines in this format:
    RISK_LEVEL: [a float between 0.0 and 1.0]
    REASON: [one sentence explanation]
    """
    
    response = llm.invoke(prompt)
    output_text = response.content
    
    # Simple parser to extract the risk level
    risk_level = 0.0
    for line in output_text.split('\n'):
        if "RISK_LEVEL:" in line:
            try:
                risk_level = float(line.split(":")[1].strip())
            except ValueError:
                risk_level = 0.0
                
    return {"risk_level": risk_level}


# --- AGENT 3: The Dispatcher ---
def dispatcher_node(state: SupplyChainState):
    print("⚡ [Dispatcher Node] Critical risk detected. Calculating evasive maneuvers...")
    
    # Catch both the text action and the GPS coords
    action, coords = get_optimized_route(state["current_location"], state["destination"])
    
    # Update the LangGraph state
    return {
        "recommended_action": action,
        "route_coordinates": coords
    }