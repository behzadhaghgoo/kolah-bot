from bot.models.game import GameManager

reply_message = """
یه بازی جدید ساخته شد، برای اینکه باقی بچه‌ها هم جوین بشن، این لینک رو باهاشون به اشتراک بذار ;)
http://t.me/kolah_game_bot?start=%s
"""


def create(update, context):
    try:
        context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: 
        pass 

    creator_id = update.effective_chat.id
    game_id = GameManager.create_game(creator_id)
    GameManager.add_player(game_id, creator_id)
    context.bot.send_message(chat_id=creator_id, text=reply_message % game_id)
    