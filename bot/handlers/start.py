from bot.helpers import update_statuses, update_message
from bot.models.player import Player
from bot.models.game import GameManager

start_text = """
سلام من به تو یار قدیمی! خوش اومدی، راستش این دکمه استارت کار خاصی نمی‌کنه، فقط کمک میکنه که باهات آشنا شم ;)
اینجا می‌تونی بازی جدید راه بندازی یا به یه بازی ساخته شده اضافه بشی.
خوش بگذره :D
"""

already_joined_text = """
عزیز دلِ، شما که قبلا عضو شدی :))))
"""

join_game_text = """
شما به بازی اضافه شدید.
"""


def start(update, context):
    context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    chat_id = update.effective_chat.id
    name = str(update.effective_chat.first_name) + " " + str(update.effective_chat.last_name)
    players = Player.objects(chat_id=chat_id)
    if len(players) != 0:
        players[0].name = name
        players[0].save()
    else:
        new_player = Player(chat_id=chat_id, name=name)
        new_player.save()
        update_message(context.bot, new_player, text=start_text)

    if len(context.args):
        game_id = context.args[0]
        result, game = GameManager.add_player(game_id, chat_id)
        if result:
            update_statuses(context.bot, game)

    # context.bot.delete_message(chat_id, update.message.message_id)