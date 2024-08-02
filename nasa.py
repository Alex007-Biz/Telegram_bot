import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
# from gtts import gTTS
# import os
from config2 import TOKEN, NASA_API_KEY
import keyboards as kb
import random
import requests
# import aiohttp


bot = Bot(token=TOKEN)
dp = Dispatcher()






async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())