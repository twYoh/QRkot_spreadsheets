from sqlalchemy import Column, String, Text

from app.models.base import FinanceBaseModel
from app.core.constants import MAX_LENGTH


class CharityProject(FinanceBaseModel):
    """Модель проектов."""
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text())
