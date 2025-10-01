import mysql.connector
from datetime import datetime

# --------------------------
# MySQL bağlantısı
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Serra133705ç*",  
    database="yeniveritabani"  # Hedef veritabanı
)
cursor = conn.cursor()

# --------------------------
# ABD Eyaletleri (Başkent koordinatları)
# --------------------------
usa_states = [
    ("Alabama", 32.361538, -86.279118),
    ("Alaska", 58.3019, -134.4197),
    ("Arizona", 33.4484, -112.0740),
    ("Arkansas", 34.7465, -92.2896),
    ("California", 38.5816, -121.4944),
    ("Colorado", 39.7392, -104.9903),
    ("Connecticut", 41.7637, -72.6851),
    ("Delaware", 39.1582, -75.5244),
    ("Florida", 30.4383, -84.2807),
    ("Georgia", 33.7490, -84.3880),
    ("Hawaii", 21.3069, -157.8583),
    ("Idaho", 43.6150, -116.2023),
    ("Illinois", 39.7983, -89.6544),
    ("Indiana", 39.7684, -86.1580),
    ("Iowa", 41.5868, -93.6250),
    ("Kansas", 39.0558, -95.6890),
    ("Kentucky", 38.1975, -84.8630),
    ("Louisiana", 30.6954, -91.1395),
    ("Maine", 44.3106, -69.7795),
    ("Maryland", 38.9784, -76.4922),
    ("Massachusetts", 42.3601, -71.0589),
    ("Michigan", 42.7325, -84.5555),
    ("Minnesota", 44.9537, -93.0900),
    ("Mississippi", 32.2988, -90.1848),
    ("Missouri", 38.5767, -92.1735),
    ("Montana", 46.5891, -112.0391),
    ("Nebraska", 40.8136, -96.7026),
    ("Nevada", 39.1638, -119.7674),
    ("New Hampshire", 43.2081, -71.5375),
    ("New Jersey", 40.2170, -74.7429),
    ("New Mexico", 35.6868, -105.9378),
    ("New York", 42.6526, -73.7562),
    ("North Carolina", 35.7796, -78.6382),
    ("North Dakota", 48.8148, -99.7930),
    ("Ohio", 39.9612, -82.9988),
    ("Oklahoma", 35.4676, -97.5164),
    ("Oregon", 44.9429, -123.0351),
    ("Pennsylvania", 40.2737, -76.8844),
    ("Rhode Island", 41.8236, -71.4222),
    ("South Carolina", 34.0007, -81.0348),
    ("South Dakota", 44.2998, -100.3499),
    ("Tennessee", 36.1627, -86.7816),
    ("Texas", 30.2672, -97.7431),
    ("Utah", 40.7608, -111.8910),
    ("Vermont", 44.2601, -72.5754),
    ("Virginia", 37.5407, -77.4360),
    ("Washington", 47.0379, -122.9007),
    ("West Virginia", 38.3498, -81.6326),
    ("Wisconsin", 43.0731, -89.4012),
    ("Wyoming", 41.1400, -104.8202)
]

# --------------------------
# Kanada Eyaletleri/Provinceleri
# --------------------------
canada_provinces = [
    ("Alberta", 53.5461, -113.4938),
    ("British Columbia", 48.4284, -123.3656),
    ("Manitoba", 49.8951, -97.1384),
    ("New Brunswick", 46.5653, -66.4619),
    ("Newfoundland and Labrador", 47.5615, -52.7126),
    ("Nova Scotia", 44.6488, -63.5752),
    ("Ontario", 51.2538, -85.3232),
    ("Prince Edward Island", 46.2382, -63.1311),
    ("Quebec", 46.8139, -71.2082),
    ("Saskatchewan", 52.1332, -106.6700),
    ("Northwest Territories", 62.4540, -114.3718),
    ("Nunavut", 64.2008, -85.4166),
    ("Yukon", 60.7212, -135.0568)
]

# --------------------------
# Meksika Eyaletleri
# --------------------------
mexico_states = [
    ("Aguascalientes", 21.8853, -102.2916),
    ("Baja California", 32.6245, -115.4523),
    ("Baja California Sur", 24.1426, -110.3106),
    ("Campeche", 19.8301, -90.5349),
    ("Chiapas", 16.7569, -93.1292),
    ("Chihuahua", 28.6353, -106.0886),
    ("Coahuila", 28.7043, -100.4979),
    ("Colima", 19.2433, -103.7240),
    ("Durango", 24.0277, -104.6532),
    ("Guanajuato", 21.0190, -101.2574),
    ("Guerrero", 17.5466, -99.5033),
    ("Hidalgo", 20.0911, -98.7620),
    ("Jalisco", 20.6767, -103.3476),
    ("Mexico City", 19.4326, -99.1332),
    ("Michoacán", 19.7030, -101.1842),
    ("Morelos", 18.6816, -99.1013),
    ("Nayarit", 21.5090, -104.8957),
    ("Nuevo León", 25.6866, -100.3161),
    ("Oaxaca", 17.0732, -96.7266),
    ("Puebla", 19.0413, -98.2062),
    ("Querétaro", 20.5888, -100.3899),
    ("Quintana Roo", 20.6296, -87.0739),
    ("San Luis Potosí", 22.1566, -100.9855),
    ("Sinaloa", 24.8076, -107.3940),
    ("Sonora", 29.1027, -110.9776),
    ("Tabasco", 17.9939, -92.9478),
    ("Tamaulipas", 24.1568, -98.8032),
    ("Tlaxcala", 19.3139, -98.2404),
    ("Veracruz", 19.1738, -96.1342),
    ("Yucatán", 20.9674, -89.5926),
    ("Zacatecas", 22.7709, -102.5832)
]

# --------------------------
# Tüm lokasyonları birleştir
# --------------------------
all_locations = usa_states + canada_provinces + mexico_states

# --------------------------
# Veritabanına ekle (boylam, enlem sırası)
# --------------------------
for name, lat, lon in all_locations:
    try:
        cursor.execute(
            "INSERT INTO situation (city_name, longitude, latitude , timestamp) VALUES (%s, %s, %s, %s)",
            (name, lon, lat, datetime.now())  # Dikkat: longitude önce, latitude sonra
        )
    except mysql.connector.Error as err:
        print(f"⚠ Hata eklerken: {err} ({name})")
        continue

conn.commit()
cursor.close()
conn.close()

print("✅ Tüm ABD, Kanada ve Meksika eyaletleri nasa_project.locations tablosuna (boylam, enlem) sırasıyla eklendi.")
