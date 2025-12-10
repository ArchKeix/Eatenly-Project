from fastapi import APIRouter
from models.user_model import UserPreference
from services.service_personalize import save_preference

router_personalize = APIRouter(prefix="/personalize", tags=["personalize"])


@router_personalize.post("/{id_user}/preference")
async def set_preference(id_user: str, payload: UserPreference):
    return await save_preference(id_user, payload)
