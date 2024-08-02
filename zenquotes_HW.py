import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
# from gtts import gTTS
# import os
from config2 import TOKEN
# import keyboards as kb
import random
import requests
# from datetime import datetime, timedelta
# import aiohttp


bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_quote():
    url = f'https://zenquotes.io/api/random'
    response = requests.get(url)
    return response.json()

# q = get_quote()
# print(q)

@dp.message(Command("quote"))
async def quote(message: Message):
   new_quote = get_quote()
   quote_text = new_quote[0]['q']
   author = new_quote[0]['a']

   await message.answer(f'"{quote_text}" ({author})\n')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Получите цитату дня: /quote')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())