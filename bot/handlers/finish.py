from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message


def finish(update, context):
    print("finish")
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
    game.status = "Finished"
    game.save()
    game.reload()