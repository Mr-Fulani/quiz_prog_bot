import logging
from aiogram import Dispatcher, Bot
from config import API_TOKEN
from handlers.start import register_start_handler



async def on_startup(_) -> None:
    print("Бот запущен!")




async def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()

    # Регистрируем обработчики
    register_start_handler(dp)

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
