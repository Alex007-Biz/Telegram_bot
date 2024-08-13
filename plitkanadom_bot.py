import os
   import openai
   from telegram import Update
   from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

   # Установите ваш токен и API-ключ
   TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

   openai.api_key = OPENAI_API_KEY

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

   if __name__ == '__main__':
       asyncio.run(main())