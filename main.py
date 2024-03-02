import telebot
from responses import *
from time import sleep
from collect_keys import get_info, search_object

bot = telebot.TeleBot('6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA')

# airport = ""
# airline = ""
# time = ""
# duration = ""
# cost = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = message.text
    if message.text == "/start":
        # global airport, airline, time, duration, cost
        # airport = ""
        # airline = ""
        # time = ""
        # duration = ""
        # cost = ""
        bot.send_message(message.from_user.id, ans(msg))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, ans(msg))
    elif message.text == "/search":
        bot.send_message(message.from_user.id, ans(msg))
        sleep(4.0)
        get_info()
        bot.send_message(message.from_user.id, f"✅ Ваш запрос успешно обработан!\nПроверьте введенные данные 👇\nАэропорт 🏛: {search_object['airport']}\nАвиакомпания ✈: {search_object['airline']}\n Время вылета 🕤: {search_object['time']}\nПродолжительность ⏳: до {search_object['duration']}\nЦена билетов 💵: до {search_object['cost']}")
    else:
        bot.send_message(message.from_user.id, ans(message.text))


# def get_airport(message):
#     global airport
#     airport = message.text
#     bot.send_message(message.from_user.id, 'Выберите авиакомпанию 👉\nПример: Аэрофлот')
#     bot.register_next_step_handler(message, get_airline)
#
#
# def get_airline(message):
#     global airline
#     airline = message.text
#     bot.send_message(message.from_user.id, 'Выберите время вылета 👉\nПример: утро')
#     bot.register_next_step_handler(message, get_time)
#
#
# def get_time(message):
#     global time
#     time = message.text
#     bot.send_message(message.from_user.id, 'Выберите максимальную продолжительность полета в часах 👉\nПример: 3')
#     bot.register_next_step_handler(message, get_duration)
#
#
# def get_duration(message):
#     global duration
#     duration = message.text
#     bot.send_message(message.from_user.id, 'Выберите максимальную цена билета в рублях 👉\nПример: 3000')
#     bot.register_next_step_handler(message, get_cost)
#
#
# def get_cost(message):
#     global cost
#     while cost == 0:
#         try:
#             cost = int(message.text)
#         except Exception:
#             bot.send_message(message.from_user.id, '⚠ Введите одно целое число')

bot.polling(none_stop=True, interval=0)