# tempo service dosyası açmazsa bunu çalıştır ama sadece no2 için
import datetime as dt
from harmony import BBox, Client, Collection, Request
import os
from dotenv import load_dotenv
import traceback

# --------------------------
# .env yükle (Earthdata kullanıcı adı/şifre)
# --------------------------
load_dotenv()
USERNAME = os.getenv("EARTHDATA_USER")
PASSWORD = os.getenv("EARTHDATA_PASS")

if not USERNAME or not PASSWORD:
    raise ValueError("Earthdata kullanıcı adı ve şifresi .env dosyasında bulunamadı!")

# --------------------------
# Harmony client
# --------------------------
harmony_client = Client(auth=(USERNAME, PASSWORD))

# --------------------------
# Kullanılacak koleksiyonlar
# --------------------------
gases = {
    "no2": [("NO2_L3", "C3685896708-LARC_CLOUD")]
}

# --------------------------
# Manuel tarih (örnek: dünün tarihi)
# --------------------------
# Örnek: 26 Eylül 2025
start_time = dt.datetime.strptime("26/09/2025", "%d/%m/%Y").replace(tzinfo=dt.timezone.utc)
stop_time  = dt.datetime.strptime("27/09/2025", "%d/%m/%Y").replace(tzinfo=dt.timezone.utc)

# --------------------------
# ABD bounding box (daha dar)
# --------------------------
xmin, ymin, xmax, ymax = -125, 24, -66, 50
bbox = BBox(xmin, ymin, xmax, ymax)

# --------------------------
# Her gaz için veri indir
# --------------------------
for gas_key, gas_list in gases.items():
    for gas_name, collection_id in gas_list:
        try:
            print(f"\n📡 {gas_name} için veri indiriliyor...")

            # Harmony request
            request = Request(
                collection=Collection(id=collection_id),
                temporal={"start": start_time, "stop": stop_time},
                spatial=bbox
                # format parametresi kaldırıldı çünkü NO2 L3 bunu desteklemiyor
            )

            # Job gönder
            job_id = harmony_client.submit(request)
            print(f"📄 Harmony Job ID: {job_id}")

            # Job bitmesini bekle
            harmony_client.wait_for_processing(job_id)

            # Dosyaları indir
            results = list(harmony_client.download_all(job_id))
            print(f"✅ {gas_name}: {len(results)} dosya indirildi")

            # Dosya yollarını yazdır
            for idx, future_file in enumerate(results, start=1):
                file_path = future_file.result()
                print(f"📂 [{idx}] Dosya indirildi: {file_path}")

        except Exception as e:
            print(f"⚠ {gas_name} hata: {e}")
            traceback.print_exc()
