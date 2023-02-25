from pydantic import BaseModel


class TaskOut(BaseModel):
    id: int
    title: str
    content: str
    status: str


class TaskIn(BaseModel):
    title: str
    content: str
    status: str
