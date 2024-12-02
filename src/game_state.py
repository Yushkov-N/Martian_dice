from src.dice import Dice
from src.player import Player


class GameState:

    def __init__(self, players: list[Player], current_player: int = 0, current_round=1,
                 remaining_dice: list = [Dice.VALUES[0]] * 13, chosen_dice: list = list()):
        self.players: list[Player] = players
        self.end_play_players = list()
        self.current_player_index: int = current_player
        self.remaining_dice = remaining_dice
        self.chosen_dice = chosen_dice
        self.current_round = current_round
        self.last_round = False
        self.several_winner = False

    def __repr__(self):
        return f"""
            [ Game_state ]:
                "current_player_index": {self.current_player_index}, 
                "players": {[p for p in self.players]}"""

    def __eq__(self, other):
        return self.players == other.players and self.current_player_index == other.current_player_index

    def save(self) -> dict:
        return {
            "current_player_index": self.current_player_index,
            "players": [p.save() for p in self.players]
        }

    @classmethod
    def load(cls, data: dict):
        players = [Player.load(d) for d in data['players']]
        return cls(
            players=players,
            current_player=int(data['current_player_index']))

    def current_player(self) -> Player:
        try:
            return self.players[self.current_player_index]
        except:
            self.current_player_index = 0
            return self.players[self.current_player_index]

    def next_player(self):
        n = len(self.players)
        self.current_player_index = (self.current_player_index + 1) % n

    def roll_dice(self):
        self.remaining_dice = Dice.roll(len(self.remaining_dice))
        for _ in range(self.remaining_dice.count(Dice.TANK)):
            self.chosen_dice.append(Dice.TANK)
            self.remaining_dice.remove(Dice.TANK)

    def reroll_dice(self):
        self.remaining_dice = Dice.roll(len(self.remaining_dice))
        for _ in range(self.remaining_dice.count(Dice.TANK)):
            self.chosen_dice.append(Dice.TANK)
            self.remaining_dice.remove(Dice.TANK)

    def choose_dice(self, dice: Dice):
        self.chosen_dice.append(dice)
        self.remaining_dice.remove(dice)

    def add_score(self):
        self.players[self.current_player_index].add_score(self.chosen_dice)

    def return_dice(self):
        for el in self.chosen_dice:
            self.remaining_dice.append(el)
        self.chosen_dice.clear()

    def score(self):
        if self.players:
            return {p.name: p.player_score() for p in self.players}
        else:
            return {p.name: p.player_score() for p in self.end_play_players}

    @staticmethod
    def draw_dice(dice_rem: list, dice_chs: list = None):

        print('\nTank dice(s) : ', end='')
        for dice in dice_chs:
            if dice == Dice.TANK:
                print('|', dice, '|', sep='', end=' ')
        print(end='\n')

        print('Chosen ray dice(s) : ', end='')
        for dice in dice_chs:
            if dice == Dice.RAY:
                print('|', dice, '|', sep='', end=' ')
        print(end='\n')

        print('Chosen dice(s) : ', end='')
        for dice in dice_chs:
            if dice != Dice.TANK and dice != Dice.RAY:
                print('|', dice, '|', sep='', end=' ')
        print(end='\n')

        print('Remaining dice(s) : ', end='')
        for dice in dice_rem:
            print('|', dice, '|', sep='', end=' ')
        print(end='\n')
