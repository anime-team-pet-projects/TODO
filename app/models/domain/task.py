from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    content: str
    id: Optional[int] = None
