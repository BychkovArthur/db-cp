from fastapi import APIRouter

from app.routers import user, battle_type, subscribe
from app.settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(user.router)
api_router.include_router(battle_type.router)
api_router.include_router(subscribe.router)
