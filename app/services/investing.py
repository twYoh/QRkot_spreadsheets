from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_project_or_donat(
        obj_db: Union[CharityProject, Donation],
        close_date: datetime
):
    """Меняет статус объекта БД пожертвования или проекта."""
    obj_db.fully_invested = True
    obj_db.close_date = close_date
    obj_db.invested_amount = obj_db.full_amount


async def create_new_investing(
        obj_db_project: Union[CharityProject, Donation],
        obj_db_invest: Union[list[CharityProject], list[Donation]],
        session: AsyncSession
) -> None:
    """
    Функция, выполняющая процесс инвестирования.

    Параметры:
    1) obj_db_project — объект проекта или пожертвования;
    2) obj_db_invest — список проектов или пожертвований;
    3) session — асинхронная сессия БД.

    Если передано пожертвование,
    оно распределяется между незакрытыми проектами.
    Если передан проект, ему добавляются нераспределённые пожертвования.

    В ходе инвестирования объекты, полностью распределившие свои средства,
    помечаются как закрытые, а изменения сохраняются в БД.
    """
    full_amount = obj_db_project.full_amount
    close_date = datetime.now()
    for invest in obj_db_invest:
        free_sum = invest.full_amount - invest.invested_amount
        remains_sum = full_amount - free_sum
        if remains_sum > 0:
            close_project_or_donat(invest, close_date)
            obj_db_project.invested_amount += full_amount - remains_sum
            full_amount = remains_sum
        elif remains_sum < 0:
            close_project_or_donat(obj_db_project, close_date)
            invest.invested_amount += full_amount
        else:
            close_project_or_donat(invest, close_date)
            close_project_or_donat(obj_db_project, close_date)
        session.add(invest)
        if remains_sum <= 0:
            break
    session.add(obj_db_project)
    await session.commit()
    await session.refresh(obj_db_project)
