import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

BOT_TOKEN = "6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


reply_keyboard = [['/start', '/help'], ['/search', '/stop']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

params = {}


async def start(update, context):
    await update.message.reply_text("Привет!\nМеня зовут Cheap & Daily и я телеграм-бот.\nХотите выбраться из Москвы и куда-нибудь слетать? Тогда вам ко мне! Я помогу найти самые выгодные билеты, удовлетворяющие вашим пожеланиям.\nНу что, начнем?\nТогда нажимайте /search и поехали!\nP.S. Не знаете, как со мной работать? Нажмите /help для получения списка команд и прочих инструкций.", reply_markup=markup)


async def help(update, context):
    await update.message.reply_text("К сожалению, пока я не могу вам ни чем помочь.")


async def search(update, context):
    await update.message.reply_text("Нажмите /tips для получения подсказок по поиску\nили нажмите /go для продолжения.")


async def tips(update, context):
    await update.message.reply_text("В данный момент подсказки отсутствуют.\nНажмите /go для продолжения.")


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
    params["amount"] = update.message.text
    await update.message.reply_text("Выберите время вылета 🕤\nПример: после 18")
    # check
    return 3


async def third_r(update, context):
    params["time"] = update.message.text
    await update.message.reply_text("Выберите максимальную продолжительность полета в часах ⏳\nПример: 3")
    # check
    return 4


async def fourth_r(update, context):
    params["duration"] = update.message.text
    await update.message.reply_text("Выберите максимальную цена билета в рублях 💵\nПример: 3000")
    # check
    return 5


async def fifth_r(update, context):
    params["cost"] = update.message.text
    await update.message.reply_text(f"✅ Ваш запрос успешно обработан!\nПроверьте введенные данные 👇\nАэропорт 🏛: {params['airport']}\nБудет предложено вариантов: {params['amount']}\nВремя вылета 🕤: {params['time']}\nПродолжительность ⏳: до {params['duration']}\nЦена билетов 💵: до {params['cost']}")
    # add buttons
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
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_r)]
        },
        fallbacks=[CommandHandler('stop', stop)])

    app.add_handler(conv_handler)
    app.run_polling()


if __name__ == "__main__":
    main()