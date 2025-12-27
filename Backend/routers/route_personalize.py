from fastapi import APIRouter, HTTPException
from models.user_model import UserPersonalize
from services.service_personalize import save_personalize
from db_conf import users_collect

router_personalize = APIRouter(prefix="/personalize", tags=["personalize"])


@router_personalize.post("/{id_user}")
async def set_personalize(id_user: str, payload: UserPersonalize):
    return await save_personalize(id_user, payload)


# --- ENDPOINT 2: UNTUK MENGAMBIL DATA (GET) ---
@router_personalize.get("/{id_user}")
async def get_personalize(id_user: str):
    # 1. Cari data user di database berdasarkan id_user
    user_data = await users_collect.find_one({"id_user": id_user})

    # 2. Jika user tidak ketemu, berikan error 404
    if not user_data:
        raise HTTPException(status_code=404, detail="Data user tidak ditemukan")

    # 3. Jika ketemu, kembalikan data JSON ke dashboard
    return {
        "nama_panggilan": user_data.get("nama_panggilan", "-"),
        "umur": user_data.get("umur", "-"),
        "jenis_kelamin": user_data.get("jenis_kelamin", "-"),
        "riwayat_penyakit": user_data.get("riwayat_penyakit", "-"),
        "preferensi": user_data.get("preferensi", "-"),
    }
