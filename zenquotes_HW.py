import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from config2 import TOKEN
import requests
# from datetime import datetime, timedelta
# import aiohttp
# from gtts import gTTS
# import os
# import keyboards as kb
# import random
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

def get_quote():
    url = f'https://zenquotes.io/api/random'
    response = requests.get(url)
    return response.json()

# Перевод текста
def translate_text(text, target_language='ru'):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text  # Возвращаем исходный текст в случае ошибки

# trr = translate_text('Hello world')
# print(trr)

@dp.message(Command("quote"))
async def quote(message: Message):
   new_quote = get_quote()
   quote_text = new_quote[0]['q']
   translated_quote = translate_text(quote_text)
   author = new_quote[0]['a']

   await message.answer(f'"{translated_quote}" ({author})\n')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Получите цитату дня: /quote')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())