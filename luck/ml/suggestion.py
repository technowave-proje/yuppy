# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from ml.advisor import check_activity, age_group_advice, pregnancy_advice, respiratory_advice, cardio_metabolic_advice

app = FastAPI()

# ----------------------
# Request modelleri
# ----------------------
class ActivityRequest(BaseModel):
    activity: str
    temperature: float
    wind_speed: float
    rain: bool
    aqi: int
    pm25: float

class HealthRequest(BaseModel):
    temperature: float
    aqi: int
    pm25: float

# ----------------------
# Endpoints
# ----------------------
@app.post("/activity_recommendation")
def activity_recommendation(req: ActivityRequest):
    return check_activity(req.activity, req.temperature, req.wind_speed, req.rain, req.aqi, req.pm25)

@app.post("/health/age_group/{age_group}")
def health_age_group(age_group: str, req: HealthRequest):
    return age_group_advice(age_group, req.temperature, req.aqi, req.pm25)

@app.post("/health/pregnancy/{status_group}")
def health_pregnancy(status_group: str, req: HealthRequest):
    return pregnancy_advice(status_group, req.temperature, req.aqi, req.pm25)

@app.post("/health/respiratory/{disease}")
def health_respiratory(disease: str, req: HealthRequest):
    return respiratory_advice(disease, req.aqi, req.pm25)

@app.post("/health/cardio/{disease}")
def health_cardio(disease: str, req: HealthRequest):
    return cardio_metabolic_advice(disease, req.temperature, req.aqi, req.pm25)
