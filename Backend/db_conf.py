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
riwayat_analisis_collection = db["riwayat_analisis"]
