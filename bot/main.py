from telegram.ext import Updater, CommandHandler

from config import TELEGRAM_BOT_TOKEN
from handlers.start import start
from handlers.create import create

updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

create_handler = CommandHandler('new', create)
dispatcher.add_handler(create_handler)

updater.start_polling()


