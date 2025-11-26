from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        """Получить проект по имени."""
        project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[tuple[str]]:
        """
        Метод, возвращающий список закрытых проектов
        с вычислением времени, затраченного на сбор пожертвований.
        Разница во времени указывается в секундах.
        """
        second = (extract('second', self.model.close_date) -
                  extract('second', self.model.create_date))
        minute = (extract('minute', self.model.close_date) -
                  extract('minute', self.model.create_date)) * 60
        hour = (extract('hour', self.model.close_date) -
                extract('hour', self.model.create_date)) * 60 * 60
        day = (extract('day', self.model.close_date) -
               extract('day', self.model.create_date)) * 24 * 60 * 60
        total_second = second + minute + hour + day
        stmt = select([
            self.model.name,
            total_second.label('time'),
            self.model.description
        ]).where(self.model.fully_invested.is_(True)).order_by('time')
        projects = await session.execute(stmt)
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
