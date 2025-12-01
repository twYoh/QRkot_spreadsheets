from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import FinanceBaseModel


class Donation(FinanceBaseModel):
    """Модель пожертвований."""
    __tablename__ = "donation"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f"{super().__repr__()}, "
            f"user_id={self.user_id}, "
            f"comment='{self.comment}')"
        )
