# ----------------------------------------------------------------------- #
#                               LIBRARIES                                 #
# ----------------------------------------------------------------------- #

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
from dotenv import load_dotenv
import base64
import os
import re

# ----------------------------------------------------------------------- #
# Load .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# ----------------------------------------------------------------------- #

# Inisialisasi model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6,
    max_output_tokens=1500,
)


# ----------------------------------------------------------------------- #
# Encode gambar ke base64
with open("produk3.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

# ----------------------------------------------------------------------- #
# Setup Pesan dan Task
messages = [
    SystemMessage(
        content=(
            """
            Anda adalah asisten AI ahli dalam menganalisis produk konsumsi kemasan dari gambar.
            Gunakan framework berikut untuk menjawab:
            1. Kandungan gizi/komposisi produk
            2. Kesehatan komposisi produk
            3. Rekomendasi konsumsi produk
            4. List referensi sumber jawaban (Sumber: scholar.google.com, sciencedirect.com, nature.com, atau nih.gov) 
               dengan format nomor urut dan link

            Note:
            - Jika tidak ada nama merek, buat dugaan berdasarkan visual kemasan.
            - Hasil teks analisa harus rapi, tanpa simbol aneh seperti *, -, #, [], dll.
            - Gunakan referensi dari jurnal ilmiah 3 tahun terakhir
            - Berikan hasil analisa ringkas tapi lengkap, detail, dan valid.
            """
        )
    ),
    HumanMessage(
        content=[
            {"type": "text", "text": "Analisa produk berikut:"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"},
            },
        ]
    ),
]

# ----------------------------------------------------------------------- #
# Jalankan model
response = model.invoke(messages)
response = re.sub(r"\*+", "", response.content)
response = response.strip()
print(response)
