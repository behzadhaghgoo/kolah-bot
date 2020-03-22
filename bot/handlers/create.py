from bot.models.game import GameManager, Game
from bot.helpers import update_statuses



def create(update, context):
    try:
        context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: 
        pass 

    creator_id = update.effective_chat.id
    if len(Game.objects(players=creator_id, status__ne="Finished")) != 0:
        return

    game_id = GameManager.create_game(creator_id)
    res, game = GameManager.add_player(game_id, creator_id)
    update_statuses(context.bot, game)
    # context.bot.send_message(chat_id=creator_id, text=reply_message % game_id)
    