from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from db_conf import users_collect
from models.user_model import UserSignup
import uuid


# bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define Fungsi Signup
async def signup(payload: UserSignup):
    # Cek apakah email sudah terdaftar
    isExist = await users_collect.find_one({"email": payload.email})
    if isExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Akun sudah terdaftar",
        )
    else:
        # Melakukan hash pada password sebelum disimpan ke database
        hashed_password = pwd_context.hash(payload.password)  # Hashing pada pw
        userSignup_Payload = payload.model_dump()  # Ubah pydantic model ke dict
        userSignup_Payload["password"] = (
            hashed_password  # Ganti password asli dengan hashed
        )
        userSignup_Payload.pop(
            "confirm_password"
        )  # Hapus confirm_password dari payload

        # Generate UUID untuk id
        userSignup_Payload["id_user"] = str(uuid.uuid4())

        # Memasukkan data payload signup user ke database
        await users_collect.insert_one(userSignup_Payload)

        return {
            "message": "Akun berhasil didaftarkan",
            "email": str(userSignup_Payload["email"]),
            "id_user": str(userSignup_Payload["id_user"]),
        }
