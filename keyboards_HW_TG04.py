from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет")],
    [KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/watch?v=HfaIcB4Ogxk")],
    [InlineKeyboardButton(text="Музыка", url="https://www.youtube.com/watch?v=HfaIcB4Ogxk")],
    [InlineKeyboardButton(text="Новости", url="https://www.plitkanadom.ru")]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)

async def test_keyboard_2():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='www.plitkanadom.ru'))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)