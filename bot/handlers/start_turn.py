from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message
from threading import Timer

def end_turn(telegram_bot, game, player_index):

    def res():
        game.reload()
        if game.status != "Playing" or player_index != game.active_player_index:
            print("Bright/Forceful man :D")
            return 
        game.status = "Waiting"
        game.active_player_index = (game.active_player_index + 1) % len(game.players)
        game.save()
        game.reload()
        update_statuses(telegram_bot, game)
    
    return res

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
    print("{} second timer".format(game.rounds_timeout[game.active_round]))
    timer = Timer(game.rounds_timeout[game.active_round], end_turn(context.bot, game, game.active_player_index))
    timer.start()
