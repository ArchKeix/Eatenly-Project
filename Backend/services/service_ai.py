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
async def img_compress_b64(img_product: bytes) -> str:

    img = Image.open(io.BytesIO(img_product))
    MaxSize = (512, 512)
    img.thumbnail(MaxSize, Image.Resampling.LANCZOS)
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_product = buffered.getvalue()

    # Encode Img ke Base64 (Gemini hanya bisa terima base64 untuk image)
    img_b64 = base64.b64encode(img_product).decode("utf-8")
    return img_b64


def parse_to_json_structure(text: str) -> dict:
    """
    Parser Logik: Mengubah teks mentah dari AI menjadi Dictionary (JSON Object).
    Regex diperbarui untuk menangkap format dengan EMOJI atau TANPA EMOJI.
    """

    # Default values
    parsed_data = {
        "product_name": "Tidak Teridentifikasi",
        "halal_status": "Unknown",
        "recommendation": "Netral",
    }

    # 1. Ambil Nama Produk
    # Regex: Mencari '🍕 Produk :' ATAU 'Nama Produk :' ATAU 'Produk :'
    # (?: ... ) adalah non-capturing group untuk alternatif pilihan
    match_prod = re.search(r"(?:🍕|Nama)?\s*Produk\s*:\s*(.*)", text, re.IGNORECASE)
    if match_prod:
        parsed_data["product_name"] = match_prod.group(1).strip()

    # 2. Ambil Status Halal
    # Regex: Mencari '🍽️ Status Halal:' ATAU 'Status Halal:'
    match_halal = re.search(r"(?:🍽️|🍽)?\s*Status Halal\s*:\s*(.*)", text, re.IGNORECASE)
    if match_halal:
        parsed_data["halal_status"] = match_halal.group(1).strip()

    # 3. Ambil Rekomendasi
    # Regex: Mencari '😽 Rekomendasi konsumsi produk :' ATAU 'Rekomendasi :'
    # Bagian '(?:konsumsi produk)?' membuatnya opsional
    match_rek = re.search(
        r"(?:😽)?\s*Rekomendasi\s*(?:konsumsi produk)?\s*:\s*(.*)", text, re.IGNORECASE
    )
    if match_rek:
        parsed_data["recommendation"] = match_rek.group(1).strip()

    return parsed_data


# Define Fungsi AI Analyst
async def AI_Analyst(img_product: bytes, personalize: str) -> str:

    # Compress & Convert image ke base64
    img_b64 = await img_compress_b64(img_product)

    # Inisialisasi model
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_output_tokens=4500,
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

            Template Teks:
            🍕 Produk : (jika ada merek, sebutkan nama mereknya. Jika tidak ada, buat dugaan berdasarkan visual kemasan)

            😽 Rekomendasi konsumsi produk : (berikan respon hanya direkomendasikan /tidak disarankan )

            🍽️ Status Halal: (berikan respon hanya halal/haram)

            👨‍🔬 Kandungan gizi/komposisi produk :
            (Dibawah sini berisi analisisnya berdasarkan dari komposisi produk yang terlihat pada gambar kemasan.) 
            
            💪 Kesehatan komposisi produk : 
            (Berikan analisis terkait sesuai dengan {personalize} user dan Kehalalan produk berdasarkan 
            komposisi yang ada pada kemasan produk dan sertakan jika ada kandungan yang meragukan)

            📚 Referensi : 
            1.) 
            2.) 
            3.) 

            Note:
            - Jika gambar produk selain produk konsumsi kemasan, berikan satu kalimat: "Maaf, gambar bukan produk konsumsi kemasan."
            - Berikan analisis jelas dan padat sesuaikan dengan template.
            - Gunakan paragraf panjang terstruktur untuk menjelaskan kesehatan komposisi produk (minimal 500 token) tanpa 
              menggunakan point formating.
            - Wajib ada referensi berformat jurnal ilmiah,tahun.Rentang tahun referensi 2023-2025.

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
        # === Bersihkan jawaban dari model === #
        response = model.invoke(messages)
        response = re.sub(r"(\*\*|__)", "", response.content)
        result_json = parse_to_json_structure(response)
        return {"status": "success", "analysis": response, "response_json": result_json}

    except Exception as e:
        response = f"Maaf, terjadi kesalahan {e}."
        return {"status": "error", "analysis": response, "response_json": None}
