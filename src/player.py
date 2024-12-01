from src.dice import Dice


class Player:

    def __init__(self, name: str, score:int = 0):
        self.name = name
        self.score = score

    def __repr__(self):
        return f'{self.name}: {self.score}'

    def save(self) -> dict:
        return {
            'name': self.name,
            'score': self.score
        }

    @classmethod
    def load(cls, data: dict):
        if 'score' not in data:
            data['score'] = 0
        return cls(name=data['name'], score=int(data['score']))

    def add_score(self,selected_dices: list = None):
        if selected_dices.count(Dice.RAY) >= selected_dices.count(Dice.TANK):
            for dice in selected_dices:
                if dice == Dice.HUMAN:
                    self.score += 1
                if dice == Dice.COW:
                    self.score += 1
                if dice == Dice.CHICKEN:
                    self.score += 1
            if (Dice.HUMAN in selected_dices and
                Dice.COW in selected_dices and
                Dice.CHICKEN in selected_dices):
                self.score += 3

    def scoree(self):
        return self.score