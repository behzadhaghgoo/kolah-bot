from bot.models.game import GameManager, Game
from bot.helpers import update_statuses

def add_word(update, context):
    context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    print("add word")
    games = Game.objects(players=update.effective_chat.id, status="Getting Words")
    if len(games) != 1:
        print("games:", len(game))
        return
    
    game = games[0]
    word = update.message.text.split("/add_word")[1].strip()
    print(word, game)
    game = GameManager.add_words(game, word)
    update_statuses(context.bot, game)

