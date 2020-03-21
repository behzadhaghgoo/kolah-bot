from .models.game import Game
from .models.player import Player

joining_status = """
بازیکنان فعال:
%s
"""


def update_message(telegram_bot, player, text):
    if player.status_message_id is None:
        message = telegram_bot.send_message(chat_id=player.chat_id, text=text)
        player.status_message_id = message.message_id
        player.save()
    else:
        telegram_bot.edit_message_text(text, chat_id=player.chat_id, message_id=player.status_message_id)


def update_statuses(telegram_bot, game):
    players = Player.objects(chat_id__in=game.players)
    active_players_text = "\n".join(["%d.%s" % (index + 1, player.name) for index, player in enumerate(players)])
    if game.status == "Joining":
        for player in players:
            update_message(telegram_bot, player, joining_status % active_players_text)