from pydantic import BaseModel
from utils import to_camel_case

# Валидация задачки
class Task(BaseModel):
    id: int
    title: str
    is_completed: bool


    # конфиг для преобразования полей
    class Config:
        alias_generator = staticmethod(to_camel_case) # заменяет имена полей на результат функции
        validate_by_name = True # разрешает ипользовать оригинальные имена