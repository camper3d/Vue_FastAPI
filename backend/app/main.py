from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import Task, CreateTask
from db_models import TaskORM
from database import SessionLocal, engine, Base
from utils import to_camel_case

Base.metadata.create_all(bind=engine) # создаём таблицы

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
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskORM).all() # возвращаем все задачи
    return tasks


@app.post('/api/tasks', response_model=Task)
def create_task(task: CreateTask, db: Session = Depends(get_db)):
    try:
        camel_title = to_camel_case(task.title)
        db_task = TaskORM(title=camel_title, completed=task.completed) # создаём задачу
        db.add(db_task) # добавляем задачу в базу
        db.commit() # сохраняем задачу в базу
        db.refresh(db_task) # обновляем объект из базы данных

        return Task(id=db_task.id, title=db_task.title, completed=db_task.completed)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такая задача уже есть")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка базы данных')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete('/api/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskORM).filter(TaskORM.id == task_id).first() # поиск нужной задачи
    if not task:
        raise HTTPException(status_code=404, detail='Нет задачи')
    db.delete(task) # удаляем задачу
    db.commit() # комитим изменение
    return {'msg': 'задача удалена'}


