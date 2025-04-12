from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Annotated
from dateutil.relativedelta import relativedelta
from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationResponse, Reserv
from app.backend.db_depends import get_db

router = APIRouter(prefix='/reservations', tags=['Reservations'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/', response_model=list[ReservationResponse])
async def get_all_reservations(db: DbSession):
    """
    Получить список всех бронирований
    """
    result = db.query(Reservation).order_by(Reservation.reservation_time).all()
    return result


@router.post('/', response_model=Reserv, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: Reserv, db: DbSession):
    """
    Создать новое бронирование

    Проверяет:
    - Существование столика
    - Время брони в будущем но не более чем на 30 дней вперед
    - Положительную длительность
    - Отсутствие конфликтов с другими бронированиями
    """
    # Проверка существования столика
    if not db.query(Table).filter(Table.id == reservation.table_id).first():
        raise HTTPException(status_code=404, detail="Столик не найден")

    # Вычисляем время окончания новой брони
    end_time = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)

    # Проверка конфликтов
    conflicting = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.reservation_time < end_time,
        func.datetime(
            Reservation.reservation_time,
            f"+{Reservation.duration_minutes} minutes"
        ) > reservation.reservation_time
    ).first()

    if conflicting:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Столик уже забронирован (ID существующей брони: {conflicting.id})"
        )

    # Проверка времени брони

    current_time = datetime.now(reservation.reservation_time.tzinfo)

    if reservation.reservation_time < current_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время бронирования должно быть в будущем"
        )

    # Проверка что бронь не более чем на 1 месяц вперед
    max_reservation_date = current_time + relativedelta(months=1)
    if reservation.reservation_time > max_reservation_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бронирование возможно не более чем на 1 месяц вперед"
        )

        # Создание бронирования
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, description="Успешно удалено")
async def delete_reservation(id: int, db: DbSession):
    """
    Удалить бронирование по ID
    Возвращает 404 если бронирование не найдено
    """
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    db.delete(reservation)
    db.commit()
    return None
