# routers/register.py

from fastapi import APIRouter, HTTPException, status
from models.user_model import UserSignup
from services.services_register import signup

router_regis = APIRouter(prefix="/register", tags=["register"])


@router_regis.post("/")
async def user_regis(payload: UserSignup):
    """
    Endpoint untuk registrasi user baru
    """
    try:
        result = await signup(payload)  # panggil service signup
        return result
    except HTTPException as e:
        # Jika ada error, lemparkan HTTPException kembali
        raise e
    except Exception as e:
        # Error lain, misal koneksi DB gagal
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
