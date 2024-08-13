import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
import random

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

# Прописываем хендлер и варианты ответов:

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://s1.1zoom.ru/big3/813/421743-svetik.jpg',
            'https://www.rabstol.net/uploads/gallery/main/410/rabstol_net_river_10.jpg', 'https://balthazar.club/o/uploads/posts/2024-01/1704994092_balthazar-club-p-gori-letom-oboi-49.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


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
    await message.answer('Этот бот умеет выполнять команды:\n/start \n/help \n/photo \n/weather')
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет я бот!')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
