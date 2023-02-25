# TODO Backend

# Установка
- Скопируйте проект
    ```console
    $ git clone https://github.com/anime-team-pet-projects/todo.git -b backend/production
    ```
- Скопируйте `.env`, либо создайте руками
    ```console
    $ cp .env.example .env
    ```
- Установите параметры в файле `.env`
- Запустите контейнер
    ```console
    $ docker-compose up -d --build
    ```

# Миграции
- Создать миграции
    ```console
    $ alembic revision --message="Название" --autogenerate
    ```
- Поднять миграции
    ```console
    $ alembic upgrade head
    ```