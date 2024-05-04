### Шаг 3: Подготовка кода для бота
#Создаем код бота для общения с пользователем и выполнения функций добавления, отслеживания и отмечания выполнения привычек.
#pip install pyTelegramBotAPI
import telebot
import datetime #позволяет работать с датой и работать со временем
import time #используется в основном для задержек. То есть, с помощью него можно, например, программу приостановить на 60 или 5 секунд, или на какое-то другое время. Потом она снова начнет работать.
import threading #ужен для работы с потоками
import random
import sqlite3


TOKEN = '7121309234:AAFP6PfgdA1n9krO0OROiRI3EkdQSeYVETU'  # Замените YOUR_BOT_TOKEN на токен вашего бота
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных пользователей
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Добавление пользователя в базу данных
def add_user(user_id, first_name, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (id, first_name, username) VALUES (?, ?, ?)', (user_id, first_name, username))
        conn.commit()
    conn.close()


# Обработчик команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    # Сохранение пользователя в базе данных
    add_user(user_id, first_name, username)

    bot.reply_to(message, f"Привет, {first_name}! Твои данные сохранены.")

    bot.reply_to(message, text='Привет, я бот-ассистент, который поможет тебе работать над собой /help')
    # reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))# создаем поток
    # reminder_thread.start()# запускаем поток

if __name__ == '__main__':
    create_table()  # Создать таблицу, если она еще не создана

# Обработчик команды help
@bot.message_handler(commands=['help'])
def help_message (message):
    help_text = """
    Вот что я умею:
    /start - начать работу
    /help - получить справку по командам
    /positive_habits - список положительных привычек
    /negative_habits - список отрицательных привычек
    /list_remind - список напомнинаний   
    /addhabit - привычка которую надо сохранить
    /complete - удалить привычку
    /statistics - отчеты о выполнении привычек
    /diagram - график выполнения 
    """
    bot.send_message(message.chat.id, text=help_text)

@bot.message_handler(commands=['positive_habits'])
def show_positive_habits(message):
    habits = fetch_habits('positive_habits1.db')
    if habits:
        response = "\n".join([habit[0] for habit in habits])
        bot.send_message(message.chat.id, "Положительные привычки:\n" + response)
    else:
        bot.send_message(message.chat.id, "Список положительных привычек пуст.")

@bot.message_handler(commands=['negative_habits'])
def show_negative_habits(message):
    habits = fetch_habits('negative_habits1.db')
    if habits:
        response = "\n".join([habit[0] for habit in habits])
        bot.send_message(message.chat.id, "Негативные привычки:\n" + response)
    else:
        bot.send_message(message.chat.id, "Список негативных привычек пуст.")



# Запуск бота
bot.polling(non_stop=True)
