from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL) # создание движка SQLalchemy
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # общение с базой данных через сессии
Base = declarative_base() # базовый класс для моделей SQLalchemy


