from fastapi import FastAPI

from app.backend.db import Base, engine
from routers import table, reservation
import logging
from contextlib import asynccontextmanager

from sqlalchemy import inspect


# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при старте приложения
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка при завершении
    logger.info("Application shutdown")


# Инициализация FastAPI с lifespan-менеджером
app = FastAPI(
    title="Restaurant Reservation API",
    description="API для бронирования столиков в ресторане",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def welcome():
    """
    Приветственная страница API для бронирования столиков
    """
    return {"message": "Добро пожаловать в систему бронирования столиков ресторана"}


# Подключение роутеров
app.include_router(table.router)

app.include_router(reservation.router)

if __name__ == "__main__":
    import uvicorn

    # Конфигурация сервера
    server_config = {
        "app": "main:app",
        "host": "127.0.0.1",
        "port": 8000,
        "reload": True,
        "log_level": "info"
    }

    logger.info("Starting server...")
    uvicorn.run(**server_config)
