from dotenv import load_dotenv
load_dotenv()
import requests
import os
from typing import Optional
from app.services.cache_service import cache

OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.cache_ttl = int(os.getenv("CACHE_TTL", 600))

    def get_weather(self, city: str) -> Optional[dict]:
        # Step 1 — Check cache first
        cache_key = f"weather:{city.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data["source"] = "cache"
            return cached_data

        # Step 2 — Cache miss → call OpenWeatherMap API
        try:
            response = requests.get(
                f"{OPENWEATHER_BASE_URL}/weather",
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric"    # Celsius
                },
                timeout=5               # 5 second timeout
            )

            if response.status_code == 404:
                return None

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")

            data = response.json()

            # Step 3 — Format the response
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "source": "api"         # tells us data came from API not cache
            }

            # Step 4 — Save to cache for next request
            cache.set(cache_key, weather_data, self.cache_ttl)

            return weather_data

        except requests.Timeout:
            raise Exception("OpenWeatherMap API timed out")
        except Exception as e:
            raise Exception(f"Weather service error: {str(e)}")

weather_service = WeatherService()