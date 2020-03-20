from bot.models.player import Player

start_text = """
سلام! خوش اومدی، راستش این دکمه استارت کار خاصی نمی‌کنه، فقط کمک میکنه که باهات آشنا شم ;)
اینجا می‌تونی بازی جدید راه بندازی یا به یه بازی ساخته شده اضافه بشی.
خوش بگذره D:
"""

already_joined_text = """
عزیز دلِ، شما که قبلا عضو شدی :))))
"""


def start(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_chat.first_name + " " + update.effective_chat.last_name
    players = Player.objects(chat_id=chat_id)
    if len(players) != 0:
        players[0].name = name
        players[0].save()
        context.bot.send_message(chat_id=chat_id, text=already_joined_text)
        return
    new_player = Player(chat_id=chat_id, name=name)
    new_player.save()
    context.bot.send_message(chat_id=chat_id, text=start_text)
