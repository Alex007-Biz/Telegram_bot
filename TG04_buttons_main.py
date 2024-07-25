import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from gtts import gTTS
import os
from config import TOKEN
import keyboards as kb
import random
import requests
import aiohttp
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kb.main)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


