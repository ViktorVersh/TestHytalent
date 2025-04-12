from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timezone, timedelta

MAX_RESERVATION_ADVANCE_DAYS = 30


class Reserv(BaseModel):
    custom_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class ReservationResponse(Reserv):
    id: int


class ReservationCreate(Reserv):
    pass

    @field_validator('reservation_time')
    def validate_reservation_time(cls, v: datetime):
        current_time = datetime.now(v.tzinfo if v.tzinfo else None)
        max_reservation_date = current_time + timedelta(days=MAX_RESERVATION_ADVANCE_DAYS)

        if v < current_time:
            raise ValueError("Время бронирования должно быть в будущем")

        if v > max_reservation_date:
            raise ValueError("Бронирование возможно не более чем на 1 месяц вперед")

        return v

    @field_validator('reservation_time')
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            # Если время без пояса, считаем что это UTC
            return v.replace(tzinfo=timezone.utc)
        # Конвертируем любой пояс в UTC
        return v.astimezone(timezone.utc)

    model_config = ConfigDict(from_attributes=True)
