from fastapi import APIRouter
from models.user_model import UserPersonalize
from services.service_personalize import save_personalize

router_personalize = APIRouter(prefix="/personalize", tags=["personalize"])


@router_personalize.post("/{id_user}")
async def set_personalize(id_user: str, payload: UserPersonalize):
    return await save_personalize(id_user, payload)
