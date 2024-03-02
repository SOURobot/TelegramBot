import telebot
from responses import *
from time import sleep

bot = telebot.TeleBot('6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA')

airport = ""
airline = ""
time = ""
duration = ""
cost = 0


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
        bot.send_message(message.from_user.id, 'Выберите аэропорт (например, Внуково):')
        bot.register_next_step_handler(message, get_airport)
    else:
        bot.send_message(message.from_user.id, ans(message.text))


def get_airport(message):
    global airport
    airport = message.text
    bot.send_message(message.from_user.id, 'Выберите авиакомпанию (например, Аэрофлот)')
    bot.register_next_step_handler(message, get_airline)


def get_airline(message):
    global airline
    airline = message.text
    bot.send_message(message.from_user.id, 'Выберите время вылета (например, утро):')
    bot.register_next_step_handler(message, get_time)


def get_time(message):
    global time
    time = message.text
    bot.send_message(message.from_user.id, 'Выберите максимальную продолжительность полета (например, 3):')
    bot.register_next_step_handler(message, get_duration)


def get_duration(message):
    global time
    time = message.text
    bot.send_message(message.from_user.id, 'Выберите максимальную цена билета (например, 3000):')
    bot.register_next_step_handler(message, get_cost)


def get_cost(message):
    global cost
    while cost == 0:
        try:
            cost = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

    bot.send_message(message.from_user.id, "Ваш запрос успешно обработан!")


bot.polling(none_stop=True, interval=0)