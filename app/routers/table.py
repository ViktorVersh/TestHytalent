from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.table import TableCreate, TableResponse
from app.backend.db_depends import get_db

router = APIRouter(prefix='/table', tags=['table'])
DbSession = Annotated[Session, Depends(get_db)]


@router.get('/all', response_model=list[TableResponse])  # Список всех столиков
async def get_all_tables(db: DbSession):
    """
    Получить список всех столиков
    """

    tables = db.query(Table).all()
    return tables


@router.post('/create', response_model=TableResponse)  # Создание нового столика
async def create_table(table: TableCreate, db: DbSession):
    """
    Создать новый столик
    """

    db_table = Table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)  # Удаление столика
async def delete_table(id: int, db: DbSession):
    """
    Удалить столик по ID
    """
    db_table = db.query(Table).filter(Table.id == id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Проверка активных бронирований
    active_reservations = db.query(Reservation).filter(
        Reservation.table_id == id,
        Reservation.reservation_time >= datetime.now()
    ).count()

    if active_reservations > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete table with active reservations"
        )

    db.delete(db_table)
    db.commit()
    return None