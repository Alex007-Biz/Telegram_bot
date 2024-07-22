import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import random
import requests
# from aiogram.dispatcher import filters
import aiohttp
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
    list = ['https://avatars.dzeninfra.ru/get-zen_doc/4350071/pub_60de8be6af5456312960b7a9_60ecd6de528cff4cb60ac9e8/scale_1200',
            'https://i.ytimg.com/vi/ef_wAHtfRkg/maxresdefault.jpg',
            'https://api.rbsmi.ru/attachments/64cc0b158b2a2b1588014ad0266192ea534759ca/store/crop/0/0/660/440/1600/0/0/6b857324d3de02768ad0fc0d7fc4b5e58e4f299c32445aadddc299071650/0c2a00dd349a3a3178d00fa722443b42.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутой я')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'непонятно что это!', 'не отправляй мне такое больше!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == "Что такое ИИ")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')


@dp.message()
async def start(message: Message):
    if message.text.lower() == "тест":
        await message.answer('тестируем')
    else:
        await message.answer(f'Сам {message.text}!')
        # await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


