

from services.weather_service import update_weather
from fastapi import FastAPI
from routers import fastapi_tempo
from routers import fastapi_openweather
 # tempo.py dosyanın yolu

app = FastAPI()


# Router’ı ekle
app.include_router(fastapi_tempo.router)
app.include_router(fastapi_openweather.router)
