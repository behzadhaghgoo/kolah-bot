# Assuming that there are an even number of players.
# Assuming that player ids are unique.

import numpy as np
import mongoengine


class Team(mongoengine.EmbeddedDocument):
    players = mongoengine.ListField(mongoengine.IntField())
    score = mongoengine.IntField(default=0)


class Game(mongoengine.Document):
    players = mongoengine.ListField(mongoengine.IntField(), default=list)
    teams = mongoengine.EmbeddedDocumentListField(Team, default=list)
    words = mongoengine.ListField(mongoengine.StringField(), default=list)
    remaining_words = mongoengine.ListField(mongoengine.StringField(), default=list)
    creator_id = mongoengine.IntField(required=True)
    status = mongoengine.StringField(default="Joining")


class GameManager:

    @staticmethod
    def get_game(game_id):
        games = Game.objects(id=game_id)
        if len(games) == 0:
            return None
        return games[0]

    @staticmethod
    def create_game(creator_id):
        games = Game.objects(creator_id=creator_id, status__ne="Finished")
        if len(games):
            return str(games[0].id)
        game = Game(creator_id=creator_id)
        game.save()
        return str(game.id)

    @staticmethod
    def add_player(game, player_id):
        """
        Works both with a list or single input
        """
        if isinstance(game, str):
            game = GameManager.get_game(game)
            if game is None:
                return False, None
        if isinstance(player_id, list):
            player_ids = player_id
        else:
            player_ids = [player_id]

        for player_id in player_ids:
            game.update(add_to_set__players=player_id)
        return True, game

    @staticmethod
    def add_words(game, words):
        """
        Works both with a list or a single input
        """
        print("add words")
        if isinstance(game, str):
            game = GameManager.get_game(game)
            if game is None:
                return None
        print("dorood")
        if not isinstance(words, list):
            words = [words]
        print("vay")
        for word in words:
            game.update(add_to_set__words=word)
        print("e")
        return game


    # TODO: fix odd players edge-case.
    @staticmethod
    def assign_teams(game):
        print("assign_teams started", game.__dict__)
        if isinstance(game, str):
            game = GameManager.get_game(game)
            if game is None:
                return None
        team_assignments = np.random.permutation(game.players).reshape((-1, 2))
        # Reorder players
        game.update(set__players = team_assignments.T.reshape(-1))
        game.update(set__teams=list())
        for team_assignment in team_assignments:
            curr_team = Team(players=team_assignment)
            game.update(push__teams=curr_team)
            print(curr_team.__dict__, curr_team.players)
        return game

    @staticmethod
    def get_random_word(game):
        current_word = np.random.choice(list(game.remaining_words))
        return current_word

    @staticmethod
    def reset(game):
        game.remaining_words = game.words
        game.save()

    @staticmethod
    def round_result(game, success, word, player):
        """
        Success (bool)
        """
        if success:
            game.remaining_words.remove(word)
            for index in range(len(game.teams)):
                if player in game.teams[index].players:
                    game.teams[index].score += 1
            game.save()

