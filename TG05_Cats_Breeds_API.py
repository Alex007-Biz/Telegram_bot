import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests

from config import TOKEN, THE_CAT_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breeds():
   url = 'https://api.thecatapi.com/v1/breeds'
   headers = {'x-api-key' : THE_CAT_API_KEY}
   response = requests.get(url, headers=headers)
   return response.json()
def get_cat_image_by_breed(breed_id):
   url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
   headers = {'x-api-key' : THE_CAT_API_KEY}
   response = requests.get(url, headers=headers)
   data = response.json()
   return data[0]['url']

def get_breed_info(breed_name):
   breeds = get_cat_breeds()
   for breed in breeds:
      if breed['name'].lower() == breed_name.lower():
         return breed
   return None

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer("Привет! Напиши мне название породы кошки и я пришлю ее фотку и информацию о ней")

@dp.message(Command('breeds'))
async def breeds(message: Message):
    breeds = get_cat_breeds()
    await message.answer("Породы кошек:")
    for breed in breeds:
       await message.answer(f"Порода: {breed['name']}\n")

@dp.message()
async def send_cat_info(message: Message):
   breed_name = message.text
   breed_info = get_breed_info(breed_name)
   if breed_info:
      cat_image_url = get_cat_image_by_breed(breed_info['id'])
      info = (f"Порода - {breed_info['name']}\n"
              f"Описание - {breed_info['description']}\n"
              f"Продолжительность жизни - {breed_info['life_span']} лет")
      await message.answer_photo(photo=cat_image_url, caption=info)
   else:
      await message.answer("Порода не найдена. Попробуйте еще раз.")

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())