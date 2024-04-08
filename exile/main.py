import telebot

from exile.responses import *
from parsing import *

from time import sleep
from telebot import types

bot = telebot.TeleBot('6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA')

reqs = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        main_func(reqs)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пока ничем не могу помочь')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = message.text
    if message.text == "/start":
        global airport, airline, time, duration, cost
        airport = ""
        airline = ""
        time = ""
        duration = ""
        cost = ""
        bot.send_message(message.from_user.id, ans(msg))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, ans(msg))
    elif message.text == "/search":
        bot.send_message(message.from_user.id, ans(msg))
        sleep(4.0)
        bot.send_message(message.from_user.id, 'Выберите аэропорт 🏛\nПример: Внуково')
        bot.register_next_step_handler(message, get_airport)
    else:
        bot.send_message(message.from_user.id, ans(message.text))


def get_airport(message):
    reqs["airport"] = message.text
    bot.send_message(message.from_user.id, 'Выберите количество пассажиров 🙂\nПример: 2')
    bot.register_next_step_handler(message, get_passengers)


def get_passengers(message):
    reqs["passengers"] = message.text
    bot.send_message(message.from_user.id, 'Выберите время вылета 🕤\nПример: после 18')
    bot.register_next_step_handler(message, get_time)


def get_time(message):
    reqs["time"] = message.text
    bot.send_message(message.from_user.id, 'Выберите максимальную продолжительность полета в часах ⏳\nПример: 3')
    bot.register_next_step_handler(message, get_duration)


def get_duration(message):
    reqs["duration"] = message.text
    bot.send_message(message.from_user.id, 'Выберите максимальную цена билета в рублях 💵\nПример: 3000')
    bot.register_next_step_handler(message, get_cost)


def get_cost(message):
    reqs["cost"] = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Искать 🔍', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Редактировать ✏', callback_data='no')
    keyboard.add(key_no)
    question = f"✅ Ваш запрос успешно обработан!\nПроверьте введенные данные 👇\nАэропорт 🏛: {reqs['airport']}\nВсего пассажиров 🙂: {reqs['passengers']}\nВремя вылета 🕤: {reqs['time']}\nПродолжительность ⏳: до {reqs['duration']}\nЦена билетов 💵: до {reqs['cost']}"

    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)