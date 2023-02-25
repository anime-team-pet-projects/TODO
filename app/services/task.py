from app.db.models import Task as TaskModel
from app.models.domain.task import Task
from app.repositories.task import TaskRepository
from app.services.base import BaseService


class TaskService(BaseService):
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def get_all_tasks(self, user_id: int) -> list[TaskModel]:
        return await self.repository.get_all(user_id)

    async def create_task(self, task: Task) -> Task:
        return await self.repository.create(task)

    async def delete_task(self, task_id: int) -> None:
        await self.repository.delete(task_id)

    async def update_task(self, task: Task) -> Task:
        return await self.repository.update(task)

    async def get_task_by_id(self, task_id: int) -> Task:
        return await self.repository.get_by_id(task_id)
