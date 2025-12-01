from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.services.investing import create_new_investing
from app.models import User
from app.schemas.donation import DonationCreate, DonationtDB, AllDonationDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[AllDonationDB],
    dependencies=[Depends(current_superuser)])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает полный список пожертвований.
    Доступ разрешён только суперпользователям.

    Параметры:
        1) session (AsyncSession): Асинхронная сессия работы с базой данных.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get('/my', response_model=list[DonationtDB])
async def get_all_current_users_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Возвращает список пожертвований, сделанных текущим пользователем.
    Доступно только авторизованным пользователям.

    Параметры:
        1) session (AsyncSession): Асинхронная сессия работы с базой данных;
        2) user (User): Текущий авторизованный пользователь.
    """
    all_user_donations = await donation_crud.get_all_user_donations(
        session, user
    )
    return all_user_donations


@router.post('/', response_model=DonationtDB)
async def make_a_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)

):
    """
    Создаёт новое пожертвование. Доступно только авторизованным пользователям.
    После создания пожертвование может быть автоматически распределено
    между открытыми проектами.

    Параметры:
        1) donation (DonationCreate): Данные для создания пожертвования;
        2) session (AsyncSession): Асинхронная сессия работы с базой данных;
        3) user (User): Текущий авторизованный пользователь.
    """
    new_donation = await donation_crud.create(donation, session, user)
    projects = await (
        charity_project_crud.get_open(session)
    )
    if projects is not None:
        await create_new_investing(new_donation, projects, session)
    return new_donation
