from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import MAX_LENGTH


class CharityProjectBase(BaseModel):
    """Базовая схема данных благотворительного проекта."""
    name: str = Field(None, max_length=MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """Схема для частичного обновления данных благотворительного проекта."""


class CharityProjectCreate(CharityProjectUpdate):
    """Схема данных для создания нового благотворительного проекта."""
    name: str = Field(..., max_length=MAX_LENGTH)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    """Схема для представления информации о проекте."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
