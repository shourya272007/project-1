import os
import sys
import requests
from dotenv import load_dotenv

#load environment variables from .env files is available
load_dotenv()

WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")
NEWS_API_KEY =os.getenv("NEWS_API_KEY")

WEATHER_URL="https://api.weatherapi.com/v1/current.json"
NEWS_URL="https://newsapi.org/v2/top-headlines"

def check_api_keys():
    """validates that api keys exist before running."""
    if not WEATHER_API_KEY:
        missing.append("WEATHER_API_KEY (from https://www.weatherapi.com/)")
    if not NEWS_API_KEY:
        missing.append("NEWS_API_KEY (from https://newsapi.org/)")
    
    if missing:
        print("⚠️ missing API key configuration:")
        for key in missing:
            print (f" - {key}")
        print("\n please set them in a .env file or environment vriables.")
        return False
    return True

def get_weather(city: str):
    """fetch weather data for a given city """
    params={
        "key" : WEATHER_API_KEY,
        "q": city,
        "aqi":"no",
    }
    try:
        response= request.get(WEATHER_URL, params=params, timeout=8)
        if response.status_code==200:
            data = response.json()
            return {
                "city": data["location"]["name"],
                "country" : data["location"]["country"],
                "country_code": data["location"]["country"][:2].lower(),
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"],
            }   
        elif response.status_code == 400:
            return{"error": f"City '{city}' not found. Please check spelling."}
        else:
            return {"error": f"Weather API error: HTTP {response.status_code}"}
    except request.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
        
        
        



