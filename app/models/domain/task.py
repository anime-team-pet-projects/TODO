from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    content: str
    user_id: int
    id: Optional[int] = None
