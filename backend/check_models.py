import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google.genai import Client
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables!")
    else:
        print(f"✅ API Key found: {api_key[:10]}...")
        
    client = Client(api_key=api_key)
    
    models = client.models.list()
    print("\n📋 Available models:")
    for model in models:
        print(f"  - {model.name}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
