# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Url MongoDB dari .env
uri = os.getenv("mongo_url")

# Connect to MongoDB
client = AsyncIOMotorClient(uri)

# Database Eatenly_Project
db = client["Eatenly_Project"]

# Collection Eatenly_Project
users_collect = db["user"]
produk_collect = db["produk"]
kondisi_kesehatan_collect = db["kondisi_kesehatan"]
riwayat_analisis_collection = db["riwayat_analisis"]
preferensi_collect = db["preferensi"]

preferensi_pengguna_collect = db["preferensi_pengguna"]
profile_kesehatan_pengguna_collection = db["profile_kesehatan_pengguna"]

# Test connection
try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Test CRUD
result = riwayat_analisis_collection.insert_one(
    {
        "id_riwayat": 12,
        "hasil_analisa": "produk yupi ga aman dikonsumsi oleh penderita diabetes",
        "rekomendasi_produk": "Produk ini tidak aman dikonsumsi oleh penderita diabetes. Sebaiknya pilih produk dengan kandungan gula yang lebih rendah atau tanpa gula tambahan.",
    }
)


# r = users_collect.find()
# print(list(r))
