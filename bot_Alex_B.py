import asyncio
import logging
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN_BOT_ALEX_B, WEATHER_API_KEY, NASA_API_KEY, NEWS_API_KEY
from database import create_table, add_user
from datetime import datetime, timedelta
import random
import aiohttp
from googletrans import Translator
import keyboards
# import sqlite3
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
# from aiogram.types import FSInputFile
# from aiogram.filters import CommandStart
# from aiogram import Router
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = Bot(token=TOKEN_BOT_ALEX_B)
dp = Dispatcher()
translator = Translator()

logging.basicConfig(level=logging.INFO)

button_exhange_rates = KeyboardButton(text="Курс валют")
button_News = KeyboardButton(text="Новости")
button_weather = KeyboardButton(text="Погода")
button_Nasa = KeyboardButton(text="Фото НАСА")
button_Thoughts = KeyboardButton(text="Цитаты")

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_exhange_rates, button_News, button_weather],
    [button_Nasa, button_Thoughts]
    ], resize_keyboard=True)


async def on_startup():
    await create_table()

async def extract_user_data(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    last_access = datetime.now().isoformat()
    # Сохраняем данные о пользователе
    await add_user(user_id, username, first_name, last_name, last_access)


@dp.message(Command('start'))
async def send_start(message: Message):
    user_data = await extract_user_data(message)

    await message.answer(f"Приветствую Вас, {message.from_user.full_name}!"
                         f"\nЯ бот Алексея. Выберите одну из опций в меню:", reply_markup=keyboards)


@dp.message(F.text == "Курс валют")
async def exhange_rates(message: Message):
    user_data = await extract_user_data(message)
    url = "https://v6.exchangerate-api.com/v6/3f031b399ea3af49d0a38061/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Не удалось получить данные о курсе валют!")
            return
        usd_to_rub = data['conversion_rates']['RUB']
        eur_to_usd = data['conversion_rates']['EUR']
        eur_to_rub = usd_to_rub / eur_to_usd
        # Получаем текущую дату
        current_date = datetime.now().strftime("%Y-%m-%d")  # Формат: ГГГГ-ММ-ДД

        await message.answer(f"Курс валют на {current_date}:\n"
                             f"1 USD - {usd_to_rub:.2f} RUB\n"
                            f"1 EUR - {eur_to_rub:.2f} RUB")

    except Exception as e:
        await message.answer("Произошла ошибка при получении данных.")
        print(f"Error: {e}")  # Рекомендуется логировать ошибку для дальнейшего анализа

@dp.message(F.text == "Новости")
async def news(message: Message):
    user_data = await extract_user_data(message)
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        if articles:
            news_messages = []
            for article in articles[:5]:  # Ограничиваем количество новостей
                news_messages.append(f"{article['title']}\n{article['url']}")
            await message.answer('\n'.join(news_messages))
        else:
            await message.answer('Нет доступных новостей.')
    else:
        await message.answer('Произошла ошибка при получении новостей.')


@dp.message(F.text == "Погода")
async def send_location_request(message: Message):
    user_data = await extract_user_data(message)
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
    user_data = await extract_user_data(message)
    apod = await get_random_apod()

    photo_url = apod['url']
    title = apod['title']
    await message.answer_photo(photo=photo_url, caption=f"{title}")


def get_quote():
    url = f'https://zenquotes.io/api/random'
    response = requests.get(url)
    return response.json()

# Перевод текста
def translate_text(text, target_language='ru'):
    try:
        # Проверка на наличие текста для перевода
        if not text:
            raise ValueError("Текст для перевода не может быть пустым.")
        translated = translator.translate(text, dest=target_language)

        # Проверка, что перевод действительно был выполнен
        if translated is None or not translated.text:
            raise ValueError("Перевод не удался.")
        return translated.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text  # Возвращаем исходный текст в случае ошибки

@dp.message(F.text == "Цитаты")
async def quote(message: Message):
    user_data = await extract_user_data(message)
    new_quote = get_quote()
    quote_text = new_quote[0]['q']
    translated_quote = translate_text(quote_text)
    author = new_quote[0]['a']

    await message.answer(f'"{translated_quote}" {author}\n'
                        f'({quote_text})')

async def main():
    await on_startup()  # Вызов функции на старте
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())