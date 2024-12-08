from fastapi import Depends, HTTPException
from app.services.user import CurrentUserDep
from app.models.user import User
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
import subprocess
import os
import datetime
from loguru import logger

from app.schemas.admin import RestoreDumpRequest

router = APIRouter(prefix="/admin", tags=["Admin"])


# Путь для сохранения дампов
DUMP_DIR = "/dumps/"


@router.post("/dump")
async def create_database_dump():
    """
    Создание дампа БД с данными и структурой всех таблиц.
    """
    # Формируем имя файла дампа
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"dump_{now}.sql"
    dump_path = os.path.join(DUMP_DIR, filename)

    # Убедимся, что директория для дампов существует
    if not os.path.exists(DUMP_DIR):
        os.makedirs(DUMP_DIR)

    try:
        # Формируем корректную команду для создания полного дампа
        command = [
            "pg_dump", 
            "-U", "postgres",  # Пользователь
            "-h", "db",  # Хост
            "-d", "fastdb",
            "--format=c",  # Формат 'custom' для совместимости с pg_restore
            "--file", dump_path  # Путь для сохранения дампа
        ]
        
        # Выполняем команду
        subprocess.run(command, check=True, env={"PGPASSWORD": os.environ.get("POSTGRES_PASSWORD")})
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Dump failed: {e}")
        raise HTTPException(status_code=500, detail="Dump creation failed")

    logger.info(f"Dump successfully created: {dump_path}")
    return {"message": f"Dump created successfully: {filename}", "dump_file": dump_path}


@router.post("/restore")
async def restore_database_from_dump(request: RestoreDumpRequest):
    """
    Очищаем БД и восстанавливаем данные из дампа.
    """
    dump_path = os.path.join(DUMP_DIR, request.filename)

    if not os.path.exists(dump_path):
        raise HTTPException(status_code=404, detail="Dump file not found")

    try:
        # Очищаем базу данных
        logger.info("Clearing database schema...")
        clear_command = [
            "psql", "-U", "postgres", "-h", "db",
            "-c", "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        ]
        subprocess.run(clear_command, check=True, env={"PGPASSWORD": os.environ.get("POSTGRES_PASSWORD")})

        # Восстанавливаем данные из дампа
        logger.info("Restoring database from dump...")
        restore_command = [
            "pg_restore", "--format=c",
            "-U", "postgres",
            "-d", "fastdb", "-h", "db", "-c",
            dump_path
        ]
        subprocess.run(restore_command, check=True, env={"PGPASSWORD": os.environ.get("POSTGRES_PASSWORD")})
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Restore failed: {e}")
        raise HTTPException(status_code=500, detail="Restore failed")
    
    logger.info(f"Database cleared and restored from: {request.filename}")
    return {"message": f"Database cleared and restored from {request.filename}"}

@router.post("/dumps")
async def list_database_dumps():
    
    dump_dir = "/dumps/"
    if not os.path.exists(dump_dir):
        return {"dumps": []}
    
    files = os.listdir(dump_dir)
    dump_files = [f for f in files if f.endswith(".sql")]
    logger.info(f"Dumps available: {dump_files}")
    return {"dumps": dump_files}