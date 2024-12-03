import unittest
from src.game_state import GameState
from src.player import Player
class TestCase(unittest.TestCase):

    def test_init(self):
        p1 = Player('Rebecca')
        p2 = Player('Ballu')
        state = GameState([p1,p2])
        assert state.players == [p1, p2]
        assert state.end_play_players == []
        assert state.current_player_index == 0
        assert len(state.remaining_dice) == 13
        assert state.chosen_dice == []
        assert state.current_round == 1
        assert state.last_round == False
        assert state.several_winner == False

    def test_repr(self):
        pass