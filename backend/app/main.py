from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Task
from utils import to_camel_case


app = FastAPI()


# доступ для фронтендика
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    tasks = [
        Task(id=1, title=to_camel_case('Получить удовольствие от процесса'), is_completed=True),
        Task(id=2, title=to_camel_case('Пофиксить баги'), is_completed=True),
        Task(id=3, title=to_camel_case('Написать фронтенд'), is_completed=False)
    ]
    return tasks