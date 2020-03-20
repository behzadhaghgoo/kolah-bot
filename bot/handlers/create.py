import random
from bot.models.game import GameManager

reply_message = """
یه بازی جدید ساخته شد، برای اینکه باقی بچه‌ها هم جوین بشن، این لینک رو باهاشون به اشتراک بذار ;)
https://telegram.me/kolah_game_bot?join=%s
"""


def create(update, context):
    creator_id = str(update.effective_chat.id)
    game_id = GameManager.create_game(creator_id)
    context.bot.send_message(chat_id=creator_id, text=reply_message % game_id)
