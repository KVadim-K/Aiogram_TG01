import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
import requests
import random
from gtts import gTTS
import os

from config import TOKEN, API_KEY


bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения погоды
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return f"Температура в {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    else:
        return "Не удалось получить данные о погоде."

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('videos/Astronomy.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("voice/sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('sounds/sound2.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("doc/Портфолио.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   await bot.send_chat_action(message.chat.id, 'upload_voice')
   audio = FSInputFile('training.ogg')
   await bot.send_voice(message.chat.id, voice=audio)
   os.remove("training.ogg")

# Прописываем хендлер и варианты ответов:

@dp.message(Command('photo'))  # Можно изменить префикс (Command('photo', prefix='&'))
async def photo(message: Message):
    list = ['https://s1.1zoom.ru/big3/813/421743-svetik.jpg',
            'https://www.rabstol.net/uploads/gallery/main/410/rabstol_net_river_10.jpg',
            'https://balthazar.club/o/uploads/posts/2024-01/1704994092_balthazar-club-p-gori-letom-oboi-49.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

# Убедитесь, что папка 'img' существует
if not os.path.exists('img'):
    os.makedirs('img')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    # Сохранение фотографии в папке 'img' или 'tmp'
    # await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    # await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')
    # Получаем информацию о файле
    file_info = await bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path

    # Определяем имя и расширение файла
    file_name = os.path.basename(file_path)

    # Скачиваем файл с сохранением оригинального расширения
    await bot.download_file(file_path, destination=f'img/{file_name}')
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять '
                         'творческие функции, которые традиционно считаются прерогативой человека; наука и технология '
                         'создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('weather'))
async def weather(message: Message):
    city = "Ростов-на-Дону"  # Укажите город для прогноза погоды
    weather_info = get_weather(city)
    await message.answer(weather_info)
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start \n/help \n/photo \n/weather \n/voice \n/video \n/doc \n/training")
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')

translator = Translator()  # Создаем экземпляр Translator

@dp.message(F.text)
async def translate(message: Message):
    text = message.text
    translation = translator.translate(text, dest='en')
    await message.answer(translation.text)

# @dp.message()
# async def start(message: Message):
#     if message.text.lower() == 'test':
#         await message.answer('Тестируем')
#     await message.send_copy(chat_id=message.chat.id)  # Эхо-бот

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
