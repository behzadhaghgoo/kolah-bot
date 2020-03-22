from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message

def correct(update, context):
    print("correct")

    chat_id = update.effective_chat.id
    try:
        context.bot.delete_message(chat_id, update.message.message_id)
    except:
        pass
    
    games = Game.objects(players=chat_id, status__ne="Finished")

    if len(games) == 0:
        print("games:", len(game))
        update_message(context.bot, player, "فعلا تو بازی‌ای نیستی D:")
        return

    if len(games) > 1:
        print("nakon dige")
        return 

    game = games[0]
    if game.players[game.active_player_index] == chat_id:
        game.teams[game.active_player_index % (len(game.players)//2)].score += 1
        game.save()
        game.update(pull__remaining_words=game.current_word)
        game.reload()
        GameManager.get_random_word(game)
    game.save()
    game.reload()
    update_statuses(context.bot, game)

    context.bot.delete_message(chat_id, update.message.message_id)