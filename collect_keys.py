from main import bot

counter = 0


def get_info(message=None):
    global counter

    if counter - 1 >= 0:
        prev_object = ASK_LIST[counter - 1]
        search_object[prev_object] = ASK_TYPE[prev_object](message.text)
        #search_object[prev_object] = message + '-' + str(counter - 1)
        if counter == len(ASK_LIST):
            counter = 0
            return

    object_name = ASK_LIST[counter]
    bot.send_message(message.from_user.id, ASK_TEXT[object_name])

    if ASK_TYPE[object_name] != str:
        try:
            search_object[counter] = ASK_TYPE[object_name](message.text)
        except Exception:
            bot.send_message(message.from_user.id, '⚠ Введите одно целое число')

    #Здесь можно осуществить проверку с помощью ASK_SPEC

    if counter + 1 <= len(ASK_LIST):
        counter += 1
        bot.register_next_step_handler(message, get_info)


search_object = {"airport": "",
                 "airline": "",
                 "time": "",
                 "duration": "",
                 "cost": 0}

ASK_LIST = ["airport", "airline", "time", "duration", "cost"]

ASK_TEXT = {"airport": 'Выберите аэропорт 👉\nПример: Внуково',
            "airline": 'Выберите авиакомпанию 👉\nПример: Аэрофлот',
            "time": 'Выберите время вылета 👉\nПример: утро',
            "duration": 'Выберите максимальную продолжительность полета в часах 👉\nПример: 3',
            "cost": 'Выберите максимальную цена билета в рублях 👉\nПример: 3000'}

ASK_TYPE = {"airport": str,
            "airline": str,
            "time": str,
            "duration": str,
            "cost": int}


#здесь можно сохранить какие-нибудь фацлы всех аэропортов и т.п. вещей
#(т.е. если нам нужны будут именно значения из какого НАБОРА ЗНАЧЕНИЙ,то эти наборы будут находится здесь)
ASK_SPEC = {}