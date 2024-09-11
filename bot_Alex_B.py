import asyncio
import logging
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN_BOT_ALEX_B, WEATHER_API_KEY, NASA_API_KEY
from datetime import datetime, timedelta
import aiohttp
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

@dp.message(F.text == "Погода")
async def send_location_request(message: Message):
    # Необходимо явно указывать параметр 'keyboard', даже если пусто
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Отправить местоположение", request_location=True)]
        ],
        resize_keyboard=True
    )
    await message.answer('Пожалуйста, отправьте свое местоположение (нажмите на кнопку "Отправить местоположение"):', reply_markup=keyboard)

# Используем правильный фильтр для сообщений с местоположением
@dp.message(F.content_type == "location")
async def get_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await message.answer(f"Ваше местоположение: Широта: {latitude}, Долгота: {longitude}")

    # Запрос к API погоды
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Проверка на успешный ответ
        data = response.json()

        city = data['name']
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']

        await message.answer(f"Погода в {city}:\nТемпература: {temperature}°C\nОписание: {weather_description}",
                             reply_markup=keyboards)
    except requests.RequestException as e:
        await message.answer("Не удалось получить данные о погоде. Пожалуйста, попробуйте позже.")
        print(f"Ошибка запроса: {e}")

async def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")
    # logging.info(f"Generated date: {date_str}")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@dp.message(F.text == "Фото НАСА")
async def random_apod(message: Message):
    # logging.info("Handler random_apod triggered")
    apod = await get_random_apod()
    # logging.info(f"APOD data received: {apod}")
    # if apod['media_type'] == 'image':
    photo_url = apod['url']
    title = apod['title']
    await message.answer_photo(photo=photo_url, caption=f"{title}")
    # else:
    #     await message.answer(f"Сегодняшний медиафайл: {apod['title']}\n{apod['url']}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())