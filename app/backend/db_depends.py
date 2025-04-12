from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/reservtable"
SQLALCHEMY_DATABASE_URL = "sqlite:///./reservtable.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# импортируем модели
from app.models.table import Table
from app.models.reservation import Reservation

#  создание базы данных, если ее нет
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
