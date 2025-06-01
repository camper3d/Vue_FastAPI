from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Валидация данных в базу Postgresql
class TaskORM(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)