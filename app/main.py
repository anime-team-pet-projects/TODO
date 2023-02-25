from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.handlers.api import router as api_router
from app.core.config import get_app_settings
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    # Загружаем настройки
    settings = get_app_settings()

    # Настраиваем логгирование
    settings.configure_logging()

    # Создаём приложение FastAPI
    application = FastAPI()

    # Настройка CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Добавляем обработчики на запуск и стоп приложения
    application.add_event_handler(
        'startup',
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        'shutdown',
        create_stop_app_handler(application),
    )

    application.include_router(api_router)

    return application


app = get_application()
