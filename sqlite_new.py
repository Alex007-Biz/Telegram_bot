import sqlite3

conn = sqlite3.connect('bot.db')
cusor = conn.cursor()

cusor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    chat_id INTEGER)''')

conn.commit()
conn.close()