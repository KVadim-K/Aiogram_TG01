import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_yes_no(force_choice=None):
    url = 'https://yesno.wtf/api'
    if force_choice in ["yes", "no", "maybe"]:
        url += f'?force={force_choice}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    user_first_name = message.from_user.first_name
    welcome_text = (
        f"Привет, {user_first_name}!\n"
        "Отправь мне любое сообщение, и я отвечу 'да', 'нет' или 'может быть'.\n"
        "Выберите один из вариантов:"
    )

    # Создаем инлайн-клавиатуру с тремя кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes"),InlineKeyboardButton(text="Нет", callback_data="no")],
        [InlineKeyboardButton(text="Может быть", callback_data="maybe")]
    ])

    await message.answer(welcome_text, reply_markup=keyboard)


@dp.callback_query()
async def handle_callback(query: CallbackQuery):
    # Ответ на нажатие кнопки
    choice = query.data
    if choice in ["yes", "no", "maybe"]:
        # Получаем ответ с сайта yesno.wtf с указанием force
        response_data = await get_yes_no(force_choice=choice)
        if response_data:
            answer_text = response_data.get("answer", "Нет ответа")
            gif_url = response_data.get("image", "")

            # Отправляем пользователю текст и анимацию
            await query.message.answer(f"Вы выбрали: {choice.capitalize()}\nОтвет: {answer_text}")
            if gif_url:
                await query.message.answer_animation(gif_url)
        else:
            await query.message.answer("Не удалось получить ответ с сервера.")

    await query.answer()  # Закрываем уведомление о нажатии кнопки


async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())