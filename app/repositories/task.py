from sqlalchemy import delete, insert, select, update

from app.db.models import Task as TaskModel
from app.models.domain.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def get_all(self, user_id: int, limit: int = 100, skip: int = 0) -> list[TaskModel]:
        query = select(TaskModel).filter(TaskModel.user_id == user_id).limit(limit).offset(skip)

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

    async def get_by_id(self, task_id: int) -> Task:
        query = select(TaskModel).where(TaskModel.id == task_id)

        return self.model_to_domain(await self.database.fetch_one(query))

    @classmethod
    def model_to_domain(cls, model: TaskModel) -> Task:
        return Task(
            id=model.id,
            user_id=model.user_id,
            status=model.status,
            title=model.title,
            content=model.content,
        )
