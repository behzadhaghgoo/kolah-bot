from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message



reply_message = """توضیح این که بازی چطوریه"""

def start_game(update, context):
    print("start_game")
    
    try:
        context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: 
        pass 
        
    
    games = Game.objects(creator_id = update.effective_chat.id, status__ne="Finished")
    print("yare ghadimi")
    print(games)
    print(len(games))
    if len(games) != 1:
        print("Aghaa!")
        return
    print("manam hamoon")
    game = games[0]
    print("havadare ghadimi")
    game.status = "Waiting"
    game.save()
    GameManager.reset(game)
    print("hanooz hamoon")
    game.reload()
    print("kharabatio mastam")
    current_word = GameManager.get_random_word(game)
    print("vali bi to")
    update_statuses(context.bot, game)
    print("sabooye may shekastam")
    # game.active_player_index = (game.active_player_index + 1) % len(game.players)

