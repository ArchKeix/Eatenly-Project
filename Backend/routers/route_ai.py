from fastapi import APIRouter, Header, HTTPException, UploadFile, File
from db_conf import users_collect, riwayat_analisis_collection
from services.service_ai import AI_Analyst
import jwt
import os
from fastapi.responses import StreamingResponse
from datetime import datetime

router_ai = APIRouter(prefix="/ai", tags=["ai"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


@router_ai.post("/")
async def set_ai(
    img_product: UploadFile = File(...), Authorization: str = Header(None)
):

    if not Authorization:
        raise HTTPException(status_code=401, detail="Token diperlukan")
    else:
        token = Authorization.split(" ")[1]  # Bearer <token>
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            raise HTTPException(status_code=401, detail="Token invalid atau expired")

        id_user = decoded["id_user"]

        # Ambil preferensi user
        user = await users_collect.find_one({"id_user": id_user})

        # Buat personalisasi
        pref = user.get("preferensi")
        riwayat = user.get("riwayat_penyakit")

        personalize = f"""
        1. Preferensi user: {pref}
        2. Riwayat penyakit user: {riwayat}
        """

        # Img byte dari UploadFile
        img_product = await img_product.read()

        answer = await AI_Analyst(img_product, personalize)

        ai_data = answer["response_json"]

        # Buat ID unik (timestamp milidetik)
        new_id_riwayat = int(datetime.now().timestamp() * 1000)

        data_to_save = {
            "id_riwayat": new_id_riwayat,
            "id_user": id_user,
            "nama_produk": ai_data.get("product_name", "Tidak Teridentifikasi"),
            "preferensi": pref,
            "rekomendasi_produk": ai_data.get("recommendation", "Netral"),
            "status_halal": ai_data.get("halal_status", "Unknown"),
            "tanggal_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        try:
            await riwayat_analisis_collection.insert_one(data_to_save)
        except Exception as e:
            print(f"Gagal menyimpan riwayat: {e}")

        #         # Hapus _id objectID mongo untuk return JSON
        if "_id" in data_to_save:
            del data_to_save["_id"]

    return {
        "id_user": id_user,
        "status": answer["status"],
        "analysis": answer["analysis"],
        "response_json": answer["response_json"],
    }


# from fastapi import APIRouter, Header, HTTPException, UploadFile, File
# from db_conf import users_collect, riwayat_analisis_collection
# from services.service_ai import AI_Analyst
# import jwt
# import os
# from datetime import datetime

# router_ai = APIRouter(prefix="/ai", tags=["ai"])

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = "HS256"


# @router_ai.post("/")
# async def set_ai(
#     img_product: UploadFile = File(...), Authorization: str = Header(None)
# ):

#     if not Authorization:
#         raise HTTPException(status_code=401, detail="Token diperlukan")
#     else:
#         # --- 1. Decode Token & Ambil Data User ---
#         token = Authorization.split(" ")[1]
#         try:
#             decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         except:
#             raise HTTPException(status_code=401, detail="Token invalid atau expired")

#         id_user = decoded["id_user"]

#         # Ambil preferensi user
#         user = await users_collect.find_one({"id_user": id_user})
#         if not user:
#             raise HTTPException(status_code=404, detail="User tidak ditemukan")

#         pref = user.get("preferensi", "-")
#         riwayat = user.get("riwayat_penyakit", "-")

#         personalize = f"""
#         1. Preferensi user: {pref}
#         2. Riwayat penyakit user: {riwayat}
#         """

#         # --- 2. Proses AI ---
#         file_content = await img_product.read()
#         answer = await AI_Analyst(file_content, personalize)

#         if answer["status"] == "error":
#             raise HTTPException(status_code=500, detail=answer["analysis"])

#         # --- 3. SIMPAN KE DATABASE (Format Ringkas) ---
#         ai_data = answer["response_json"]

#         # Buat ID unik (timestamp milidetik)
#         new_id_riwayat = int(datetime.now().timestamp() * 1000)

#         data_to_save = {
#             "id_riwayat": new_id_riwayat,
#             "id_user": id_user,
#             "nama_produk": ai_data.get("product_name", "Tidak Teridentifikasi"),
#             "preferensi": pref,
#             "rekomendasi_produk": ai_data.get("recommendation", "Netral"),
#             # [PERUBAHAN DISINI]
#             # Ganti 'hasil_analisis' (full text) jadi 'status_halal' (singkat)
#             "status_halal": ai_data.get("halal_status", "Unknown"),
#             "tanggal_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }

#         try:
#             await riwayat_analisis_collection.insert_one(data_to_save)
#         except Exception as e:
#             print(f"Gagal menyimpan riwayat: {e}")

#         # Hapus _id objectID mongo untuk return JSON
#         if "_id" in data_to_save:
#             del data_to_save["_id"]

#         # Kembalikan data yang persis disimpan di DB
#         return {
#             "status": "success",
#             "message": "Analisis berhasil dan tersimpan",
#             "data": data_to_save,
#         }

# --- Endpoint untuk mengambil riwayat scan ---
@router_ai.get("/history")
async def get_history(Authorization: str = Header(None)):
    
    # 1. Cek Token (Sama seperti fungsi POST)
    if not Authorization:
        raise HTTPException(status_code=401, detail="Token diperlukan")
    
    token = Authorization.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user = decoded["id_user"]
    except:
        raise HTTPException(status_code=401, detail="Token invalid")

    # 2. Ambil data dari MongoDB
    # - Filter berdasarkan id_user
    
    cursor = riwayat_analisis_collection.find({"id_user": id_user}).sort("tanggal_analisis", -1).limit(20)
    
    riwayat_list = []
    async for document in cursor:
        # Hapus _id (ObjectID Mongo) karena tidak bisa di-convert ke JSON langsung
        if "_id" in document:
            del document["_id"]
        riwayat_list.append(document)

    # 3. Kembalikan data ke Frontend
    return {"status": "success", "data": riwayat_list}