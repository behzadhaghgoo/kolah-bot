from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message

def next_player(update, context):
    print("next_player")
    chat_id = update.effective_chat.id
    try:
        context.bot.delete_message(chat_id, update.message.message_id)
    except: 
        pass
    games = Game.objects(creator_id=chat_id, status__ne="Finished")
    print("nagoo nagoo nemiam")
    if len(games) == 0:
        print("games:", len(game))
        update_message(context.bot, player, "فعلا تو بازی‌ای نیستی D:")
        return
    if len(games) > 1:
        print("nakon dige")
        return 
    game = games[0]
    game.active_player_index = (game.active_player_index + 1) % len(game.players)
    current_word = GameManager.get_random_word(game)
    game.save()
    game.reload()
    update_statuses(context.bot, game)

    context.bot.delete_message(chat_id, update.message.message_id)



def prev_player(update, context):
    print("prev_player")
    try:
        context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except:
        pass
        
    chat_id = update.effective_chat.id
    games = Game.objects(creator_id=chat_id, status__ne="Finished")
    print("nagoo nagoo nemiam")
    if len(games) == 0:
        print("games:", len(game))
        update_message(context.bot, player, "فعلا تو بازی‌ای نیستی D:")
        return
    print("nagoo nagoo nemiam")
    if len(games) > 1:
        print("nakon dige")
        return 
    print("omido par dadan")
    game = games[0]
    game.active_player_index = (game.active_player_index - 1) % len(game.players)
    print("dige sakhte baram aam")
    # current_word = GameManager.get_random_word(game)
    print("hala ke")
    game.save()
    print("daste goldoon")
    game.reload()
    print("be sagheye")
    update_statuses(context.bot, game)

    context.bot.delete_message(chat_id, update.message.message_id)