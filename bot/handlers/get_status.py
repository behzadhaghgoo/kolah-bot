from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message


def get_status(update, context):
    print("get status")
    chat_id = update.effective_chat.id
    games = Game.objects(players=chat_id, status__ne="Finished")
    player = Player.objects(chat_id=chat_id)[0]

    if len(games) == 0:
        print("games:", len(game))
        update_message(context.bot, player, "فعلا تو بازی‌ای نیستی D:")
        return

    if len(games) > 1:
        print("nakon dige")
        return 

    game = games[0]
    player.status_message_id = None
    player.save()
    update_statuses(context.bot, game)