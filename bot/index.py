from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import mongoengine

from .config import TELEGRAM_BOT_TOKEN, PORT, WEBHOOK_URL
from .handlers.start import start
from .handlers.create import create
from .handlers.assign_teams import assign_teams
from .handlers.start_getting_words import start_getting_words
from .handlers.add_word import add_word
from .handlers.get_status import get_status
from .handlers.start_game import start_game
from .handlers.correct import correct
from .handlers.next_player import next_player, prev_player
from .handlers.finish import finish
from .handlers.button import button
from .handlers.start_turn import start_turn

def run():
    mongoengine.connect('kolah')
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('new', create))
    dispatcher.add_handler(CommandHandler('assign_teams', assign_teams))
    dispatcher.add_handler(CommandHandler('start_getting_words', start_getting_words))
    # dispatcher.add_handler(CommandHandler('add_word', add_word))    
    dispatcher.add_handler(CommandHandler('get_status', get_status))    
    dispatcher.add_handler(CommandHandler('start_game', start_game))
    dispatcher.add_handler(CommandHandler('start_turn', start_turn))
    dispatcher.add_handler(CommandHandler('correct', correct))
    dispatcher.add_handler(CommandHandler('next_player', next_player))
    dispatcher.add_handler(CommandHandler('prev_player', prev_player))
    dispatcher.add_handler(CommandHandler('finish', finish))

    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(MessageHandler(Filters.text, add_word))
    
    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/inlinekeyboard.py#L29
    

    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example

    # /start_getting_words -> can submitted by game creator only
    # /assign_teams -> creator only, show the teams afterwards
    # /start_game -> دکمه شیشه‌ای باشه جذابتره احسنت
    # /finish_game
    # /show_scores اینو به صورت لایو هم میتونیم داشته باشیم
    updater.start_webhook(listen='0.0.0.0',
                      port=PORT,
                      url_path=TELEGRAM_BOT_TOKEN,
                      key='private.key',
                      cert='cert.pem',
                      webhook_url=WEBHOOK_URL + TELEGRAM_BOT_TOKEN)


