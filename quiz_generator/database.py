import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Подключение к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Базовый класс для всех моделей
Base = declarative_base()




class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    level = Column(String)
    question = Column(Text)  # Поле для описания задачи
    correct_answer = Column(String)
    wrong_answers = Column(Text)
    explanation = Column(Text)
    resource_link = Column(Text)

    # Добавляем новое поле для кода задачи
    code = Column(Text)  # Поле для кода задачи


# Создание таблиц в базе данных
def init_db():
    Base.metadata.create_all(bind=engine)
