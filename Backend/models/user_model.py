from pydantic import BaseModel, EmailStr, Field
from typing import Optional

"""pydantic models digunakan untuk validasi data saat menerima request dan response dari API"""


class UserSignup(BaseModel):  # -> Untuk Signup
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):  # -> Untuk Login
    email: EmailStr
    password: str


class UserPersonalize(BaseModel):  # -> Untuk Personalisasi User (saat isi formulir)
    id_user: str
    nama_panggilan: str
    umur: str
    jenis_kelamin: str
    riwayat_penyakit: Optional[str] = None
    preferensi: Optional[str] = None


class User(BaseModel):  # -> Model User di Database
    id_user: str
    email: EmailStr
    password: str
    nama_panggilan: str
    umur: str
    jenis_kelamin: str
    riwayat_penyakit: Optional[str] = None
    preferensi: Optional[str] = None
