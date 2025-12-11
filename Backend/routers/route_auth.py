from fastapi import APIRouter, HTTPException, status
from models.user_model import UserLogin
from services.service_auth import login

router_auth = APIRouter(prefix="/auth", tags=["auth"])


@router_auth.post("/login")
async def user_login(payload: UserLogin):
    """
    Endpoint untuk login user
    """
    try:
        result = await login(payload)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
