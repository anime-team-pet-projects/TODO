from pydantic import BaseModel


class TaskOut(BaseModel):
    id: int
    title: str
    content: str


class TaskIn(BaseModel):
    title: str
    content: str


class UpdateTask(BaseModel):
    ...
