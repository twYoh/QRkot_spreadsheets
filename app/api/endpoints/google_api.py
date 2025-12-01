from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value)


router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_project_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
) -> dict[str, str]:
    """
    Создаёт Google-таблицу с отчётом по закрытым благотворительным проектам,
    отсортированным по времени, затраченному на сбор средств.
    Доступно только суперпользователям.
    """
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)

    spreadsheet = await spreadsheets_create(wrapper_services)
    spreadsheet_id = spreadsheet["spreadsheetId"]
    spreadsheet_url = spreadsheet["spreadsheetUrl"]
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            wrapper_services
        )
    except Exception as e:
        return {
            "error": "Не удалось обновить данные таблицы",
            "detail": str(e),
            "url": spreadsheet_url
        }

    return {"Google Sheet URL": spreadsheet_url}
