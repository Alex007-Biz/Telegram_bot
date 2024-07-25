#Импортируем библиотеки
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN  #Импортируем токен бота из конфигурационного файла

import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO) # Настраиваем уровень логирования

# Определяем состояния для формы регистрации
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('student_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

# Инициализируем базу данных
init_db()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Этот  бот поможет тебе зарегистрироваться в школе. \n Как тебя зовут?")
    await state.set_state(Form.name)  # Устанавливаем состояние на ожидание имени

# Обработчик, который принимает имя пользователя
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text) # Сохраняем имя в состоянии
    await message.answer("Сколько тебе лет?")  # Запрашиваем возраст
    await state.set_state(Form.age) # Переходим к состоянию ожидания возраста

# Обработчик, который принимает возраст пользователя
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text) # Сохраняем возраст в состоянии
    await message.answer("В каком классе ты учишься?")
    await state.set_state(Form.grade) # Переходим к состоянию ожидания класса

# Обработчик, который принимает класс пользователя
@dp.message(Form.grade)
async def city(message: Message, state:FSMContext):
    await state.update_data(grade=message.text) # Сохраняем имя в состоянии
    student_data = await state.get_data() # Получаем все данные о студенте из состояния

    # Подключаемся к базе данных для записи данных студента
    conn = sqlite3.connect('student_data.db')
    cur = conn.cursor()
    # Вставляем данные студента в таблицу
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''', (student_data['name'], student_data['age'], student_data['grade']))
    conn.commit() # Подтверждаем изменения
    conn.close()  # Закрываем подключение

    # Подтверждаем регистрацию
    await bot.send_message(message.chat.id, "Ты успешно зарегистрирован! Хорошей учебы!")

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)  # Запускаем опрос сервера для получения сообщений

# Проверяем, если скрипт выполняется как основной
if __name__ == "__main__":
    asyncio.run(main()) # Запускаем асинхронный цикл событий