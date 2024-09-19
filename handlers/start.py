from aiogram import Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
from quiz_generator.question_generator import get_random_task
from quiz_generator.image_generator import create_console_image_with_code
from services.telegram_service import send_quiz
import logging
import random
import json




def format_task_with_code(description: str, code: str) -> str:
    """
    Форматирует текст задачи с описанием и кодом.
    Добавляет пустую строку между описанием и кодом, а также знак '#' для каждой строки описания.
    """
    # Обрабатываем описание задачи, добавляя '#' перед каждой строкой описания
    processed_description_lines = []
    for line in description.splitlines():
        if line.strip():  # Добавляем '#' только к непустым строкам
            processed_description_lines.append(f"# {line.strip()}")
        else:
            processed_description_lines.append(line)  # Пустые строки оставляем без изменений

    # Соединяем описание
    formatted_description = "\n".join(processed_description_lines)

    # Проверяем код и добавляем пустую строку между описанием и кодом
    if code is None:
        code = ""  # Если код пустой, используем пустую строку

    formatted_task = f"{formatted_description}\n\n{code.strip()}"
    return formatted_task





def register_start_handler(dp: Dispatcher) -> None:
    @dp.message(Command("start"))
    async def send_welcome(message: types.Message) -> None:
        topic = "list_comprehensions"
        level = "easy"
        task = get_random_task(topic, level)

        if task:
            try:
                # Преобразуем неправильные ответы из строки в список
                wrong_answers = json.loads(task.wrong_answers)
            except (json.JSONDecodeError, TypeError):
                # Если ошибка декодирования JSON
                wrong_answers = []
                logging.error(f"Ошибка декодирования wrong_answers: {task.wrong_answers}")

            # Проверка на наличие хотя бы одного неправильного ответа
            if len(wrong_answers) < 1:
                await message.reply("Не удалось найти достаточно вариантов ответов для викторины.")
                return

            # Получаем правильный ответ
            correct_answer = task.correct_answer

            # Формируем список ответов
            answers = wrong_answers + [correct_answer]
            random.shuffle(answers)

            # Преобразуем все ответы в строки
            answers = [str(answer) for answer in answers]
            correct_index = answers.index(str(correct_answer))

            # Отладка
            logging.info(f"Вопрос: {task.question}")
            logging.info(f"Ответы: {answers}")
            logging.info(f"Правильный ответ: {correct_answer}")

            # Путь для сохранения изображения
            image_path = "question_image.png"

            # Путь к файлу логотипа
            logo_path = "media/administration/logo_no_back.png"

            # Форматируем текст задачи и код
            question_with_code = format_task_with_code(task.question, task.code)

            # Генерируем изображение с кодом и логотипом
            create_console_image_with_code(question_with_code, image_path, logo_path)

            # Отправляем изображение
            image_file = FSInputFile(image_path)
            await message.answer_photo(photo=image_file)

            # Отправляем викторину
            await send_quiz(message.chat.id, task.question, answers, correct_index)
        else:
            await message.reply("Не удалось найти задачу для данной темы и уровня сложности.")
