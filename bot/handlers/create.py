import random
from game.game import Game

games = dict()
creators = dict()

reply_message = """
یه بازی جدید ساخته شد، برای اینکه باقی بچه‌ها هم جوین بشن، این لینک رو باهاشون به اشتراک بذار ;)
https://telegram.me/kolah_game_bot?join=%s
"""


def get_random_id():
    return str(random.randint(10000, 99999))


def create_new_game():
    game_id = get_random_id()
    while game_id in games:
        game_id = get_random_id()

    games[game_id] = Game()
    return game_id


def create(update, context):
    game_id = create_new_game()
    creator_id = update.effective_chat.id
    creators[game_id] = creator_id
    print(creator_id)
    games[game_id].add_player([creator_id])
    print("ha?")
    context.bot.send_message(chat_id=creator_id, text=reply_message % game_id)
