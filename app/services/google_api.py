from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import NOW_DATE_TIME


SPREADSHEET_BODY = {
    'properties': {'title': f'Отчёт на {NOW_DATE_TIME}',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}

TABLE_VALUES = [
    ['Отчёт от', NOW_DATE_TIME],
    ['Топ проектов по скорости завершения'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def convert_seconds_to_dhms(seconds: int) -> str:
    """Функция для конвертации секунд в дни, часы, минуты, секунды."""
    days = seconds // (24 * 60 * 60)
    seconds -= days * (24 * 60 * 60)
    hours = seconds // (60 * 60)
    seconds -= hours * (60 * 60)
    minutes = seconds // 60
    seconds -= minutes * 60
    if days == 1:
        return f'{days} day, {hours}:{minutes}:{seconds}'
    return f'{days} days, {hours}:{minutes}:{seconds}'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Заглушка для создания гугл-таблицы."""
    return 'fake_spreadsheet_id'


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Заглушка для выдачи прав доступа."""


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Заглушка для обновления таблицы с данными."""
