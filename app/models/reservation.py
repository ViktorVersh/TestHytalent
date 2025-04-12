from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base  # Импортируем Base из отдельного файла


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    custom_name = Column(String(100), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    reservation_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    # Отношение к Table
    table = relationship("Table", back_populates="reservations")