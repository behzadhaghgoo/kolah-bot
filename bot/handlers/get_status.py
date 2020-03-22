from bot.models.game import GameManager, Game
from bot.models.player import Player
from bot.helpers import update_statuses, update_message


def get_status(update, context):
    chat_id = update.effective_chat.id
    context.bot.delete_message(chat_id, update.message.message_id)
    print("get status")
    
    games = Game.objects(players=chat_id, status__ne="Finished")
    player = Player.objects(chat_id=chat_id)[0]

    player.status_message_id = None
    player.save()

    if len(games) == 0:
        update_message(context.bot, player, "فعلا تو بازی‌ای نیستی D:")
        return

    if len(games) > 1:
        print("nakon dige")
        return 
        
    game = games[0]
    update_statuses(context.bot, game)