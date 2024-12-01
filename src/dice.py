import random


class Dice:

    TANK: str = 'tank'
    RAY: str = 'ray'
    HUMAN: str = 'human'
    COW: str = 'cow'
    CHICKEN: str = 'chicken'

    VALUES = [TANK, RAY, RAY, HUMAN, COW, CHICKEN]

    def __init__(self, values=VALUES[0]):
        self.side = values

    def __repr__(self):
        return f'{self.side}'

    def __eq__(self, other_side):
        return self.side == other_side

    def save(self):
        return self.side

    @classmethod
    def load(cls, side: str):
        return cls(side)

    @classmethod
    def all_sides(cls, sides: None | list[str] = None):
        if sides is None:
            sides = cls.VALUES
        sides = [cls(side) for side in sides]
        return sides

    @classmethod
    def roll(cls, count: int = 0):
        sides = cls.VALUES
        roll_result = [cls(random.choice(sides)) for _ in range(count)]
        return roll_result
