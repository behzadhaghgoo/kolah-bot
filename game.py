# Assuming that there are an even number of players.
# Assuming that player ids are unique.

import numpy as np

class Team():
    def __init__(self, players):
        self.players = players
        self.score = 0

class Player():
    def __init__(self, identifier, turn_func, input_func):
        self.id = identifier
        self.team = None
        self.turn_func = turn_func
        self.input_func = input_func

class Game():
    def __init__(self):
        self.players = []
        self.teams = []
        self.words = set()
        self.remaining_words = self.words
        self.current_player_ind = 0

    def add_player(self, player_id):
        """
        Works both with a list or single input
        """
        if isinstance(player_id, list):
            player_ids = player_id
        else:
            player_ids = [player_id]

        for player_id in player_ids:
            if player_id not in self.players:
                self.players.append(Player(player_id))

    def add_words(self, words):
        """
        Works both with a list or a single input
        """
        if not isinstance(words, list):
            words = [words]
        for word in words:
            self.words.add(word)

        self.remaining_words = self.words

    def assign_teams(self):
        team_assignments = np.random.permutation(self.players).reshape((-1,2))
        # Reorder players
        self.players = team_assignments.T.reshape(-1)
        for team_assignment in team_assignments:
            curr_team = Team(team_assignment)
            self.teams.append(curr_team)
            print(team_assignment)
            team_assignment[0].team = curr_team
            team_assignment[1].team = curr_team

    def get_random_word(self):
        current_word = np.random.choice(list(self.words))
        return current_word

    def reset(self):
        self.remaining_words = self.words

    def round_result(self, success, word, player):
        """
        Success (bool)
        """
        if success:
            self.remaining_words.remove(word)
            self.players[self.current_player_ind].team.score += 1
