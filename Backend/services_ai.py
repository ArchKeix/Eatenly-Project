# ----------------------------------------------------------------------- #
#                               LIBRARIES                                 #
# ----------------------------------------------------------------------- #

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from PIL import Image
import base64
import os
import re
import io

# ----------------------------------------------------------------------- #

# Load .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# ----------------------------------------------------------------------- #


# Define Fungsi AI Analyst
def AI_Analyst(img_product: bytes) -> str:

    # Encode Img ke Base64 (Gemini hanya bisa terima base64 untuk image)
    img = Image.open(io.BytesIO(img_product))
    mime_type = Image.MIME.get(img.format)
    MaxSize = (1024, 1024)
    img.thumbnail(MaxSize, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_product = buffered.getvalue()
    img_b64 = base64.b64encode(img_product).decode("utf-8")

    # Inisialisasi model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.5,
        max_output_tokens=5000,
    )
    # Inisialisasi Task sistem & human message
    messages = [
        SystemMessage(
            content=(
                """
            Anda adalah asisten AI ahli dalam menganalisis produk konsumsi kemasan dari gambar.
            Gunakan framework berikut untuk menjawab:
            1. Kandungan gizi/komposisi produk
            2. Kesehatan komposisi produk
            3. Rekomendasi konsumsi produk
            4. List referensi 3 sumber jurnal ilmiah terbaru yang digunakan
               tanpa menyertakan penjelasannya

            Note:
            - Jika tidak ada nama merek, buat dugaan berdasarkan visual kemasan.
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
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                },
            ]
        ),
    ]

    try:
        print(f"\n--- Menjalankan AI ---")
        response = model.invoke(messages)
        response = re.sub(r"(\*\*|__)", "", response.content)
        # Normalisasi spasi
        response = re.sub(r"[ \t]+", " ", response)
        # Rapikan line break
        response = re.sub(r"\n{2,}", "\n\n", response)

        return {"status": "success", "analysis": response}

    except Exception as e:
        response = f"Maaf, terjadi kesalahan {e}."
        return {"status": "error", "analysis": response}
