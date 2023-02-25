import sqlalchemy

from app.db.models.common import BaseModel, IDColumnMixIn


class Task(IDColumnMixIn, BaseModel):
    __tablename__ = 'tasks'

    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
