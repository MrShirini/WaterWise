import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
# ------------------ Plant Profiles ------------------
plant_profiles = {
    "tomato": {"water_threshold_temp": 25, "base_water": 1.5},
    "basil": {"water_threshold_temp": 20, "base_water": 0.8},
    "lettuce": {"water_threshold_temp": 18, "base_water": 1.0}
}

# ------------------ Get Weather Data ------------------
def get_weather(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()

    if "current" in data:
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        will_rain = "rain" in condition.lower()
        return temp, condition, will_rain
    else:
        print("Error getting weather data:", data)
        return None, None, None

# ------------------ Watering Logic ------------------
def watering_advice(plant, temp, will_rain):
    profile = plant_profiles.get(plant.lower())
    if not profile:
        return f"Sorry, I don't have data for {plant}."

    base = profile["base_water"]
    threshold = profile["water_threshold_temp"]

    if temp is None:
        return "Couldn't fetch temperature."

    if will_rain:
        return f"It’s raining or expected to rain today. Don’t water your {plant}."

    if temp >= threshold:
        return f"It’s {temp}°C — Water your {plant} with around {base + 0.5:.1f}L today."
    else:
        return f"It’s {temp}°C — Water your {plant} with about {base:.1f}L today."

# ------------------ Main Program ------------------
if __name__ == "__main__":
    city = input("Enter your city: ")
    plant = input("Enter your plant (tomato, basil, lettuce): ")

    temp, condition, will_rain = get_weather(city, API_KEY)
    print(f"\nWeather condition: {condition}")
    print(watering_advice(plant, temp, will_rain))
