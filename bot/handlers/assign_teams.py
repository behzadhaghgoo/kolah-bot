from bot.models.game import GameManager, Game
from bot.helpers import update_statuses


reply_message = """خب تیم‌بندی کنیم"""

def assign_teams(update, context):
    print(update.__dict__)
    games = Game.objects(creator_id=update.effective_chat.id, status__ne="Finished")
    if len(games) != 1:
        return
    game = games[0]
    GameManager.assign_teams(game)
    if game:
        game.status = "Team Assignment"
        game.save()
        update_statuses(context.bot, game)

    