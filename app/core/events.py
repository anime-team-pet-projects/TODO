from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.config import get_security_settings
from app.core.settings.app import AppSettings
from app.db.events import close_db_connection, connect_to_db


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app, settings)
        security_settings = get_security_settings(
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            access_token_expire_minutes=settings.access_token_expire_minutes,
        )
        app.state.security_settings = security_settings

    return start_app


def create_stop_app_handler(app: FastAPI):
    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app)
