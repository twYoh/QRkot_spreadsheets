from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base
from app.core.constants import DEFAULT_VALUE


class FinanceBaseModel(Base):
    """Абстрактная базовая модель для пожертвований и проектов."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_VALUE)
    fully_invested = Column(Boolean(), default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_valid_range'
        ),
    )

    def __str__(self):
        return (
            f"{type(self).__name__}("
            f"{self.full_amount=}, "
            f"{self.invested_amount=}, "
            f"{self.fully_invested=}, "
            f"{self.create_date=}, "
            f"{self.close_date=}"
            ")"
        )
