from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
metadata = BaseModel.metadata


class IDColumnMixIn:
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
