from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import Task, CreateTask
from db_models import TaskORM
from database import SessionLocal, engine
from utils import to_camel_case
from database import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()


# доступ для фронтендика
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def get_db():
    db = SessionLocal() # создание сессии
    try:
        yield db # возвращаем объект сессии
    finally:
        db.close() # обязательно закрываем сессию


@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    tasks = [
        Task(id=1, title=to_camel_case('Получить удовольствие от процесса'), is_completed=True),
        Task(id=2, title=to_camel_case('Пофиксить баги'), is_completed=True),
        Task(id=3, title=to_camel_case('Написать фронтенд'), is_completed=False)
    ]
    return tasks


@app.post('/api/tasks', response_model=Task)
def create_task(task: CreateTask, db: Session = Depends(get_db)):
    try:
        db_task = TaskORM(title=task.title, is_completed=task.is_completed) # создаём задачу
        db.add(db_task) # добавляем задачу в базу
        db.commit() # сохраняем задачу в базу
        db.refresh(db_task) # обновляем объект из базы данных

        return Task(id=db_task.id, title=to_camel_case(db_task.title), is_completed=db_task.is_completed)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая задача уже есть")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка базы данных')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка сервера')


