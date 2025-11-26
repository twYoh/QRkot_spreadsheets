from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """
    Проверяет, существует ли проект с указанным названием.
    Если в базе уже есть проект с таким именем,
    генерируется исключение HTTP 400.

    Параметры:
        1) project_name (str): Название проекта для проверки;
        2) session (AsyncSession): Асинхронная сессия взаимодействия с БД.
    """
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Определяет, присутствует ли в базе проект с указанным ID.

    Параметры:
        1) project_id (int): Идентификатор проверяемого проекта;
        2) session (AsyncSession): Асинхронная сессия работы с базой данных.
    """
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_before_edit(
        charity_project: CharityProject,
        update_data: CharityProjectUpdate
) -> None:
    """
    Проверяет, допускается ли обновление данных проекта.
    Редактирование запрещается, если проект уже закрыт
    или если указанная новая сумма меньше той, что уже была вложена.

    Параметры:
        1) charity_project (CharityProject): Проект, который требуется изменить;
        2) update_data (CharityProjectUpdate): Новые данные для обновления проекта.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Редактирование закрытого проекта недоступно!'
        )
    if (update_data.full_amount and
       update_data.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=422,
            detail='Запрошенная сумма не должна быть меньше внесённых средств!'
        )


async def check_charity_project_is_not_invested_or_closed(
        charity_project: CharityProject
) -> None:
    """
    Определяет, допустимо ли удаление проекта.
    Удаление запрещено, если проект является закрытым
    или если в него уже внесены какие-либо средства.

    Параметры:
        1) charity_project (CharityProject): Проект, который планируется удалить.
    """
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Проект нельзя удалить,'
                    'так как в него были сделаны взносы!'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Удаление закрытых проектов запрещено!'
        )