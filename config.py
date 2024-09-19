import os
from dotenv import load_dotenv
from typing import List

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота
API_TOKEN: str = os.getenv('API_TOKEN')

# Преобразуем строку каналов в список строк (каналы должны быть разделены запятыми)
CHANNELS: List[str] = os.getenv('CHANNELS', '').split(',')
