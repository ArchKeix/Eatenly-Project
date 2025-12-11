from fastapi import APIRouter, Header, HTTPException, UploadFile, File
from db_conf import users_collect
from services.service_ai import AI_Analyst
import jwt
import os


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

        # Img byte dari UploadFile
        img_product = await img_product.read()

        # Buat personalisasi
        pref = user.get("preferensi")
        riwayat = user.get("riwayat_penyakit")

        personalize = f"""
        Berikut adalah preferensi user: {pref}
        Berikut adalah riwayat penyakit user: {riwayat}
        """
        answer = await AI_Analyst(img_product, personalize)

    return {
        "status": answer["status"],
        "analysis": answer["analysis"],
        "id_user": id_user,
    }
