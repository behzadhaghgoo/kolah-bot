
start_text = """
سلام! خوش اومدی، راستش این دکمه استارت کار خاصی نمی‌کنه، فقط کمک میکنه که باهات آشنا شم ;)
اینجا می‌تونی بازی جدید راه بندازی یا به یه بازی ساخته شده اضافه بشی.
خوش بگذره D:
"""


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)
