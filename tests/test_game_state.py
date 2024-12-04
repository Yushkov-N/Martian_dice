import unittest
import copy
from src.game_state import GameState
from src.player import Player
from src.dice import Dice


class TestCase(unittest.TestCase):

    def test_init(self):
        p1 = Player('Rebecca')
        p2 = Player('Ballu')
        state = GameState([p1, p2])
        assert state.players == [p1, p2]
        assert state.end_play_players == []
        assert state.current_player_index == 0
        assert len(state.remaining_dice) == 13
        # assert state.chosen_dice == []
        assert state.current_round == 1
        assert state.last_round == False
        assert state.several_winner == False

    def test_repr(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        p3 = Player('Kit', 5)
        state = GameState([p1, p2])

        assert state.__repr__() == f"""
                [ Game_state ]:
                    "current_player_index": 0, 
                    "players": [Rebecca: 25, Ballu: 25]"""

        state.end_play_players = [p3]
        assert state.__repr__() == f"""
               [ Game_state ]:
                   "current_player_index": 0, 
                   "players": [Rebecca: 25, Ballu: 25], 
                   "end_game_players": [Kit: 5]"""

    def test_eq(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Rebecca', 25)
        p3 = Player('Ballu', 20)
        state1 = GameState([p1, p2])
        state2 = GameState([p1, p2])
        state3 = GameState([p1, p3])

        assert state1 == state2
        assert state2 != state3

    def test_save(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        state = GameState([p1, p2])
        state.current_player_index = 1
        data = state.save()

        assert data == {
            'current_player_index': 1,
            'players': [
                {
                    'name': 'Rebecca',
                    'score': 25
                },
                {
                    'name': 'Ballu',
                    'score': 25
                }
            ]
        }

    def test_load(self):
        data = {
            'current_player_index': 1,
            'players': [
                {
                    'name': 'Rebecca',
                    'score': 25
                },
                {
                    'name': 'Ballu',
                    'score': 24
                }
            ]
        }
        state = GameState.load(data)
        assert state.current_player_index == 1
        assert state.players[0].name == 'Rebecca' and state.players[0].score == 25
        assert state.players[1].name == 'Ballu' and state.players[1].score == 24

    def test_current_player(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        state = GameState([p1, p2])
        state.current_player_index = 1

        cur_pl = state.current_player()
        assert cur_pl == p2

        state.current_player_index = 10
        cur_pl = state.current_player()
        assert cur_pl == p1

    def test_next_player(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        state = GameState([p1, p2])

        state.current_player_index = 0
        assert state.current_player() == p1

        state.next_player()
        assert state.current_player() == p2

    def test_roll_dice(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        state = GameState([p1, p2])

        dice1 = copy.deepcopy(state.remaining_dice)
        state.roll_dice()
        dice2 = state.remaining_dice
        assert dice1 != dice2

    def test_choose_dice(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 25)
        state = GameState([p1, p2])

        dice1 = Dice(Dice.HUMAN)
        dice2 = Dice(Dice.COW)
        dice3 = Dice(Dice.RAY)
        state.remaining_dice = [dice1, dice2, dice3]

        state.choose_dice(dice1)
        assert state.chosen_dice == [dice1]

        state.choose_dice(dice2)
        assert state.chosen_dice == [dice1, dice2]

    def test_add_score(self):
        p1 = Player('Rebecca', 0)
        p2 = Player('Ballu', 0)
        state = GameState([p1, p2])
        state.current_player_index = 0
        state.chosen_dice = [Dice(Dice.COW), Dice(Dice.HUMAN), Dice(Dice.CHICKEN),
                             Dice(Dice.RAY), Dice(Dice.TANK)]

        state.add_score()
        assert state.current_player().score == 6

        state.current_player_index = 1
        state.chosen_dice = [Dice(Dice.COW), Dice(Dice.HUMAN), Dice(Dice.CHICKEN),
                             Dice(Dice.RAY), Dice(Dice.TANK), Dice(Dice.TANK)]

        state.add_score()
        assert state.current_player().score == 0

        state.chosen_dice = [Dice(Dice.COW), Dice(Dice.HUMAN)]
        state.add_score()
        assert state.current_player().score == 2

    def test_return_dice(self):
        p1 = Player('Rebecca', 0)
        p2 = Player('Ballu', 0)
        state = GameState([p1, p2])
        state.chosen_dice = copy.deepcopy(state.remaining_dice)

        state.remaining_dice.clear()
        assert state.remaining_dice == []

        state.return_dice()
        assert state.remaining_dice != []
        assert state.chosen_dice == []

    def test_score(self):
        p1 = Player('Rebecca', 25)
        p2 = Player('Ballu', 12)
        state = GameState([p1, p2])

        score = state.score()
        assert score == {'Rebecca': 25, 'Ballu': 12}

        state.end_play_players.append(p2)
        state.players.remove(p2)
        score = state.score()
        assert score == {'Rebecca': 25}

        state.end_play_players.append(p1)
        state.players.remove(p1)
        score = state.score()
        assert score == {'Rebecca': 25, 'Ballu': 12}
