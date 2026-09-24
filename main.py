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
        



