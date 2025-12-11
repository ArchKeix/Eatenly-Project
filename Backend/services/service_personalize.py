from models.user_model import UserPersonalize
from db_conf import users_collect


async def save_personalize(id_user: str, payload: UserPersonalize):
    personalize_data = payload.model_dump()

    result = await users_collect.update_one(
        {"id_user": id_user}, {"$set": personalize_data}
    )

    if result.modified_count == 0:
        return {"message": "User tidak ditemukan atau tidak ada perubahan data."}
    nama_panggilan = personalize_data.get("nama_panggilan")
    umur = personalize_data.get("umur")
    jenis_kelamin = personalize_data.get("jenis_kelamin")
    riwayat_penyakit = personalize_data.get("riwayat_penyakit")
    preferensi = personalize_data.get("preferensi")
    return {
        "message": "Data personalisasi pengguna berhasil disimpan.",
        "nama_panggilan": nama_panggilan,
        "umur": umur,
        "jenis_kelamin": jenis_kelamin,
        "riwayat_penyakit": riwayat_penyakit,
        "preferensi": preferensi,
    }
