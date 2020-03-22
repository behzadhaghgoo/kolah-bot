from .start import start
from .create import create
from .assign_teams import assign_teams
from .start_getting_words import start_getting_words
from .add_word import add_word
from .get_status import get_status
from .start_game import start_game
from .correct import correct
from .next_player import next_player, prev_player
from .finish import finish

def button(update, context):
    print("button pressed")
    data = update.callback_query.data
    print("data", data)
    if data == 'Start Getting Words':
        start_getting_words(update, context)
    elif data == 'Start Game':
        start_game(update, context)
    elif data == 'Assign Teams':
        assign_teams(update, context)
    elif data == 'correct':
        correct(update, context)
    elif data == 'Next Player':
        next_player(update, context)
    elif data == 'Prev Player':
        prev_player(update, context)
    elif data == 'New Game':
        create(update, context)

    return

