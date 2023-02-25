from sqlalchemy import delete, insert, select, update

from app.db.models import Task as TaskModel
from app.models.domain.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def get_all(self, limit: int = 100, skip: int = 0) -> list[TaskModel]:
        query = select(TaskModel).limit(limit).offset(skip)

        return await self.database.fetch_all(query)

    async def create(self, task: Task) -> Task:
        query = insert(TaskModel).values(**task.dict(exclude={'id'}))

        task.id = await self.database.execute(query)
        return task

    async def delete(self, task_id: int) -> None:
        query = delete(TaskModel).where(TaskModel.id == task_id)

        await self.database.execute(query)

    async def update(self, task: Task) -> Task:
        query = update(TaskModel).where(TaskModel.id == task.id).values(**task.dict(exclude={'id'}))

        await self.database.execute(query)

        return task
