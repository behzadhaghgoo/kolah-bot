from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message

def start_turn(update, context):
    print("start turn")
    chat_id = update.effective_chat.id
    try:
        context.bot.delete_message(chat_id, update.message.message_id)
    except: 
        pass

    games = Game.objects(players=chat_id, status="Waiting")
    if len(games) != 1:
        print("Ey Aghaa")
        return
    game = games[0]
    game.status = "Playing"
    game.save()
    game.reload()
    update_statuses(context.bot, game)

