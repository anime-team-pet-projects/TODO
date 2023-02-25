from typing import Any, Callable, Type

from databases import Database
from fastapi import Depends
from starlette.requests import Request

from app.repositories.base import BaseRepository


def _get_db_pool(request: Request) -> Database:
    return request.app.state.pool


def get_repository(repo_type: Type[BaseRepository]) -> Callable[[Any], BaseRepository]:
    def _get_repo(database: Database = Depends(_get_db_pool)) -> BaseRepository:
        return repo_type(database)

    return _get_repo
