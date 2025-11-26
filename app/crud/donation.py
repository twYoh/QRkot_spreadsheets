from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_all_user_donations(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        """Получить перечень всех пожертвований пользователя."""
        user_donation = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return user_donation.scalars().all()


donation_crud = CRUDDonation(Donation)
