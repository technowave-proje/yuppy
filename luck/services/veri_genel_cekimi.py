# bu kod o2o2 , o3 ve hcho için çekiyor
import datetime as dt
from harmony import BBox, Client, Collection, Request
import os
from dotenv import load_dotenv

# --------------------------
# .env yükle (Earthdata kullanıcı adı/şifre)
# --------------------------
load_dotenv()
USERNAME = os.getenv("EARTHDATA_USER")
PASSWORD = os.getenv("EARTHDATA_PASS")

# Harmony client
harmony_client = Client(auth=(USERNAME, PASSWORD))

# --------------------------
# Kullanılacak koleksiyonlar
# --------------------------
gases = {

    "o2-o2": [("O2-O2_L3", "C3685896149-LARC_CLOUD")],
    "o3": [("O3_L3", "C3685896402-LARC_CLOUD")],
    "hcho": [("HCHO_L3", "C3685897141-LARC_CLOUD")],

    "no2": [("NO2_L3", "C3685896708-LARC_CLOUD")],
    
}

# --------------------------
# Manuel tarih (örnek: 26/09/2025)
# --------------------------
start_time = dt.datetime.strptime("25/09/2025 00:00:00", "%d/%m/%Y %H:%M:%S").replace(tzinfo=dt.timezone.utc)
stop_time = dt.datetime.strptime("25/09/2025 23:59:59", "%d/%m/%Y %H:%M:%S").replace(tzinfo=dt.timezone.utc)

# --------------------------
# ABD bounding box
# --------------------------
xmin, ymin, xmax, ymax = -170, 14, -50, 72
bbox = BBox(xmin, ymin, xmax, ymax)

# --------------------------
# Her gaz için veri indir (sadece indir, açma!)
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
            )

            job_id = harmony_client.submit(request)
            harmony_client.wait_for_processing(job_id)
            print(f"Harmony Job ID: {job_id}")

            results = list(harmony_client.download_all(job_id))
            print(f"✅ {gas_name}: {len(results)} dosya indirildi")

            # Dosya yollarını yazdır
            for idx, future_file in enumerate(results, start=1):
                file_path = future_file.result()
                print(f"📂 [{idx}] Dosya indirildi: {file_path}")

        except Exception as e:
            print(f"⚠ {gas_name} hata: {e}")


