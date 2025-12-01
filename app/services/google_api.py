from datetime import datetime
from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT


def get_now_datetime_str() -> str:
    return datetime.now().strftime({FORMAT})


def build_spreadsheet_body() -> dict:
    return {
        'properties': {
            'title': f'Отчёт на {get_now_datetime_str()}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }]
    }


def build_table_values() -> list[list[str]]:
    return [
        ['Отчёт от', get_now_datetime_str()],
        ['Топ проектов по скорости завершения'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]


PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}


async def convert_seconds_to_dhms(seconds: int) -> str:
    """Конвертация секунд в формат дней/часов/минут/секунд."""
    days = seconds // (24 * 60 * 60)
    seconds -= days * (24 * 60 * 60)
    hours = seconds // (60 * 60)
    seconds -= hours * (60 * 60)
    minutes = seconds // 60
    seconds -= minutes * 60

    if days == 1:
        return f'{days} day, {hours}:{minutes}:{seconds}'
    return f'{days} days, {hours}:{minutes}:{seconds}'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> dict:
    """Создание Google-таблицы."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=build_spreadsheet_body())
    )
    return spreadsheet


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Выдача доступа к таблице по email."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    """Запись данных в таблицу отчёта."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *build_table_values(),
        *[list(map(str, project)) for project in projects]
    ]

    for values in table_values[3:]:
        if values[1] and values[1].isdigit():
            values[1] = await convert_seconds_to_dhms(int(values[1]))

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{len(table_values)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
