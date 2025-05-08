from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.routers.api_router import api_router
from app.settings import settings
from app.services.royale_api_client import ClashRoyaleApiService
from app.services.notification_service import setup_battle_notifications
from app.services.redis_service import redis_service

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db import AsyncSessionFactory
import asyncio

app = FastAPI(title=settings.PROJECT_NAME, version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    async def scheduled_fetch_battles():
        async with AsyncSessionFactory() as session:
            await ClashRoyaleApiService.fetch_battles(session)
    
    async def scheduled_fetch_user_detailed_info():
        async with AsyncSessionFactory() as session:
            await ClashRoyaleApiService.fetch_user_detailed_info(session)
    
    scheduler.add_job(scheduled_fetch_battles, "interval", seconds=60)
    scheduler.add_job(scheduled_fetch_user_detailed_info, "interval", seconds=300)
    scheduler.start()

    # Настраиваем уведомления о боях
    await setup_battle_notifications()
    # Запускаем прослушивание событий в фоновом режиме
    asyncio.create_task(redis_service.start_listening())

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()