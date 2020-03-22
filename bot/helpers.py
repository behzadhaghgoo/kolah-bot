from .models.game import Game
from .models.player import Player
import telegram 
joining_status = """
**Active Players:**
%s
"""

def update_message(telegram_bot, player, text, keyboard = None):
    print("salam")
    # [[telegram.InlineKeyboardButton("Previous Player", callback_data='1'), telegram.InlineKeyboardButton("Next Player", callback_data='2')],
                                            #    [telegram.InlineKeyboardButton("Correct", callback_data='3')]]
    in_markup = None
    if keyboard:
        in_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton(element, callback_data=element) for element in key_array] for key_array in keyboard])
    print("keyboard:", in_markup)
    if player.status_message_id is None:
        print("creating new message for", player.name)
        message = telegram_bot.send_message(chat_id=player.chat_id, text=text, parse_mode="Markdown", reply_markup=in_markup)
        player.status_message_id = message.message_id
        player.save()
    else:
        print("editing message for", player.name)
        telegram_bot.edit_message_text(text, chat_id=player.chat_id, message_id=player.status_message_id, parse_mode="Markdown", reply_markup=in_markup)
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

        reply_message = """
        The game is created, add players by sharing this message with them. \n\n[Join](http://t.me/kolah_game_bot?start=%s)
        """

        #  % game_id

        for player in game.players:
            keyboard = None
            if player == game.creator_id:
                keyboard = [['Start Getting Words']]
            update_message(telegram_bot, players_dict[player],(reply_message % game.id) + "" + (joining_status % active_players_text), keyboard)

    if game.status == "Team Assignment":
        teams_str = ""
        for i, team in enumerate(game.teams):
            teams_str += "team {}: {} - {} : {} points \n".format(i, players_dict[team.players[0]].name, players_dict[team.players[1]].name, team.score)
        for player in players:
            keyboard = None
            if player.chat_id == game.creator_id:
                keyboard = []
                if game.active_round == 0:
                    keyboard.append(['Assign Teams'])
                if game.active_round < len(game.rounds_timeout):
                    keyboard.append(['Start Round'])
                else: 
                    keyboard.append(['Finish Game'])
            update_message(telegram_bot, player, teams_str, keyboard)
            
    if game.status == "Getting Words":
        message = """کلمه وارد کن گل من
         {} کلمه وارد شده تا الان""".format(len(game.words))
        for player in players:
            keyboard = None
            if player.chat_id == game.creator_id:
                keyboard = [['Assign Teams']]
            update_message(telegram_bot, player, message, keyboard)

    if game.status == "Waiting":

        curr_player_keyboard = [['Start Explaining']]
        admin_keyboard = [['Prev Player','Next Player']]
        
        message = """منتطرِ: {}""".format(players_dict[game.players[game.active_player_index]].name)

        for ind, player in enumerate(game.players):
            if ind != (game.active_player_index % len(game.players)):
                if player == game.creator_id:
                    update_message(telegram_bot, players_dict[player], message, admin_keyboard)
                else:
                    update_message(telegram_bot, players_dict[player], message)
            else: 
                special_message = """\n\n **نوبت توئه!**"""
                if player == game.creator_id:
                    update_message(telegram_bot, players_dict[player], special_message, curr_player_keyboard + admin_keyboard)
                else:
                    update_message(telegram_bot, players_dict[player], special_message, curr_player_keyboard)



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
        print("message", message)
        curr_player_keyboard = [['Correct']]
        admin_keyboard = [['Prev Player','Next Player']]
        for ind, player in enumerate(game.players):
            if ind != (game.active_player_index % len(game.players)):
                if player == game.creator_id:
                    update_message(telegram_bot, players_dict[player], message, admin_keyboard)
                else:
                    update_message(telegram_bot, players_dict[player], message)
            else: 
                special_message = """\n\n **کلمه: {}**""".format(game.current_word)
                if player == game.creator_id:
                    update_message(telegram_bot, players_dict[player], message + special_message, curr_player_keyboard + admin_keyboard)
                else:
                    update_message(telegram_bot, players_dict[player], message + special_message, curr_player_keyboard)

    if game.status == "Finished":
        for player in players:
            update_message(telegram_bot, player, "be payan amad in daftar, hekayat hamchenan baghist", [['New Game']])
        pass
    