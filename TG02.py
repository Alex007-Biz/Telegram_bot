import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
import requests
# from aiogram.dispatcher import filters
import aiohttp
import asyncio
from gtts import gTTS
import os
from translate  import Translator
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher()

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghijklmnopqrstuvwxyz'

@dp.message()
async def echo(message: types.Message):
    text = message.text.strip()  # Убираем лишние пробелы
    if not text:  # Проверка на пустое сообщение
        await message.answer("Сообщение пустое.")
        return

    if text[0].lower() in ru_letters:
        translator = Translator(from_lang='russian', to_lang='english')
    elif text[0].lower() in en_letters:
        translator = Translator(from_lang='english', to_lang='russian')
    else:
        await message.answer("Я не понимаю языка этого сообщения.")
        return
    translation = translator.translate(text)
    await message.answer(translation)


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('audio'))
async def audio(message: Message):
    # await bot.send_chat_action(message.chat.id, 'upload_video')
    audio = FSInputFile("audio.m4a")
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f'Это ваша мини-тренировка на сегодня {rand_tr}')
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save('training.ogg')
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('training.ogg')

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://avatars.dzeninfra.ru/get-zen_doc/4350071/pub_60de8be6af5456312960b7a9_60ecd6de528cff4cb60ac9e8/scale_1200',
            'https://i.ytimg.com/vi/ef_wAHtfRkg/maxresdefault.jpg',
            'https://api.rbsmi.ru/attachments/64cc0b158b2a2b1588014ad0266192ea534759ca/store/crop/0/0/660/440/1600/0/0/6b857324d3de02768ad0fc0d7fc4b5e58e4f299c32445aadddc299071650/0c2a00dd349a3a3178d00fa722443b42.jpg'
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это я - супер бот!')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'непонятно что это!', 'не отправляй мне такое больше!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


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
        await message.answer(f'Сам ты {message.text}!')
        # await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


