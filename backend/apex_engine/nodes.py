# apex_engine/nodes.py
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

from .state import SupplyChainState
from .tools import get_news, get_optimized_route, get_route_preview, get_weather


class MockLLM:
    """Mock LLM for testing without API quota limits."""

    def invoke(self, prompt):
        class Response:
            content = "RISK_LEVEL: 0.85\nREASON: High risk due to hurricane and port strike."

        return Response()


# llm = MockLLM()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)


def intel_gatherer_node(state: SupplyChainState):
    """Gather fresh weather and news intelligence."""
    print("[Intel Node] Gathering live data...")
    weather = get_weather(state["destination"])
    news = get_news(state["destination"])
    return {"weather_data": weather, "news_data": news}


def risk_oracle_node(state: SupplyChainState):
    """Ask the model for a normalized risk score."""
    print("[Oracle Node] Gemini is analyzing the risk...")

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

    risk_level = 0.0
    for line in output_text.split("\n"):
        if "RISK_LEVEL:" in line:
            try:
                risk_level = float(line.split(":")[1].strip())
            except ValueError:
                risk_level = 0.0

    return {"risk_level": risk_level}


def route_planner_node(state: SupplyChainState):
    """Prepare the base map geometry for normal, low-risk routes."""
    print("[Route Planner Node] Calculating GPS coordinates for map visualization...")
    coords = get_route_preview(state["current_location"], state["destination"])
    return {"route_coordinates": coords}


def dispatcher_node(state: SupplyChainState):
    """Calculate evasive routing details only for high-risk routes."""
    print("[Dispatcher Node] Critical risk detected. Calculating evasive maneuvers...")
    action, coords = get_optimized_route(state["current_location"], state["destination"])
    return {
        "recommended_action": action,
        "route_coordinates": coords,
    }
