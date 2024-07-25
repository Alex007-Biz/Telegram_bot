import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from gtts import gTTS
import os
from config import TOKEN
import keyboards_HW_TG04 as kb
import random
import requests
import aiohttp
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.text == "Привет")
async def test_button(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message(F.text == "Пока")
async def test_button(message: Message):
    await message.answer(f'До свидания, {message.from_user.first_name}!')

# @dp.callback_query(F.data == 'news')
# async def news(callback: CallbackQuery):
#     await callback.answer("Новости подгружаются", show_alert=True)
#     await callback.message.edit_text('Вот свежие новости', reply_markup=await kb.test_keyboard_2())


@dp.message(Command('links'))
async def links(message: Message):
    await message.answer(f'меню:', reply_markup=kb.inline_keyboard_test) #Клавиатура Inline

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer(f'Привет!', reply_markup=kb.inline_keyboard_2) #Клавиатура Inline

@dp.callback_query(F.data == "more")
async def more(callback: CallbackQuery):
    await callback.message.answer(f'Обработка нажатия на кнопку "Показать больше"', reply_markup=kb.inline_keyboard_3)

@dp.callback_query(F.data == "option1")
async def option1(callback: CallbackQuery):
    await callback.message.answer(f'Обработка нажатия на кнопку "Опция 1"')

@dp.callback_query(F.data == "option2")
async def option1(callback: CallbackQuery):
    await callback.message.answer(f'Обработка нажатия на кнопку "Опция 2"')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kb.main) #Клавиатура main
    # await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=kb.inline_keyboard_test) #Клавиатура Inline
    # await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=await kb.test_keyboard()) #keyboard Builder


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


