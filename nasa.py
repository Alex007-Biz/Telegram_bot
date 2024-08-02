import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
# from gtts import gTTS
# import os
from config2 import TOKEN, NASA_API_KEY
# import keyboards as kb
import random
import requests
from datetime import datetime, timedelta
# import aiohttp


bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
    response = requests.get(url)
    return response.json()

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
   title = apod['title']

   await message.answer_photo(photo=photo_url, caption=f"{title}")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот NASA!')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())