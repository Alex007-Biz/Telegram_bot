from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопка 1")],
    [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/watch?v=HfaIcB4Ogxk")]
])