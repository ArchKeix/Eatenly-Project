# ----------------------------------------------------------------------- #
#                               LIBRARIES                                 #
# ----------------------------------------------------------------------- #

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from PIL import Image
import os
import base64
import re
import io


# ----------------------------------------------------------------------- #

# Load .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# ----------------------------------------------------------------------- #


# Define Kompresi Image ke Base64
def img_compress_b64(img_product: bytes) -> str:

    img = Image.open(io.BytesIO(img_product))
    MaxSize = (1024, 1024)
    img.thumbnail(MaxSize, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_product = buffered.getvalue()

    # Encode Img ke Base64 (Gemini hanya bisa terima base64 untuk image)
    img_b64 = base64.b64encode(img_product).decode("utf-8")
    return img_b64


# Define Fungsi AI Analyst
async def AI_Analyst(img_product: bytes, personalize: str) -> str:

    # Compress & Convert image ke base64
    img_b64 = img_compress_b64(img_product)

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
                f"""
            Anda adalah asisten AI ahli dalam menganalisis produk konsumsi kemasan dari gambar.
            Berikut merupakan tugas anda dalam menganalisis produk konsumsi kemasan:
            1. Kandungan gizi/komposisi produk
            2. Kesehatan komposisi produk
            3. Rekomendasi konsumsi produk
            4. List referensi 3 sumber jurnal ilmiah terbaru dari tahun 2023-2025 yang digunakan
               tanpa menyertakan penjelasannya dan format tanpa penomoran.

            Template jawaban:
            🍕 Produk : (jika ada merek, sebutkan nama mereknya. Jika tidak ada, buat dugaan berdasarkan visual kemasan)
            
            😽 Rekomendasi konsumsi produk : (apakah direkomendasikan /tidak direkomendasikan untuk dikonsumsi)
            
            🍽️ Status Halal: (berikan respon cukup produk ini halal/haram)
            
            👨‍🔬 Kandungan gizi/komposisi produk :
            (Dibawah sini berisi analisisnya berdasarkan dari komposisi produk yang terlihat pada gambar kemasan.) 
            
            💪 Kesehatan komposisi produk : 
            (Berikan analisis terkait semua komposisi produk yang terkait dengan resiko jangka pendek dan panjang
            terhadap kondisi tubuh sesuai dengan {personalize} user dan Kehalalan produk berdasarkan 
            komposisi yang ada pada kemasan produk dan sertakan jika ada kandungan yang meragukan)

            📚 Referensi : 
            1. (judul jurnal ilmiah 1 beserta tahun)
            2. (judul jurnal ilmiah 2 beserta tahun)
            3. (judul jurnal ilmiah 3 beserta tahun)
 
            Note:
            - Jika gambar produk tidak jelas, berikan satu kalimat: "Maaf, gambar kurang jelas untuk dianalisa."
              Sedangkan jika gambar produk selain produk kemasan, berikan satu kalimat: "Maaf, gambar bukan produk konsumsi kemasan."
            - Selalu buat analisa panjang, rinci, dan tidak boleh singkat.
            - Hindari penulisan poin-poin, gunakan paragraf panjang terstruktur hanya pada template
              kesehatan komposisi produk.


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
