import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import requests
import os
from app import crud
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# -----------------------------
# 1️⃣ Dosya yolları
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "aqi_model.pkl")

# -----------------------------
# 2️⃣ Model eğitme
# -----------------------------

def train_and_save_model(csv_path= CSV_PATH, model_path=MODEL_PATH):
    # Debug: CSV dosyasını kontrol et
    print("CSV yolu:", csv_path)
    import os
    print("Dosya var mı:", os.path.exists(csv_path))
    if os.path.exists(csv_path):
        print("Boyut:", os.path.getsize(csv_path))
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            print("İlk 200 karakter:\n", f.read(200))

    # CSV'yi oku
    data = pd.read_csv(csv_path, encoding = "utf-8-sig")

def train_and_save_model(csv_path=CSV_PATH, model_path=MODEL_PATH):
    data = pd.read_csv(csv_path, encoding="utf-8-sig")
    X = data.drop("activity_ok", axis=1)
    y = data["activity_ok"]

    categorical_cols = ["age_group", "pregnancy_status", "respiratory_disease", "cardio_disease", "activity"]
    X = pd.get_dummies(X, columns=categorical_cols)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"✅ Model başarıyla eğitildi ve kaydedildi: {model_path}")

# -----------------------------
# 3️⃣ Model yükleme
# -----------------------------
try:
    model = joblib.load(MODEL_PATH)
    print(f"📂 Kayıtlı model yüklendi: {MODEL_PATH}")
except:
    print("⚠️ Model bulunamadı, eğitim başlatılıyor...")
    train_and_save_model()
    model = joblib.load(MODEL_PATH)

# -----------------------------
# 4️⃣ API anahtarları (env’den alınıyor)
# -----------------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TEMPO_API_URL = os.getenv("TEMPO_API_URL")
TEMPO_TOKEN = os.getenv("TEMPO_TOKEN")

# -----------------------------
# 5️⃣ Hava durumu verisi
# -----------------------------
def get_realtime_weather(lat: float, lon: float):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather = requests.get(weather_url).json()

    air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    air = requests.get(air_url).json()

    return {
        "temperature": weather["main"]["temp"],
        "humidity": weather["main"]["humidity"],
        "wind_speed": weather["wind"]["speed"],
        "rain": "rain" in weather,
        "aqi": air["list"][0]["main"]["aqi"],
        "pm25": air["list"][0]["components"]["pm2_5"]
    }

def get_tempo_data(lat: float, lon: float):
    headers = {"Authorization": f"Bearer {TEMPO_TOKEN}"}
    params = {"latitude": lat, "longitude": lon}
    resp = requests.get(TEMPO_API_URL, headers=headers, params=params).json()
    return {
        "aqi": resp.get("aqi", 2),
        "pm25": resp.get("pm25", 10.0)
    }


class Predictor:
    def __init__(self):
        self.model_path = MODEL_PATH
        print(f"📂 Kayıtlı model yüklendi: {os.path.abspath(self.model_path)}")
        self.model = joblib.load(self.model_path)

    def predict(self, features: dict):
        """
        features dict → model inputa uygun hale getirilmeli
        Örnek: {"temperature": 25, "humidity": 60, ...}
        """
        X = [list(features.values())]
        return self.model.predict(X)[0]
