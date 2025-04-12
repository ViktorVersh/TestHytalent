from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base  # Импортируем Base из отдельного файла


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String(100))

    # Отложенная настройка relationship
    reservations = relationship("Reservation", back_populates="table")
