from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml_model import MLModel
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TEMPO_API_URL = os.getenv("TEMPO_API_URL")
TEMPO_TOKEN = os.getenv("TEMPO_TOKEN")

app = FastAPI(title="Health Activity Predictor API")
model = MLModel()

# -----------------------------
# 1️⃣ Kullanıcı veri modeli
# -----------------------------
class PredictRequest(BaseModel):
    age_group: str
    pregnancy_status: str
    respiratory_disease: str
    cardio_disease: str
    activity: str
    temperature: float
    humidity: float
    wind_speed: float
    rain: bool
    aqi: int
    pm25: float

# -----------------------------
# 2️⃣ Tahmin endpointi
# -----------------------------
@app.post("/predict")
def predict_activity(data: PredictRequest):
    try:
        features = data.dict()
        prediction = model.predict(features)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# 3️⃣ Canlı hava verisi endpointi
# -----------------------------
@app.get("/weather")
def get_weather(lat: float, lon: float):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"

        weather = requests.get(weather_url).json()
        air = requests.get(air_url).json()

        data = {
            "temperature": weather["main"]["temp"],
            "humidity": weather["main"]["humidity"],
            "wind_speed": weather["wind"]["speed"],
            "rain": "rain" in weather and bool(weather["rain"]),
            "aqi": air["list"][0]["main"]["aqi"],
            "pm25": air["list"][0]["components"]["pm2_5"]
        }
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# 4️⃣ Tempo veri endpointi
# -----------------------------
@app.get("/tempo")
def get_tempo(lat: float, lon: float):
    try:
        headers = {"Authorization": f"Bearer {TEMPO_TOKEN}"}
        params = {"latitude": lat, "longitude": lon}
        resp = requests.get(TEMPO_API_URL, headers=headers, params=params).json()
        return {
            "aqi": resp.get("aqi", 2),
            "pm25": resp.get("pm25", 10.0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))