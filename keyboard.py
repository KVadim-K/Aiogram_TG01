from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")],
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", callback_data="video")],
    [InlineKeyboardButton(text="Музыка", callback_data="music")],
    [InlineKeyboardButton(text="Новости", callback_data="news")],
])

# Инлайн-кнопки с URL-ссылками
inline_keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="!Видео", callback_data="video", url="https://example.com/video")],
    [InlineKeyboardButton(text="!Музыка", callback_data="music", url="https://example.com/music")],
    [InlineKeyboardButton(text="!Новости", callback_data="news")],
])

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="!Показать больше", callback_data="show_more")],
])

inline_keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Привет", callback_data="hello"), InlineKeyboardButton(text="Пока", callback_data="bay")],
])

inline_keyboard_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
    [InlineKeyboardButton(text="Опция 2", callback_data="option_2")],
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

start = ["Привет?", "Пока?"]

dynamic = ["Опция 1", "Опция 2"]

options = ["Опция 1!", "Опция 2!", "Опция 3", "Опция 4"]

# async def test_keyboard():
#    keyboard = ReplyKeyboardBuilder()
#    for key in test:
#       keyboard.add(KeyboardButton(text=key))
#    return keyboard.adjust(2).as_markup()

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()  # InlineKeyboardBuilder() либо ReplyKeyboardBuilder() можно выполнять на выбор
   for key in test:
      keyboard.add(InlineKeyboardButton(text=key, url="https://yandex.ru/video/preview/1797773809890076088"))
   return keyboard.adjust(2).as_markup()

async def dynamic_keyboard():
   keyboard = InlineKeyboardBuilder()  # InlineKeyboardBuilder() либо ReplyKeyboardBuilder() можно выполнять на выбор
   for key in dynamic:
       keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
   return keyboard.adjust(2).as_markup()

async def options_keyboard():
   keyboard = InlineKeyboardBuilder()  # InlineKeyboardBuilder() либо ReplyKeyboardBuilder() можно выполнять на выбор
   for key in options:
       keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
   return keyboard.adjust(2).as_markup()

# # Динамическая кнопка "Показать больше"
# inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
# ])

# Кнопки "Опция 1" и "Опция 2"
inline_keyboard_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1!", callback_data="option_1")],
    [InlineKeyboardButton(text="Опция 2!", callback_data="option_2")]
])