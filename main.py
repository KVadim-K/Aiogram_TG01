import asyncio
import os
import random

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from googletrans import Translator
from gtts import gTTS

import keyboard as kb
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

# @dp.message(CommandStart())
# async def start(message: Message):
#     await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_test)  # Клавиатура kb.main для reply кнопки/ kb.inline_keyboard_test для inline кнопки/ await kb.test_keyboard() для Builder кнопок

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Здравствуй, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_start)

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_links)

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_dynamic)

@dp.callback_query(F.data == 'hello')  # обработка нажатия на кнопку
async def hello(callback: CallbackQuery):
    await callback.answer("Готовлю ответ")
    await callback.message.answer(f'Здравствуйте!!!, {callback.from_user.full_name}')

@dp.callback_query(F.data == 'bay')  # обработка нажатия на кнопку
async def hello(callback: CallbackQuery):
    await callback.answer("Готовлю ответ")
    await callback.message.answer(f'До свидания!!!, {callback.from_user.full_name}')

@dp.callback_query(F.data == 'option_1')  # обработка нажатия на кнопку
async def option_1(callback: CallbackQuery):
    await callback.answer("Готовлю ответ")
    await callback.message.edit_text(f'До свидания!!!, {callback.from_user.full_name}')

@dp.message(F.text == 'Опция 1')  # обработка нажатия на кнопку
async def option_1(message: Message):
    await message.answer("Готовлю ответ")
@dp.message(F.text == 'Опция 2')  # обработка нажатия на кнопку
async def option_2(message: Message):
    await message.answer("Готовлю ответ")

@dp.callback_query(F.data == 'video')  # обработка нажатия на кнопку
async def video(callback: CallbackQuery):
    await callback.answer("Видео подгружаются")  # всплывающий ответ бота. show_alert=True - всплывающее окно
    await callback.message.answer("Новое видео")
    # await callback.message.answer("https://yandex.ru/news/")

@dp.callback_query(F.data == 'music')  # обработка нажатия на кнопку
async def music(callback: CallbackQuery):
    await callback.answer("Музыка подгружаются")  # всплывающий ответ бота. show_alert=True - всплывающее окно
    await callback.message.answer("Хорошая музыка")
    # await callback.message.answer("https://yandex.ru/news/")

@dp.callback_query(F.data == 'news')  # обработка нажатия на кнопку
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются")  # всплывающий ответ бота. show_alert=True - всплывающее окно
    await callback.message.edit_text("Свежая новость", reply_markup=await kb.test_keyboard())  # обновление сообщения: меняем answer на edit_text и добавляем: reply_markup=await kb.test_keyboard() и убираем старую ссылку ниже.
    # await callback.message.answer("https://yandex.ru/news/")

@dp.callback_query(F.data == 'show_more')  # обработка нажатия на кнопку
async def show_more(callback: CallbackQuery):
    await callback.answer("Сейчас подгрузится")  # всплывающий ответ бота. show_alert=True - всплывающее окно
    await callback.message.edit_text("Подгружаю еще", reply_markup=await kb.dynamic_keyboard())  # обновление сообщения: меняем answer на edit_text и добавляем: reply_markup=await kb.test_keyboard() и убираем старую ссылку ниже.
    # await callback.message.answer("https://yandex.ru/weather/")

@dp.callback_query(F.data == 'option')  # обработка нажатия на кнопку
async def option(callback: CallbackQuery):
    await callback.answer("Почти подгрузилось")  # всплывающий ответ бота. show_alert=True - всплывающее окно
    await callback.message.edit_text("Подгружаю Опция 1", reply_markup=await kb.options_keyboard())  # обновление сообщения: меняем answer на edit_text и добавляем: reply_markup=await kb.test_keyboard() и убираем старую ссылку ниже.
    # await callback.message.answer("https://yandex.ru/weather/")


@dp.message(F.text == "Привет")
async def test_button(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')

@dp.message(F.text == "Пока")
async def test_button(message: Message):
    await message.answer(f'До свидания, {message.from_user.full_name}')


translator = Translator()  # Создаем экземпляр Translator

@dp.message(F.text)
async def translate(message: Message):
    text = message.text
    detected_lang = translator.detect(text).lang # Определяем язык текста
    if detected_lang == 'ru':
        dest_lang = 'en'
    else:
        dest_lang = 'ru'
    translation = translator.translate(text, dest=dest_lang)
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
