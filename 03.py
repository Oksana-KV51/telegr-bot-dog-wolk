import telebot
from telebot import types
import datetime #позволяет работать с датой и работать со временем
import time #используется в основном для задержек. То есть, с помощью него можно, например, программу приостановить на 60 или 5 секунд, или на какое-то другое время. Потом она снова начнет работать.
import threading #ужен для работы с потоками
import random
import sqlite3

TOKEN = '7121309234:AAFP6PfgdA1n9krO0OROiRI3EkdQSeYVETU'  # Замените YOUR_BOT_TOKEN на токен вашего бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню", callback_data='open_menu')
    markup.add(menu_button)
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'open_menu')
def callback_query(call):
    bot.answer_callback_query(call.id, "Вы нажали Меню!")
    bot.send_message(call.message.chat.id, "Здесь может быть ваше меню.")

bot.polling(non_stop=True)