import requests


def get_current_weather(city: str) -> dict:
    """
    Returns current weather for a city using Open-Meteo APIs.
    """
    try:
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city}&language=en&format=json&count=1"
        )

        geo_res = requests.get(geo_url, timeout=10)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if "results" not in geo_data or not geo_data["results"]:
            return {
                "success": False,
                "message": f"No location found for '{city}'."
            }

        place = geo_data["results"][0]
        lat = place["latitude"]
        lon = place["longitude"]
        name = place["name"]
        country = place.get("country", "")

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )

        weather_res = requests.get(weather_url, timeout=10)
        weather_res.raise_for_status()
        weather_data = weather_res.json()

        current = weather_data.get("current_weather", {})

        return {
            "success": True,
            "city": name,
            "country": country,
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
            "weathercode": current.get("weathercode"),
            "time": current.get("time"),
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Weather service unavailable: {str(e)}"
        }
