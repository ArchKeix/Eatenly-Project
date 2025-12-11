from fastapi import HTTPException, status
from passlib.context import CryptContext
from db_conf import users_collect
from models.user_model import UserLogin
import jwt
import datetime
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET KEY
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


async def login(payload: UserLogin):
    # 1. Cari user berdasarkan email
    user = await users_collect.find_one({"email": payload.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email tidak ditemukan. Silakan daftar terlebih dahulu",
        )

    # 2. Verifikasi Password
    if not pwd_context.verify(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password salah"
        )

    # 3. Generate JWT TOKEN
    token_payload = {
        "id_user": user["id_user"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=0.5),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # 4. Return response ke frontend
    return {
        "message": "Login berhasil",
        "token": token,
        "id_user": user["id_user"],
        "email": user["email"],
        "nama_panggilan": user.get("nama_panggilan"),
        "umur": user.get("umur"),
        "jenis_kelamin": user.get("jenis_kelamin"),
        "riwayat_penyakit": user.get("riwayat_penyakit"),
        "preferensi": user.get("preferensi"),
    }
