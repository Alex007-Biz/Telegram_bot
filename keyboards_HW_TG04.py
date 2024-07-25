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

inline_keyboard_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data='more')]
])

inline_keyboard_3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data='option1')],
    [InlineKeyboardButton(text="Опция 2", callback_data='option2')]

])

test = ["Опция 1", "Опция 2"]

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