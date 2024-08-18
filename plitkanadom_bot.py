import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import requests
import os
from config2 import TOKEN_PLITKA_BOT, OPENAI_API_KEY
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from openai import OpenAI
client = OpenAI()


# Установите ваш токен и API-ключ
TOKEN = TOKEN_PLITKA_BOT
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, готов помочь вам с отделочными материалами.')

def respond(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message},
        ]
    )
    bot_reply = response['choices'][0]['message']['content']
    update.message.reply_text(bot_reply)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()
    updater.idle()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())