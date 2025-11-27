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
    """Функция отвечающая за создание гугл-таблицы."""
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция для выдачи прав доступа к таблице
    личному гугл-аккаунту.
    """
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция отвечающая за формирование отчета в гугл-таблице
    на основе переданных данных. В гугл-таблицах значения по
    умолчанию в ячейках None, поэтому нужно использовать метод update.
    """
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *TABLE_VALUES,
        *[
            list(map(str, project)) for project in projects
        ]
    ]
    for values in table_values[len(TABLE_VALUES):]:
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
