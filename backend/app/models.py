from pydantic import BaseModel
from utils import to_camel_case

# Валидация задачки
class Task(BaseModel):
    id: int
    title: str
    completed: bool

    # конфиг для преобразования полей
    class Config:
        alias_generator = staticmethod(to_camel_case)
        populate_by_name = True
        from_attributes = True

# Валидация данных для созданной задачи(путём наследования от Task)
class CreateTask(BaseModel):
    title: str
    completed: bool

    class Config:
        alias_generator = staticmethod(to_camel_case)
        populate_by_name = True

