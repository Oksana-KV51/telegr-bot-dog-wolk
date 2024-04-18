### Шаг 2: Создание базы данных и таблиц
#Создадим базу данных SQLite для хранения данных о привычках.

import sqlite3
def init_db():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            habit_name TEXT,
            description TEXT,
            frequency INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            habit_id INTEGER,
            date TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

### Шаг 3: Подготовка кода для бота
#Создаем код бота для общения с пользователем и выполнения функций добавления, отслеживания и отмечания выполнения привычек.

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

TOKEN = '7121309234:AAFP6PfgdA1n9krO0OROiRI3EkdQSeYVETU'  # Замените YOUR_BOT_TOKEN на токен вашего бота
bot = telebot.TeleBot(TOKEN)

def remind_habits():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    now = datetime.date.today()
    c.execute("SELECT id, user_id, habit_name FROM habits WHERE frequency <= ?",
              ((now - datetime.date(2000, 1, 1)).days % 7,))
    habits = c.fetchall()
    for habit in habits:
        bot.send_message(habit[1], f"Не забудьте выполнить привычку: {habit[2]}")
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(remind_habits, 'interval', days=1)
scheduler.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я помогу тебе отслеживать твои привычки. Используй команды /addhabit чтобы добавить новую привычку.")
@bot.message_handler(commands=['help'])
def help_message (message):
    help_text = """
    Вот что я умею:
    /start - начать работу со мной
    /help - получить справку по командам
    /addhabit - привычка которую надо сохранить
    """
    bot.send_message(message.chat.id, text=help_text)

@bot.message_handler(commands=['addhabit'])
def add_habit(message):
    msg = bot.send_message(message.chat.id, "Введите название привычки:")
    bot.register_next_step_handler(msg, process_habit_name_step)

def process_habit_name_step(message):
    habit_name = message.text
    user_id = message.from_user.id
    msg = bot.send_message(message.chat.id, "Введите описание привычки:")
    bot.register_next_step_handler(msg, process_description_step, user_id, habit_name)

def process_description_step(message, user_id, habit_name):
    description = message.text
    msg = bot.send_message(message.chat.id, "Как часто вы планируете выполнять эту привычку? (введите число дней между повторениями)")
    bot.register_next_step_handler(msg, process_frequency_step, user_id, habit_name, description)

def process_frequency_step(message, user_id, habit_name, description):
    frequency = int(message.text)
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('INSERT INTO habits (user_id, habit_name, description, frequency) VALUES (?, ?, ?, ?)',
              (user_id, habit_name, description, frequency))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Привычка сохранена успешно!")

bot.infinity_polling(none_stop=True, interval=0)
