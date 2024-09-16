import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN_aioAlex_Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_aioAlex_Bot)
dp = Dispatcher()

@dp.message(Command('start'))
async def send_start(message: Message):
    await message.answer("Привет! Я минимальный бот.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())