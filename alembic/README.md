## Перечень команд Alembic:

-   Инициализация Alembic:

``` bash
alembic init --template async alembic
```

Параметр --template async требуется при использовании асинхронного
подключения к базе данных.

-   Создание миграции:

``` bash
alembic revision --autogenerate -m "комментарий к миграции"
```

-   Применение всех неприменённых миграций:

``` bash
alembic upgrade head
```

-   Откат всех миграций до исходного состояния:

``` bash
alembic downgrade base
```

-   Применение миграций вплоть до указанного идентификатора (ID
    миграции):

``` bash
alembic upgrade ID
```

-   Откат миграций до выбранного ID:

``` bash
alembic downgrade ID
```

Можно указывать сокращённые идентификаторы миграций.

-   Просмотр истории миграций:

``` bash
alembic history
```

-   Проверка последней применённой миграции:

``` bash
alembic current
```
