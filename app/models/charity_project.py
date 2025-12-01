from sqlalchemy import Column, String, Text

from app.models.base import FinanceBaseModel
from app.core.constants import MAX_LENGTH


class CharityProject(FinanceBaseModel):
    __tablename__ = "charityproject"
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f"{super().__repr__()}, "
            f"name={self.name}, "
            f"description={self.description})"
        )
