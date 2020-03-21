from telegram.ext import Updater, CommandHandler
import mongoengine

from .config import TELEGRAM_BOT_TOKEN
from .handlers.start import start
from .handlers.create import create
from .handlers.assign_teams import assign_teams
from .handlers.start_getting_words import start_getting_words
from .handlers.add_word import add_word
from .handlers.get_status import get_status

def run():
    mongoengine.connect('kolah')
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    create_handler = CommandHandler('new', create)
    dispatcher.add_handler(create_handler)

    assign_teams_handler = CommandHandler('assign_teams', assign_teams)
    dispatcher.add_handler(assign_teams_handler)

    start_getting_words_handler = CommandHandler('start_getting_words', start_getting_words)
    dispatcher.add_handler(start_getting_words_handler)

    add_word_handler = CommandHandler('add_word', add_word)
    dispatcher.add_handler(add_word_handler)

    get_status_handler = CommandHandler('get_status', get_status)
    dispatcher.add_handler(get_status_handler)


    # /start_getting_words -> can submitted by game creator only
    # /assign_teams -> creator only, show the teams afterwards
    # /start_game -> دکمه شیشه‌ای باشه جذابتره احسنت
    # /finish_game
    # /show_scores اینو به صورت لایو هم میتونیم داشته باشیم
    updater.start_polling()

