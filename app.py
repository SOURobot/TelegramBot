import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from responses import ans


BOT_TOKEN = "6291281713:AAHrleKYDcmcciulEkQINb1XQcaSiCFfvcA"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


reply_keyboard = [['/search', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update, context):
    await update.message.reply_html(ans("/start"), reply_markup=markup)


async def answer(update, context):
    await update.message.reply_text(ans(update.message.text))


async def help(update, context):
    await update.message.reply_text(ans("/help"))


async def search(update, context):
    await update.message.reply_text(ans("/search"))


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, answer)
    app.add_handler(text_handler)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()


if __name__ == "__main__":
    main()