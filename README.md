# Приложение QRkot_spreadseets

Учебный проект Яндекс Практикума.
QRKot - сервис благотворительного фонда помощи котикам, созданный на базе FastAPI.

## Цель проекта

Закрепить навыки разработки с использованием FastAPI, SQLAlchemy,
pydantic и Google API.

## Используемые технологии

-   Python 3.10.3
-   FastAPI 0.78.0
-   Uvicorn 0.17.6
-   SQLAlchemy 1.4.36
-   Alembic 1.7.7
-   FastAPI Users 10.0.4
-   Aiogoogle 4.2.0
-   Google Drive API v3
-   Google Sheets API v4

## Описание

Фонд собирает средства для различных целевых проектов: медицинская
помощь котикам, обустройство мест для уличных кошек, обеспечение кормом
и другие инициативы по поддержке кошачьей популяции.

### Основной функционал

-   создание благотворительных проектов;
-   приём пожертвований и автоматическое распределение средств между
    проектами;
-   управление пользователями.

## Документация

Документация доступна после запуска приложения по адресам: - `/docs` -
`/redoc`

## База данных

Используется асинхронное подключение к базе данных через SQLAlchemy ORM.
Миграции выполняются с помощью Alembic.

## Как развернуть проект локально

1.  Клонировать репозиторий и перейти в директорию проекта:
    `bash     git clone https://github.com/twYoh/QRkot_spreadsheets.git`

2.  Создать и активировать виртуальное окружение:
    `bash     python -m venv venv` 
    Для Linux/macOS:
    `source venv/bin/activate` 
    Для Windows:
    `source venv/Scripts/activate`

3.  Установить зависимости:
    `bash     python -m pip install --upgrade pip     pip install -r requirements.txt`

4.  Создать файл `.env` с параметрами окружения, например:
    `DATABASE_URL=sqlite+aiosqlite:///./fastapi.db     SECRET=secretpassword`

5.  Выполнить миграции базы данных: 
    `bash     alembic upgrade head` 
    или:
    `bash     alembic upgrade ID` где `ID` - идентификатор
    миграции.

6.  Запустить приложение: `bash     uvicorn app.main:app`

## Формирование отчёта в Google Sheets

### Подключение Google API

Для работы с Google API необходимо создать проект в Google Cloud
Platform, добавить сервисный аккаунт и подключить API: Google Drive и
Google Sheets.\
JSON-файл с ключами сервисного аккаунта нужно перенести в переменные
окружения `.env`.

Также в `.env` требуется указать адрес Gmail-аккаунта, которому будет
предоставлен доступ к отчёту.

Пример `.env`:

    TYPE=...
    PROJECT_ID=...
    PRIVATE_KEY_ID=...
    PRIVATE_KEY=...
    CLIENT_EMAIL=...
    CLIENT_ID=...

    AUTH_URI=...
    TOKEN_URI=...
    AUTH_PROVIDER_X509_CERT_URL=...
    CLIENT_X509_CERT_URL=...

    EMAIL=...

    DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
    SECRET=secretpassword
