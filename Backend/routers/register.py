# routers/register.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from passlib.context import CryptContext
from db_conf import users_collect

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    username: Optional[str] = Field(default=None)


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    username: str
    is_active: bool


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest):
    # generate username if missing
    uname = (payload.username or payload.email.split("@")[0]).strip()

    # re-validate generated username length
    if not (3 <= len(uname) <= 32):
        raise HTTPException(
            status_code=422, detail="Username tidak valid (min 3, max 32)"
        )

    # check duplicates
    existing = await users_collect.find_one(
        {"$or": [{"email": payload.email.lower()}, {"username": uname}]}
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email atau username sudah terdaftar",
        )

    # hash password
    password_hash = pwd_context.hash(payload.password)

    # save user
    doc = {
        "email": payload.email.lower(),
        "username": uname,
        "password_hash": password_hash,
        "is_active": True,
    }
    result = await users_collect.insert_one(doc)

    return UserPublic(
        id=str(result.inserted_id),
        email=doc["email"],
        username=doc["username"],
        is_active=doc["is_active"],
    )
