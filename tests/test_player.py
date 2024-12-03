import unittest
from src.player import Player

class TestCase(unittest.TestCase):
    def test_init(self):
        player1 = Player('Ballu')
        player2 = Player('Rebecca', 10)
        assert player1.name == 'Ballu'
        assert player1.score == 0
        assert player2.name == 'Rebecca'
        assert player2.score == 10

    def test_repr(self):
        player = Player('Rebecca', 10)
        assert player.__repr__() == 'Rebecca: 10'

    def test_save(self):
        player = Player('Rebecca', 10)
        pl_save = player.save()
        assert pl_save == {'name':'Rebecca','score':10}

    def test_load(self):
        data1 = {'name':'Rebecca','score':10}
        player1 = Player.load(data1)
        data2 = {'name':'Ballu'}
        player2 = Player.load(data2)
        assert player1.name == 'Rebecca'
        assert player1.score == 10
        assert player2.name == 'Ballu'
        assert player2.score == 0

    def test_add_score(self,):
        player = Player('Rebecca', 0)
        selected_dices = ['ray', 'tank', 'cow']
        player.add_score(selected_dices)
        assert player.score == 1

        player = Player('Rebecca', 0)
        selected_dices = ['ray', 'tank', 'tank', 'cow']
        player.add_score(selected_dices)
        assert player.score == 0

        player = Player('Rebecca', 0)
        selected_dices = ['ray', 'tank', 'chicken', 'cow', 'human']
        player.add_score(selected_dices)
        assert player.score == 6

    def test_player_score(self):
        player = Player('Rebecca', 10)
        assert player.player_score() == 10