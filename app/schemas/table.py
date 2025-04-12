from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TableBase(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(TableBase):
    pass


class TableResponse(TableBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
