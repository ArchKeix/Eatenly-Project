from models.user_model import UserPersonalize
from db_conf import users_collect


async def save_personalize(id_user: str, payload: UserPersonalize):
    personalize_data = payload.model_dump()

    result = await users_collect.update_one(
        {"id_user": id_user}, {"$set": personalize_data}
    )

    if result.modified_count == 0:
        return {"message": "User tidak ditemukan atau tidak ada perubahan data."}

    return {
        "message": "Data personalisasi pengguna berhasil disimpan.",
        "personalize": personalize_data,
    }
