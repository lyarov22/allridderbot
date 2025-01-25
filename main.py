import json
import os
import random
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from dotenv import load_dotenv

from get_members import get_chat_members

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()

# Регистрация бота в диспетчере
dp["bot"] = bot

# Папка с изображениями
IMAGES_FOLDER = "images"
STICKER_PATH = os.path.join(IMAGES_FOLDER, "sticker.webp")
VIDEO_MESSAGES_FOLDER = "video_messages"  # Папка с видеосообщениями
QUOTE_FILE_URL = "https://raw.githubusercontent.com/lyarov22/WebLessons/main/quotes.txt"
JSON_FILE = "channel_messages.json"  # Имя файла с сообщениями

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    # Получаем количество файлов в папке images
    images_folder = "images"
    images_count = len([f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))])
    bsp_count = len(json.load(open(JSON_FILE))) if isinstance(json.load(open(JSON_FILE)), list) else len(json.load(open(JSON_FILE)).keys())

    res = f'''
    Команды чистяка:
        /start - список команд
        /all - упоминуть всех
        /ridder - просмотр чистяка
        /admins - позвать админов
        /quote - цитаты великих

В базе {images_count} чистяков и {bsp_count} больших субатомных пиздаков
    '''
    await message.reply(res)

# Команда бсп
@dp.message(Command("quote"))
async def send_random_quote(message: Message):
    try:
        # Читаем JSON-файл
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)

        if messages:
            # Выбираем случайное сообщение
            random_message = random.choice(messages)
            await message.reply(random_message["text"])
        else:
            await message.reply("Файл с сообщениями пуст.")
    except FileNotFoundError:
        await message.reply("Файл с сообщениями не найден. Спарсите канал сначала.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


# Команда /all — отправка упоминаний всех участников группы
@dp.message(Command("all"))
async def send_usernames(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Эта команда работает только в группах.")
        return

    # Получаем упоминания участников с помощью Telethon
    chat_members = await get_chat_members(message.chat.id)
    
    if chat_members:
        # Отправляем список упоминаний с добавленной фразой в начале
        response = "Ебальники сюда, уважаемые\n" + "\n".join(chat_members)
        await message.answer(response)
    else:
        await message.reply("У участников нет юзернеймов.")

# Команда /admins
@dp.message(Command("admins"))
async def mention_all(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Эта команда работает только в группах.")
        return

    chat_members = [member.user for member in await bot.get_chat_administrators(message.chat.id)]
    mentions = " ".join([f"[{user.first_name}](tg://user?id={user.id})" for user in chat_members])
    await message.answer(f"Призываю админов: {mentions}", parse_mode="Markdown")

# Команда /ridder для отправки случайного изображения или видео
@dp.message(Command("ridder"))
async def send_random_media(message: Message):
    if not os.path.exists(IMAGES_FOLDER) or not os.listdir(IMAGES_FOLDER):
        await message.reply("Папка с изображениями и видео пуста.")
        return

    # Выбор случайного файла
    random_file = random.choice(os.listdir(IMAGES_FOLDER))
    file_path = os.path.join(IMAGES_FOLDER, random_file)

    # Проверка расширения файла и отправка
    if random_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        await message.answer_photo(FSInputFile(file_path))
    elif random_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        await message.answer_video(FSInputFile(file_path))
    elif random_file.lower().endswith(('.webm', '.mp4')) and os.path.exists(VIDEO_MESSAGES_FOLDER):
        # Папка для видеосообщений
        video_messages = [f for f in os.listdir(VIDEO_MESSAGES_FOLDER) if f.lower().endswith('.webm')]
        if video_messages:
            random_video_msg = random.choice(video_messages)
            video_msg_path = os.path.join(VIDEO_MESSAGES_FOLDER, random_video_msg)
            await message.answer_video_note(FSInputFile(video_msg_path))
        else:
            await message.reply("Нет видеосообщений в папке.")
    else:
        await message.reply("Неподдерживаемый формат файла.")

# Обработчик упоминания слов в сообщении
@dp.message(F.text)
async def check_for_keywords(message: Message):
    if "риддер" in message.text.lower():
        if not os.path.exists(STICKER_PATH):
            await message.reply("Файл стикера отсутствует.")
            return
        await message.answer_sticker(FSInputFile(STICKER_PATH))
    if "чзх" in message.text.lower():  # Проверка на наличие слова "ЧЗХ" в сообщении
        video_path = os.path.join("video_messages", "chist.webm")
        
        # Проверка на существование файла
        if os.path.exists(video_path):
            await message.answer_video_note(FSInputFile(video_path))
        else:
            await message.reply("Видео файл не найден.")

    if "бсп" in message.text.lower():  # Проверка на наличие слова "бсп"
        await send_random_quote(message)

    if "илья" in message.text.lower():
        await message.reply("ты хотел сказать богдан.")
    if "кувырок" in message.text.lower():
        await message.reply("@Sergey_Aleksandrovich_pamela")
    if "усть-каменогорск" in message.text.lower():
        await message.reply("ЕБАТЬ ТЫ НАЗВАЛ ЕГО ПОЛНОСТЬЮ")
    if "кто на студии" in message.text.lower():
        await message.reply("я блять тут живу")
    if "сегодня пьем пиво" in message.text.lower():
        await message.reply("сегодня пьем пиво")
    if "уйгур" in message.text.lower():
        await message.reply("готовь лагман @sum1lovu")

    

# Запуск бота
async def main():
    # Пропуск накопившихся апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
