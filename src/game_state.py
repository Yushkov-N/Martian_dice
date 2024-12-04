from src.dice import Dice
from src.player import Player


class GameState:

    def __init__(self, players: list[Player], current_player: int = 0, current_round=1,
                 dice: list = [Dice()], chosen_dice: list = list()):
        self.players: list[Player] = players
        self.end_play_players = list()
        self.current_player_index: int = current_player
        self.remaining_dice = dice * 13
        self.chosen_dice = chosen_dice
        self.current_round = current_round
        self.last_round = False
        self.several_winner = False

    def __repr__(self):
        if not self.end_play_players:
            return f"""
                [ Game_state ]:
                    "current_player_index": {self.current_player_index}, 
                    "players": {[p for p in self.players]}"""
        else:
            return f"""
               [ Game_state ]:
                   "current_player_index": {self.current_player_index}, 
                   "players": {[p for p in self.players]}, 
                   "end_game_players": {[p for p in self.end_play_players]}"""

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
        for i in range(len(self.remaining_dice)):
            self.remaining_dice[i] = self.remaining_dice[i].roll()
        while Dice.TANK in self.remaining_dice:
            for d in self.remaining_dice:
                if d == Dice.TANK:
                    self.chosen_dice.append(d)
                    self.remaining_dice.remove(d)

    def reroll_dice(self):
        self.roll_dice()

    def choose_dice(self, dice):
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

        tank = [d for d in dice_chs if d == Dice.TANK]
        ray = [d for d in dice_chs if d == Dice.RAY]
        ch = [d for d in dice_chs if d != Dice.RAY and d != Dice.TANK]
        rem = [d for d in dice_rem]

        print('\nTank dice(s) : ', end='')
        print(*tank)
        print('Chosen ray dice(s) : ', end='')
        print(*ray)
        print('Chosen dice(s) : ', end='')
        print(*ch)
        print('Remaining dice(s) : ', end='')
        print(*rem)
