import unittest
from src.dice import Dice

class TestCase(unittest.TestCase):
    def test_init(self):
        dice = Dice()
        assert dice.side == 'ray'

    def test_rapr(self):
        dice = Dice('tank')
        assert dice.__repr__() == '|tank|'

    def test_eq(self):
        dice = Dice('tank')
        assert dice.__eq__('tank')

    def test_roll(self):
        dice = Dice('tank')
        roll_res = dice.roll()
        assert roll_res in Dice.VALUES

    def test_all_sides(self):
        dice = Dice()
        all_sides = dice.all_sides()
        assert all_sides == Dice.VALUES