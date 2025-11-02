# Langchain 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from google.genai import types
import base64

# Load env
from dotenv import load_dotenv
import os 

# Cleaning text
import re

# Load.env
load_dotenv()

# Mengambil API key dari .env
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Inisialisasi model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

with open("produk2.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

# Setup Task 
message = [
    HumanMessage(
        content=[
            {"type": "text", "text": "Jelaskan isi gambar ini beserta komposisi bahannya serta apakah halal."},
            {"type": "image_url", "image_url": f"data:image/png;base64,{img_b64}"}
        ]
    )
]

# Setup respon
response = model.invoke(message)
clean_response = re.sub(r"\*+", "",response.content)  # hapus semua tanda *
clean_response = clean_response.strip()  # hapus spasi awal/akhir

# Tampilkan respon
print(clean_response)