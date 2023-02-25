import sqlalchemy
from sqlalchemy_utils import ChoiceType

from app.db.models.common import BaseModel, IDColumnMixIn


class Task(IDColumnMixIn, BaseModel):
    __tablename__ = 'tasks'

    STATUSES = [('open', 'open'), ('done', 'done')]

    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    status = sqlalchemy.Column(ChoiceType(STATUSES), nullable=False, default='open')
