import random
from typing import Tuple, List
from sqlalchemy.orm import Session
from quiz_generator.database import Task, SessionLocal
import random
import textwrap
from typing import Tuple, List
import json





def format_task_with_code(code: str) -> str:
    """
    Форматирует текст кода. Убирает лишние пробелы, если есть.

    :param code: Текст кода
    :return: Форматированный код
    """
    return code.strip()  # Убираем лишние пробелы и возвращаем код





def generate_square_question() -> Tuple[str, int, List[int]]:
    """
    Генерирует задачу на нахождение квадрата числа и варианты ответов.

    :return: Кортеж, содержащий вопрос, правильный ответ и список вариантов ответов.
    """
    x: int = random.randint(2, 10)

    # Описание задачи
    description: str = """
    Напишите функцию, которая возвращает квадрат числа
    """

    # Код задачи
    code: str = f"""
    def square(x):
        return x ** 2

    print(square({x}))
    """

    # Форматируем описание и код
    question: str = format_task_with_code(description, code)

    correct_answer: int = x ** 2

    # Генерируем несколько неправильных вариантов ответа
    incorrect_answers: List[int] = [random.randint(correct_answer - 10, correct_answer + 10) for _ in range(3)]

    # Добавляем правильный ответ и перемешиваем варианты
    answers: List[int] = incorrect_answers + [correct_answer]
    random.shuffle(answers)

    return question, correct_answer, answers









def add_task(
    topic: str,
    level: str,
    question: str,
    code: str,
    correct_answer: str,
    wrong_answers: list,
    explanation: str,
    resource_link: str
) -> None:
    db = SessionLocal()

    new_task = Task(
        topic=topic,
        level=level,
        question=question,
        code=code.strip(),
        correct_answer=correct_answer,
        wrong_answers=json.dumps(wrong_answers),
        explanation=explanation,
        resource_link=resource_link
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()








# Функция для получения случайной задачи
def get_random_task(topic: str, level: str = None):
    db: Session = SessionLocal()
    query = db.query(Task).filter(Task.topic == topic)

    if level:
        query = query.filter(Task.level == level)

    tasks = query.all()
    db.close()

    if tasks:
        return random.choice(tasks)
    return None

