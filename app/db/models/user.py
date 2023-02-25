import sqlalchemy

from app.db.models.common import BaseModel, IDColumnMixIn


class User(IDColumnMixIn, BaseModel):
    __tablename__ = 'users'

    username = sqlalchemy.Column(sqlalchemy.Text(), nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)
