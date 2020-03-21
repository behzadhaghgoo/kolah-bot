from bot.models.game import GameManager


reply_message = """توضیح این که بازی چطوریه"""

def start_game(update, context):
    game_id = context.args[0]
    game = GameManager.get_game(game_id)
    while game.status != "Done":
        current_word = GameManager.get_random_word(game_id)
