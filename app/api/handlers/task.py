from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies.service import DependentService
from app.api.dependencies.user import get_current_user
from app.models.domain.task import Task
from app.models.domain.user import User
from app.models.schemas.task import TaskIn, TaskOut
from app.repositories.task import TaskRepository
from app.services.task import TaskService

router = APIRouter()


task_service = DependentService(TaskService, TaskRepository, is_security_settings=False)


@router.get('', response_model=list[TaskOut], summary='Показать все задачи')
async def get_tasks(service: TaskService = Depends(task_service), current_user: User = Depends(get_current_user)):
    return await service.get_all_tasks(user_id=current_user.id)


@router.post('', response_model=TaskOut, summary='Создать задачу')
async def create_task(
    task: TaskIn, service: TaskService = Depends(task_service), current_user: User = Depends(get_current_user)
):
    task = Task(title=task.title, content=task.content, user_id=current_user.id)
    return await service.create_task(task)


@router.delete('', summary='Удалить задачу', status_code=204)
async def delete_task(
    task_id: int, service: TaskService = Depends(task_service), current_user: User = Depends(get_current_user)
):
    task_in_database = await service.get_task_by_id(task_id)

    if task_in_database.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you have no access to this task')

    await service.delete_task(task_id)


@router.patch('/{id}', response_model=TaskOut, summary='Обновить задачу')
async def update_task(
    task_id: int,
    task: TaskIn,
    service: TaskService = Depends(task_service),
    current_user: User = Depends(get_current_user),
):
    task_in_database = await service.get_task_by_id(task_id)

    if task_in_database.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you have no access to this task')

    task = Task(id=task_id, title=task.title, content=task.content, user_id=current_user.id)
    return await service.update_task(task)
