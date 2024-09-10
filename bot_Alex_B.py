import asyncio
import logging
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN_BOT_ALEX_B
from datetime import datetime
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp


bot = Bot(token=TOKEN_BOT_ALEX_B)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_exhange_rates = KeyboardButton(text="Курс валют")
button_Nasa = KeyboardButton(text="Фото НАСА")
button_weather = KeyboardButton(text="Погода")
button_Thoughts = KeyboardButton(text="Философские мысли")

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_exhange_rates, button_Nasa],
    [button_weather, button_Thoughts]
    ], resize_keyboard=True)


@dp.message(Command('start'))
async def send_start(message: Message):
    await message.answer(f"Приветствую Вас, {message.from_user.full_name}!"
                         f"\nЯ личный бот Алексея. Выберите одну из опций в меню:", reply_markup=keyboards)


@dp.message(F.text == "Курс валют")
async def exhange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/3f031b399ea3af49d0a38061/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось данные о курсе валют!")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        eur_to_rub = usd_to_rub / eur_to_usd
        # Получаем текущую дату
        current_date = datetime.now().strftime("%Y-%m-%d")  # Формат: ГГГГ-ММ-ДД

        await message.answer(f"Курс валют на {current_date}:\n"
                             f"1 USD - {usd_to_rub:.2f} RUB\n"
                            f"1 EUR - {eur_to_rub:.2f} RUB")
    except:
        await message.answer("Произошла ошибка")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())