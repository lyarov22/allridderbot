import os
from telethon import TelegramClient
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Инициализация клиента Telethon
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_chat_members(chat_id):
    """
    Получает список упоминаний всех участников чата с помощью Telethon.
    :param chat_id: ID чата
    :return: Список упоминаний пользователей
    """
    await client.start(bot_token=BOT_TOKEN)
    chat_members = []
    
    # Получаем участников чата
    async for member in client.iter_participants(chat_id):
        if member.username:  # Если у участника есть юзернейм
            # Формируем упоминание в формате tg://user?id=<user_id>
            # mention = f"[{member.username}](tg://user?id={member.id})"
            mention = f'@{member.username}'
            chat_members.append(mention)
    
    await client.disconnect()
    return chat_members
