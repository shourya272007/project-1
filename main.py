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
NEWS_EVERYTHING_URL = "https://newsapi.org/v2/everything"

def check_api_keys():
    """validates that api keys exist before running."""
    missing = []
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
        response = requests.get(WEATHER_URL, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "country_code": data["location"]["country"][:2].lower(),
                "temp_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"],
            }   
        elif response.status_code == 400:
            return {"error": f"City '{city}' not found. Please check spelling."}
        else:
            return {"error": f"Weather API error: HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_news(query: str, country_code: str):
    """fetch top news headlines for a given query"""
    #attempt 1: fetch city-specific news using query as the city name
    params={
        "apiKey": NEWS_API_KEY,
        "q": query,
        "pageSize":3,
        "language":"en"
    }
    try:
        res = requests.get(NEWS_URL, params=params, timeout=8)
        articles = res.json().get("articles", []) if res.status_code == 200 else []

        #attempt 2: fall back to country top headline if city query fail
        if not articles:
            params = {
                "apiKey": NEWS_API_KEY,
                "country": country_code,
                "pageSize": 3,
                "language": "en"
            }
            res = requests.get(NEWS_URL, params=params, timeout=8)
            if res.status_code == 200:
                articles = res.json().get("articles", [])
        if not articles:
            return ["no recent english headlines found for this location."]

        return [art["title"] for art in articles if art.get("title")]
    except requests.exceptions.RequestException:
        return["unable to fetch news headlines (network or timeout issue)."]

def display_dashboard(weather_data: dict, news_headlines: list):
    """renders formatted CLI dashboard"""
    city_name= weather_data["city"].upper()
    country_name= weather_data["country"]
     
    print("\n"+ "=" * 45)
    print(f"🌤️ {city_name},{country_name} DASHBOARD 🌤️")
    print("=" *45)
    print(f"Weather: {weather_data['temp_c']}°C, {weather_data['condition']}")
    print(f"Humidity:{weather_data['humidity']}% | wind:{weather_data['wind_kph']}km/h")
    print("-"*45)
    print("📰 TOP NEWS HEADLINES")
    for i, headline in enumerate(news_headlines, 1):
        print(f"{i}.{headline}")
    print("="*45+"\n")

def main():
 print("\n Starting City Dashboard...")
 if not check_api_keys():
    sys.exit(1)
    
 while True:
    try:
        city_input= input("enter city name(or 'Quit','Exit','Q' to exit):").strip()
        if not city_input:
            continue
        if city_input.lower() in ("quit","exit","q"):
            print("thankyou for using city dashboard")
            break

        weather = get_weather(city_input)
        if "error" in weather:
            print(f"{weather['error']}\n")
            continue

        headlines = get_news(weather["city"], weather["country_code"])
        display_dashboard(weather, headlines)

    except KeyboardInterrupt:
        print("\n exiting...")
        break

if __name__ == "__main__":
    main()
