from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT, TABLE_ROW_COUNT, TABLE_COLUMN_COUNT


now_date_time = datetime.now().strftime(FORMAT)


TABLE_HEADER = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости завершения'],
    ['Название проекта', 'Время сбора', 'Описание']
]


SPREADSHEET_BODY_TEMPLATE = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Лист1',
                gridProperties=dict(
                    rowCount=TABLE_ROW_COUNT,
                    columnCount=TABLE_COLUMN_COUNT,
                )
            )
        )
    ]
)


PERMISSIONS_BODY = dict(
    type='user',
    role='writer',
    emailAddress=settings.email
)


def build_spreadsheet_body() -> dict:
    spreadsheet_body = deepcopy(SPREADSHEET_BODY_TEMPLATE)
    spreadsheet_body['properties']['title'] = (
        f"Отчёт на {datetime.now().strftime(FORMAT)}"
    )
    return spreadsheet_body


def build_table_values() -> list[list[str]]:
    table = deepcopy(TABLE_HEADER)
    table[0][1] = now_date_time
    return table


async def convert_seconds_to_dhms(seconds: int) -> str:
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
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=build_spreadsheet_body())
    )
    return spreadsheet['spreadsheetId'], spreadsheet['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
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
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *build_table_values(),
        *[list(map(str, project)) for project in projects]
    ]

    if len(table_values) > TABLE_ROW_COUNT:
        raise ValueError(
            'Слишком много строк для таблицы: '
            f'{len(table_values)} из {TABLE_ROW_COUNT}'
        )

    for row in table_values:
        if len(row) > TABLE_COLUMN_COUNT:
            raise ValueError(
                'Слишком много столбцов в строке: '
                f'{len(row)} из {TABLE_COLUMN_COUNT}'
            )

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=(
                f'R1C1:R{len(table_values)}C'
                f'{max(len(row) for row in table_values)}'
            ),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
