from fastapi import APIRouter, Depends

from app.api.dependencies.service import DependentService
from app.models.domain.task import Task
from app.models.schemas.task import TaskIn, TaskOut
from app.repositories.task import TaskRepository
from app.services.task import TaskService

router = APIRouter()


task_service = DependentService(TaskService, TaskRepository)


@router.get('', response_model=list[TaskOut], summary='Показать все задачи')
async def get_tasks(service: TaskService = Depends(task_service)):
    return await service.get_all_tasks()


@router.post('', response_model=TaskOut, summary='Создать задачу')
async def create_task(task: TaskIn, service: TaskService = Depends(task_service)):
    task = Task(title=task.title, content=task.content)
    return await service.create_task(task)


@router.delete('', summary='Удалить задачу', status_code=204)
async def delete_task(task_id: int, service: TaskService = Depends(task_service)):
    await service.delete_task(task_id)


@router.patch('/{id}', response_model=TaskOut, summary='Обновить задачу')
async def update_task(task_id: int, task: TaskIn, service: TaskService = Depends(task_service)):
    task = Task(id=task_id, title=task.title, content=task.content)
    return await service.update_task(task)
