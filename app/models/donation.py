from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import FinanceBaseModel


class Donation(FinanceBaseModel):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
