import requests
from datetime import datetime
from core.database import get_connection, close_connection
from core.config import OPENWEATHER_API_KEY
import time
from states import states


def update_air_quality():
    """
    Hava kalitesi verilerini çeker ve DB'ye kaydeder.
    """
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    
    for state in states:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={state['lat']}&lon={state['lon']}&appid={OPENWEATHER_API_KEY}"
            response = requests.get(url).json()
            
            aqi = response['list'][0]['main']['aqi']
            components = response['list'][0]['components']
            last_updated = datetime.utcnow()
            
            cursor.execute("""
                INSERT INTO air_quality
                (state, country, lat, lon, aqi, pm25, pm10, o3, no2, co, so2, last_updated)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    aqi=%s, pm25=%s, pm10=%s, o3=%s, no2=%s, co=%s, so2=%s, last_updated=%s
            """, (
                state['state'], state['country'], state['lat'], state['lon'],
                aqi, components['pm2_5'], components['pm10'], components['o3'], components['no2'],
                components['co'], components['so2'], last_updated,
                aqi, components['pm2_5'], components['pm10'], components['o3'], components['no2'],
                components['co'], components['so2'], last_updated
            ))
            conn.commit()
            time.sleep(1)
    
    close_connection(conn, cursor)   