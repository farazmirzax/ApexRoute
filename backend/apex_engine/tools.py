# apex_engine/tools.py
import os
import urllib.parse

import requests


LOCATION_ALIASES = {
    "gaza": "Gaza Strip, Palestine",
    "gaza, palestine": "Gaza Strip, Palestine",
    "gaza strip": "Gaza Strip, Palestine",
    "lucknow": "Lucknow, Uttar Pradesh, India",
    "lucknow, india": "Lucknow, Uttar Pradesh, India",
    "phuket": "Phuket, Mueang Phuket District, Phuket Province, Thailand",
    "phuket, thailand": "Phuket, Mueang Phuket District, Phuket Province, Thailand",
    "miami port": "PortMiami, Miami, Florida, USA",
    "rotterdam": "Rotterdam, South Holland, Netherlands",
    "kyiv": "Kyiv, Ukraine",
    "warsaw": "Warsaw, Masovian Voivodeship, Poland",
    "dubai": "Dubai, United Arab Emirates",
    "dubai, uae": "Dubai, United Arab Emirates",
    "dubai, united arab emirates": "Dubai, United Arab Emirates",
}

GENERIC_LOCATION_TERMS = {
    "city",
    "district",
    "province",
    "state",
    "country",
    "united",
    "arab",
    "emirates",
    "uae",
    "india",
    "thailand",
    "palestine",
    "netherlands",
    "ukraine",
    "poland",
    "usa",
    "florida",
    "south",
    "holland",
    "voivodeship",
    "pradesh",
}

LOGISTICS_KEYWORDS = (
    "logistics",
    "shipment",
    "shipping",
    "cargo",
    "freight",
    "port",
    "harbor",
    "harbour",
    "terminal",
    "container",
    "customs",
    "supply chain",
    "truck",
    "trucking",
    "rail",
    "route",
    "reroute",
    "delay",
    "disruption",
    "strike",
    "blockade",
    "closure",
)

THREAT_KEYWORDS = (
    "war",
    "attack",
    "missile",
    "drone",
    "protest",
    "riot",
    "violence",
    "military",
    "conflict",
    "sanction",
)

ROUTE_IMPACT_TERMS = (
    "disrupt",
    "disruption",
    "delay",
    "halt",
    "closed",
    "closure",
    "blocked",
    "reroute",
    "risk",
    "supply chain",
    "shipping",
    "cargo",
    "port",
    "freight",
)

OFF_TOPIC_KEYWORDS = (
    "crypto",
    "xrp",
    "bitcoin",
    "ethereum",
    "token",
    "coin",
    "nft",
    "stock",
    "shares",
    "earnings",
    "celebrity",
    "movie",
    "music",
    "transfer rumor",
    "premier league",
)


def _normalize_location(location: str) -> str:
    """Resolve ambiguous place names into more reliable geocoding inputs."""
    cleaned = " ".join(location.split()).strip()
    return LOCATION_ALIASES.get(cleaned.lower(), cleaned)


def _location_terms(location: str) -> list[str]:
    """Break a normalized location into terms for candidate scoring."""
    normalized = _normalize_location(location).lower().replace(",", " ")
    return [term for term in normalized.split() if term and term not in GENERIC_LOCATION_TERMS]


def _score_geocode_candidate(candidate: dict, location: str) -> tuple[int, float, int]:
    """Prefer exact place-name matches over broad regional matches."""
    display_name = (candidate.get("display_name") or "").lower()
    name = (candidate.get("name") or "").lower()
    category = (candidate.get("category") or "").lower()
    place_type = (candidate.get("type") or "").lower()
    addresstype = (candidate.get("addresstype") or "").lower()
    candidate_text = f"{name} {display_name}"

    terms = _location_terms(location)
    term_hits = sum(1 for term in terms if term in candidate_text)
    exact_name_bonus = 5 if name and any(term == name for term in terms) else 0
    phrase_bonus = 3 if _normalize_location(location).lower() in candidate_text else 0
    category_bonus = 2 if category in {"place", "boundary"} else 0
    type_bonus = 0
    preferred_types = {"city", "town", "village", "hamlet", "suburb", "administrative", "locality", "county"}
    if place_type in preferred_types or addresstype in preferred_types:
        type_bonus = 3
    broad_types = {"state", "region", "continent", "archipelago"}
    if place_type in broad_types or addresstype in broad_types:
        type_bonus = -2
    importance = float(candidate.get("importance") or 0.0)
    admin_rank = int(candidate.get("place_rank") or 1000)

    return (term_hits + exact_name_bonus + phrase_bonus + category_bonus + type_bonus, importance, -admin_rank)


def _get_location_coords(location: str, headers: dict[str, str]):
    """Convert a place name into coordinates for routing and map previews."""
    normalized_location = _normalize_location(location)
    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={urllib.parse.quote_plus(normalized_location)}&format=jsonv2&addressdetails=1&limit=10"
    )
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
        if payload:
            best_match = max(payload, key=lambda candidate: _score_geocode_candidate(candidate, normalized_location))
            return best_match["lon"], best_match["lat"]
    except requests.RequestException:
        pass
    return None, None


def _is_relevant_article(article: dict, destination: str) -> bool:
    """Keep articles that mention the destination and route-impacting signals."""
    title = article.get("title") or ""
    description = article.get("description") or ""
    combined = f"{title} {description}".lower()

    destination_terms = _location_terms(destination)
    mentions_destination = any(term in combined for term in destination_terms)
    mentions_off_topic = any(keyword in combined for keyword in OFF_TOPIC_KEYWORDS)
    mentions_logistics = any(keyword in combined for keyword in LOGISTICS_KEYWORDS)
    mentions_threat = any(keyword in combined for keyword in THREAT_KEYWORDS)
    mentions_route_impact = any(term in combined for term in ROUTE_IMPACT_TERMS)

    if mentions_off_topic:
        return False

    if not destination_terms:
        return False

    return mentions_destination and mentions_logistics and (mentions_route_impact or mentions_threat)


def get_weather(destination: str) -> str:
    """Fetches real-time weather conditions for the destination."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key or api_key == "your_openweather_key":
        return "Weather API Key missing."

    normalized_destination = _normalize_location(destination)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={normalized_destination}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("cod") != 200:
            return f"Weather Intel Unavailable: {response.get('message')}"

        desc = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        wind = response["wind"]["speed"]
        return f"Current conditions at {normalized_destination}: {desc.upper()}, Temp: {temp} C, Wind: {wind} m/s."
    except Exception as e:
        return f"Weather API Error: {str(e)}"


def get_news(destination: str) -> str:
    """Scrapes global news for logistics threats."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "your_newsapi_key":
        return "News API Key missing."

    normalized_destination = _normalize_location(destination)
    raw_query = (
        f'"{normalized_destination}" AND '
        "(logistics OR shipping OR cargo OR freight OR port OR strike OR blockade OR delay OR closure OR supply chain)"
    )
    safe_query = urllib.parse.quote(raw_query)
    url = (
        "https://newsapi.org/v2/everything"
        f"?q={safe_query}&searchIn=title,description&sortBy=relevancy&language=en&pageSize=10&apiKey={api_key}"
    )

    try:
        response = requests.get(url, timeout=10).json()
        articles = response.get("articles", [])

        filtered_articles = [article for article in articles if _is_relevant_article(article, normalized_destination)]
        top_articles = filtered_articles[:3]

        if not top_articles:
            return "No immediate logistics threats detected in recent destination-specific news."

        news_summary = " | ".join([f"HEADLINE: {article['title']}" for article in top_articles if article.get("title")])
        return f"Recent Intel: {news_summary}"
    except Exception as e:
        return f"News API Error: {str(e)}"


def get_route_preview(origin: str, destination: str):
    """Return a lightweight straight-line preview for low-risk routes."""
    headers = {"User-Agent": "RequiemSupplyChainApp/1.0"}
    lon1, lat1 = _get_location_coords(origin, headers)
    lon2, lat2 = _get_location_coords(destination, headers)

    if not (lon1 and lat1 and lon2 and lat2):
        return []

    return [[float(lat1), float(lon1)], [float(lat2), float(lon2)]]


def get_optimized_route(origin: str, destination: str):
    """Calculates an alternative physical route using open-source APIs."""
    headers = {"User-Agent": "RequiemSupplyChainApp/1.0"}

    normalized_origin = _normalize_location(origin)
    normalized_destination = _normalize_location(destination)

    print(f"[Routing Tool] Pinging OpenStreetMap for coordinates of {normalized_origin} and {normalized_destination}...")
    lon1, lat1 = _get_location_coords(normalized_origin, headers)
    lon2, lat2 = _get_location_coords(normalized_destination, headers)

    if not (lon1 and lat1 and lon2 and lat2):
        return "Routing AI Error: Could not lock GPS coordinates.", []

    print("[Routing Tool] Calculating evasive route via OSRM...")
    osrm_url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}?overview=simplified&geometries=geojson"
    )

    try:
        response = requests.get(osrm_url, timeout=15).json()
        if response.get("code") != "Ok":
            return "Alternative Route generation failed. Awaiting human override.", []

        route = response["routes"][0]
        distance_km = round(route["distance"] / 1000, 1)
        duration_hrs = round(route["duration"] / 3600, 1)
        coords = route["geometry"]["coordinates"]
        leaflet_coords = [[coord[1], coord[0]] for coord in coords]

        action_string = (
            "ALTERNATIVE ROUTE LOCKED: Rerouting via secondary continental highways. "
            f"Distance: {distance_km} km. ETA: {duration_hrs} hours."
        )
        return action_string, leaflet_coords
    except Exception as e:
        return f"Routing API Error: {str(e)}", []
