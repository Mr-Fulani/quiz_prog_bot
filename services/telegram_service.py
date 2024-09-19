from aiogram import Bot
from config import API_TOKEN

bot: Bot = Bot(token=API_TOKEN)

async def send_quiz(chat_id: int, question: str, answers: list[str], correct_option_id: int) -> None:
    """
    Отправляет викторину с вариантами ответов.

    :param chat_id: ID чата, в который будет отправлена викторина
    :param question: Текст вопроса
    :param answers: Список вариантов ответов
    :param correct_option_id: Индекс правильного ответа
    """
    await bot.send_poll(
        chat_id=chat_id,
        question=question,
        options=answers,
        type="quiz",
        correct_option_id=correct_option_id,
        is_anonymous=False
    )
