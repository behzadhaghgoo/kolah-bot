from bot.models.game import GameManager, Game
from bot.helpers import update_statuses

reply_message = """هر کسی پنج تا کلمه بده"""

def start_getting_words(update, context):
    context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    print("start_getting_words")
    games = Game.objects(creator_id=update.effective_chat.id, status__ne="Finished")
    if len(games) != 1:
        return
    
    game = games[0]
    game.status = "Getting Words"
    game.save()
    update_statuses(context.bot, game)

    context.bot.delete_message(chat_id, update.message.message_id)