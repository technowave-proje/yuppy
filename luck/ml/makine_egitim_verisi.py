import pandas as pd

# CSV’leri oku
no2 = pd.read_csv("state_avg_no2.csv")
o2o2 = pd.read_csv("state_avg_o2o2.csv")
o3 = pd.read_csv("state_avg_o3.csv")
hcho = pd.read_csv("state_avg_hcho.csv")

df = no2.copy()

# Ortak kolonlara göre birleştir
df = df.merge(o3, on=["state_name","date"])
df = df.merge(hcho, on=["state_name","date"])
df = df.merge(o2o2, on=["state_name","date"])

# Tek CSV olarak kaydet
df.to_csv("training_data.csv", index=False)
