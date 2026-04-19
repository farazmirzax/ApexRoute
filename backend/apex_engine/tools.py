# apex_engine/tools.py
import os
import requests

def get_weather(destination: str) -> str:
    """Fetches real-time weather conditions for the destination."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key or api_key == "your_openweather_key": 
        return "Weather API Key missing."

    # Using the standard weather API by city name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={destination}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return f"Weather Intel Unavailable: {response.get('message')}"
            
        desc = response['weather'][0]['description']
        temp = response['main']['temp']
        wind = response['wind']['speed']
        return f"Current conditions at {destination}: {desc.upper()}, Temp: {temp}°C, Wind: {wind} m/s."
    except Exception as e:
        return f"Weather API Error: {str(e)}"

def get_news(destination: str) -> str:
    """Scrapes global news for logistics threats."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "your_newsapi_key": 
        return "News API Key missing."

    # Search for high-risk keywords near the destination
    query = f"{destination} AND (strike OR port OR protest OR hurricane OR delay)"
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&pageSize=3&apiKey={api_key}"
    
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        
        if not articles:
            return "No immediate threats detected in recent global news."
            
        # Format the top 3 headlines for Gemini to read
        news_summary = " | ".join([f"HEADLINE: {a['title']}" for a in articles])
        return f"Recent Intel: {news_summary}"
    except Exception as e:
        return f"News API Error: {str(e)}"

def get_optimized_route(origin: str, destination: str):
    """Calculates an alternative physical route using Open-Source APIs (100% Free)."""
    
    # Identify our app to the free servers so they don't block us
    headers = {'User-Agent': 'RequiemSupplyChainApp/1.0'}

    # STEP 1: Geocoding (Convert City Names to GPS Coordinates using OpenStreetMap)
    def get_coords(city: str):
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        try:
            response = requests.get(url, headers=headers).json()
            if response:
                # Returns Longitude, Latitude
                return response[0]['lon'], response[0]['lat']
        except:
            pass
        return None, None

    print(f"📡 [Routing Tool] Pinging OpenStreetMap for coordinates of {origin} and {destination}...")
    lon1, lat1 = get_coords(origin)
    lon2, lat2 = get_coords(destination)

    if not (lon1 and lat1 and lon2 and lat2):
        return "Routing AI Error: Could not lock GPS coordinates.", []

    # STEP 2: Calculate the actual driving route (using OSRM)
    print("🛣️ [Routing Tool] Calculating evasive route via OSRM...")
    # Added &geometries=geojson to pull the literal road curves
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=simplified&geometries=geojson"
    
    try:
        response = requests.get(osrm_url).json()
        if response.get("code") != "Ok":
            return "Alternative Route generation failed. Awaiting human override.", []

        # Extract distance and time from the open-source router
        route = response['routes'][0]
        distance_km = round(route['distance'] / 1000, 1)  # Convert meters to km
        duration_hrs = round(route['duration'] / 3600, 1)  # Convert seconds to hours
        
        # Grab the literal road GPS points!
        coords = route['geometry']['coordinates']
        
        # OSRM outputs [Longitude, Latitude], but Leaflet maps need [Latitude, Longitude]
        leaflet_coords = [[c[1], c[0]] for c in coords]
        
        action_string = f"ALTERNATIVE ROUTE LOCKED: Rerouting via secondary continental highways. Distance: {distance_km} km. ETA: {duration_hrs} hours."
        
        # Return BOTH the text and the massive array of road coordinates
        return action_string, leaflet_coords
    
    except Exception as e:
        return f"Routing API Error: {str(e)}", []