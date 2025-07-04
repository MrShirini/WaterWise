import os
import requests
import pickle
import numpy as np
from dotenv import load_dotenv
from sklearn.preprocessing import OneHotEncoder

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ------------------ Model and Encoder ------------------
MODEL_PATH = "model.pkl"
ENCODER_PATH = "encoder.pkl"

# Load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load one-hot encoder
with open(ENCODER_PATH, "rb") as f:
    encoder = pickle.load(f)

# ------------------ Weather Data ------------------
def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)
        data = response.json()

        if "current" not in data:
            raise ValueError(data)

        current = data["current"]
        return {
            "temp": current["temp_c"],
            "humidity": current["humidity"],
            "wind": current["wind_kph"],
            "uv": current["uv"],
            "rain": 1 if "rain" in current["condition"]["text"].lower() else 0
        }
    except Exception as e:
        print("Error fetching weather data:", e)
        return None

# ------------------ Feature Preparation ------------------
def prepare_features(city, plant, stage, soil):
    weather = get_weather(city)
    if not weather:
        return None

    # Combine all input features
    input_data = [[
        plant.lower(),
        stage.lower(),
        soil.lower(),
        weather["temp"],
        weather["humidity"],
        weather["wind"],
        weather["uv"],
        weather["rain"]
    ]]

    # Encode categorical features
    X_cat = encoder.transform([[plant, stage, soil]]).toarray()
    X_num = np.array([[weather["temp"], weather["humidity"], weather["wind"], weather["uv"], weather["rain"]]])
    X = np.concatenate((X_cat, X_num), axis=1)

    return X

# ------------------ Prediction ------------------
def predict_watering(X):
    prediction = model.predict(X)[0]
    return max(0, round(prediction, 2))

# ------------------ Main Program ------------------
if __name__ == "__main__":
    city = input("Enter your city: ")
    plant = input("Plant type (e.g., tomato): ")
    stage = input("Growth stage (young, mature, fruiting): ")
    soil = input("Soil type (sandy, clay, loamy): ")

    X = prepare_features(city, plant, stage, soil)
    if X is not None:
        amount = predict_watering(X)
        print(f"\nRecommended watering amount: {amount} liters")
    else:
        print("Unable to compute recommendation.")
