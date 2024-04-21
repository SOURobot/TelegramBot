import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from parsing import main_func


BOT_TOKEN = "6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


reply_keyboard = [['/start', '/help'], ['/search', '/stop']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

params = {}


async def start(update, context):
    await update.message.reply_text("Привет!\nМеня зовут Cheap & Daily и я телеграм-бот.\nХотите выбраться из Москвы и куда-нибудь слетать? Тогда вам ко мне! Я помогу найти самые выгодные билеты, удовлетворяющие вашим пожеланиям.\nНу что, начнем?\nТогда нажимайте /search и поехали!\nP.S. Не знаете, как со мной работать? Нажмите /help для получения списка команд и прочих инструкций.", reply_markup=markup)


async def help(update, context):
    await update.message.reply_text("Привет! Cheap Daily – это телеграмм бот для удобного поиска дешевых авиабилетов.\nКак правильно использовать бота?\nДля того чтобы начать поиск нужно ввести команду /search, дальше от вас требуется ввести несколько параметров, по которым бот найдёт предложение/предложения, которые подойдут именно вам.\nПодробная инструкция по каждому параметру:\nПараметр №1:\nСколько вариантов вы хотите увидеть. Водить нужно цифру без пробелов или каких-либо иных символов\nПараметр №2:\nЖеланное время вылета. Водить нужно цифру перед, которой нужно написать “до” или “после”\nПараметр №3:\nМаксимальное время полёта. Водить нужно цифру без пробелов или каких-либо иных символов\nПараметр №4:\nМаксимальная цена билета. Как в 1-ом и 3-ем параметре, водить нужно цифру без пробелов или каких-либо иных символов\n\nУдачного использования Cheap Daily!")


async def search(update, context):
    await update.message.reply_text("Нажмите /tips для получения подсказок по поиску\nили нажмите /go для продолжения.")


async def tips(update, context):
    await update.message.reply_text("""⚠ В этом боте используется функция гибкого поиска. Рекомендуем ознакомиться с инструкциями ниже.\n
                                    """)


async def go(update, context):
    global params
    params = {}
    await update.message.reply_text("Выберите аэропорт 🏛\nПример: Внуково")
    #check
    return 1


async def first_r(update, context):
    params["airport"] = update.message.text
    await update.message.reply_text("Сколько вариантов вы хотите увидеть? 📋\nПример: 5")
    #check
    return 2


async def second_r(update, context):
    params["amount"] = int(update.message.text)
    await update.message.reply_text("Выберите время вылета 🕤\nПример: после 18")
    # check
    return 3


async def third_r(update, context):
    params["time"] = update.message.text
    await update.message.reply_text("Укажите максимальное время перелета в минутах ⏳\nПример: 180")
    # check
    return 4


async def fourth_r(update, context):
    params["duration"] = update.message.text
    await update.message.reply_text("Выберите максимальную цена билета в рублях 💵\nПример: 3000")
    # check
    return 5


async def fifth_r(update, context):
    params["cost"] = update.message.text
    await update.message.reply_text(f"✅ Ваш запрос успешно обработан!\nПроверьте введенные данные 👇\n\nАэропорт 🏛: {params['airport']}\nБудет предложено вариантов: {params['amount']}\nВремя вылета 🕤: {params['time']}\nПродолжительность ⏳: до {params['duration']}\nЦена билетов 💵: до {params['cost']}\n\nЕсли все верно, отправьте любое сообщение.")
    # add buttons
    return 6


async def sixth_r(update, context):
    x = update.message.text
    output = main_func(params)
    await update.message.reply_text(str(output))
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Поиск отменен ❌")
    return ConversationHandler.END


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("tips", tips))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('go', go)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_r)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_r)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_r)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_r)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_r)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, sixth_r)]
        },
        fallbacks=[CommandHandler('stop', stop)])

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()