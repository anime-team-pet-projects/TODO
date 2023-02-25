from fastapi import APIRouter

from app.api.handlers import user, task

router = APIRouter()

router.include_router(user.router, tags=['Users'], prefix='/api/users')
router.include_router(task.router, tags=['Tasks'], prefix='/api/tasks')
