from .models.game import Game
from .models.player import Player
import telegram 
joining_status = """
بازیکنان فعال:
%s
"""

def update_message(telegram_bot, player, text):
    print("salam")
    menu_keyboard = [['/prev_player', '/next_player'], ['/correct']]
    kb_markup = telegram.ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    in_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Previous Player", callback_data='1'), telegram.InlineKeyboardButton("Next Player", callback_data='2')],
                                               [telegram.InlineKeyboardButton("Correct", callback_data='3')]])
    if player.status_message_id is None:
        print("creating new message")
        message = telegram_bot.send_message(chat_id=player.chat_id, text=text, parse_mode="Markdown") #, reply_markup=kb_markup)
        player.status_message_id = message.message_id
        player.save()
    else:
        print("editing message")
        telegram_bot.edit_message_text(text, chat_id=player.chat_id, message_id=player.status_message_id) #, reply_markup=kb_markup)
        # message = telegram_bot.send_message(chat_id=player.chat_id, text=text, reply_markup=kb_markup)
        print("dorood")


def update_statuses(telegram_bot, game):
    print("game.status = {}".format(game.status))
    game.reload()
    players = Player.objects(chat_id__in=game.players)
    players_dict = dict()
    for player in players:
        players_dict[player.chat_id] = player

    active_players_text = "\n".join(["%d.%s" % (index + 1, player.name) for index, player in enumerate(players)])
    if game.status == "Joining":
        for player in players:
            update_message(telegram_bot, player, joining_status % active_players_text)

    if game.status == "Team Assignment":
        teams_str = ""
        for i, team in enumerate(game.teams):
            teams_str += "team {}: {} - {} \n".format(i, players_dict[team.players[0]].name, players_dict[team.players[1]].name)
        for player in players:
            update_message(telegram_bot, player, teams_str)
            
    if game.status == "Getting Words":
        message = """کلمه وارد کن گل من
         {} کلمه وارد شده تا الان""".format(len(game.words))
        for player in players:
            update_message(telegram_bot, player, message)

    if game.status == "Playing":
        print("hame teshne labim", game.active_player_index)
        print(players_dict[game.players[game.active_player_index]].name)
        print(players_dict[game.players[(game.active_player_index + len(game.players)//2) % len(game.players)]].name)
        message = """توضیح‌دهنده: {}
                     حدس‌زننده: {}
                    امتیاز‌ این تیم: {}                     
                  """.format(players_dict[game.players[game.active_player_index]].name, 
                             players_dict[game.players[(game.active_player_index + len(game.players)//2) % len(game.players)]].name,
                             game.teams[game.active_player_index % (len(game.players)//2)].score)
        print("hame teshne labim", message)
        for ind, player in enumerate(game.players):
            if ind != (game.active_player_index % len(game.players)):
                update_message(telegram_bot, players_dict[player], message)
            else: 
                special_message = """\n\n **کلمه: {}**""".format(game.current_word)
                update_message(telegram_bot, players_dict[player], message + special_message)

    if game.status == "Finished":
        
        for player in players:
            update_message(telegram_bot, player, "be payan amad in daftar, hekayat hamchenan baghist")
        pass
    