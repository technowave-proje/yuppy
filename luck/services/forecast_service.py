import requests
from datetime import datetime
from core.database import get_connection, close_connection
from core.config import OPENWEATHER_API_KEY
import time
from states import states



def update_forecast():
    """
    3 saatlik / 5 günlük tahmin verilerini çeker ve DB'ye kaydeder.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    
    for state in states:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={state['lat']}&lon={state['lon']}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
            response = requests.get(url).json()
            
            for forecast in response['list']:
                forecast_time = datetime.utcfromtimestamp(forecast['dt'])
                temp = forecast['main']['temp']
                feels_like = forecast['main']['feels_like']
                temp_min = forecast['main']['temp_min']
                temp_max = forecast['main']['temp_max']
                pressure = forecast['main']['pressure']
                humidity = forecast['main']['humidity']
                weather_main = forecast['weather'][0]['main']
                weather_desc = forecast['weather'][0]['description']
                weather_icon = forecast['weather'][0]['icon']
                clouds = forecast['clouds']['all']
                wind_speed = forecast['wind']['speed']
                wind_deg = forecast['wind'].get('deg', 0)
                wind_gust = forecast['wind'].get('gust', 0.0)
                visibility = forecast.get('visibility', 0)
                pop = forecast.get('pop', 0.0)
                rain_3h = forecast.get('rain', {}).get('3h', 0.0)
                snow_3h = forecast.get('snow', {}).get('3h', 0.0)
                pod = 'd'  # default day/night placeholder
                
                cursor.execute("""
                    INSERT INTO weather_3h_forecast
                    (state, country, lat, lon, forecast_time, temp, feels_like, temp_min, temp_max, pressure, humidity,
                     weather_main, weather_description, weather_icon, clouds, wind_speed, wind_deg, wind_gust,
                     visibility, pop, rain_3h, snow_3h, pod)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE 
                        temp=%s, feels_like=%s, temp_min=%s, temp_max=%s, pressure=%s, humidity=%s,
                        weather_main=%s, weather_description=%s, weather_icon=%s, clouds=%s, wind_speed=%s,
                        wind_deg=%s, wind_gust=%s, visibility=%s, pop=%s, rain_3h=%s, snow_3h=%s
                """, (
                    state['state'], state['country'], state['lat'], state['lon'], forecast_time, temp, feels_like,
                    temp_min, temp_max, pressure, humidity, weather_main, weather_desc, weather_icon, clouds,
                    wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, snow_3h, pod,
                    temp, feels_like, temp_min, temp_max, pressure, humidity, weather_main, weather_desc,
                    weather_icon, clouds, wind_speed, wind_deg, wind_gust, visibility, pop, rain_3h, snow_3h
                ))
            conn.commit()
            time.sleep(1)

    close_connection(conn, cursor) 