from models.user_model import UserPreference
from db_conf import users_collect


async def save_preference(id_user: str, payload: UserPreference):
    preference_data = payload.model_dump()

    result = await users_collect.update_one(
        {"id_user": id_user}, {"$set": preference_data}
    )

    if result.modified_count == 0:
        return {"message": "User tidak ditemukan atau tidak ada perubahan data."}

    return {"message": "Preferensi pengguna berhasil disimpan."}
