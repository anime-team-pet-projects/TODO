from fastapi import FastAPI

from databases import Database
from loguru import logger

from app.core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    db = Database(settings.database_url)
    await db.connect()

    app.state.pool = db

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.disconnect()

    logger.info("Connection closed")
