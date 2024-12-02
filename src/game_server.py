import inspect
import json


import pathlib as pb
import enum

from src.game_state import GameState
from src.player import Player
from src.dice import Dice
from src.player_interaction import PlayerInteraction
from src.player_interaction import Action
import src.player_interactions as all_player_types


class GamePhase(enum.StrEnum):
    CHOOSE = "Choose dice"
    ROLL = "Roll dices"
    REROLL = "Reroll dice(s)"
    DECLARE_WINNER = "Declare a winner"
    GAME_MOVE_END = "Game_move_end"
    NEXT_ROUND = "Round"
    LAST_ROUND = "Last_round"
    GAME_END = "Game_ended"
    UNDECIDED_WINNER = 'winner_selection'


class GameServer:

    SAVE_FILE = pb.Path(__file__).parent / 'gamedata1'

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types  # {player: PlayerInteractions}

    @classmethod
    def load_game(cls, filename: str | pb.Path):
        with open(filename, 'r') as f:
            data = json.load(f)
            game_state = GameState.load(data)
            print(game_state)
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player.name] = kind
            return GameServer(player_types=player_types, game_state=game_state)

    def save(self, filename: str | pb.Path):
        data = self.save_to_dict()
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()

        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name)
            player_types[player.name] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):

        players: list[Player] = [Player(name=name) for name in player_types.keys()]

        game_state = GameState(players=players)
        print(game_state)

        res = cls(player_types, game_state)
        return res

    def run(self):
        current_phase = GamePhase.ROLL
        while current_phase != GamePhase.GAME_END:
            phases = {
                GamePhase.ROLL: self.roll_dice_phase,
                GamePhase.CHOOSE: self.chose_dice_phase,
                GamePhase.REROLL: self.reroll_dice_phase,
                GamePhase.GAME_MOVE_END: self.end_game_move_phase,
                GamePhase.NEXT_ROUND: self.next_round_phase,
                GamePhase.LAST_ROUND: self.last_round_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase,
                GamePhase.UNDECIDED_WINNER: self.decide_winner_phase,
                GamePhase.GAME_END: self.end_game_phase
            }
            if current_phase == GamePhase.NEXT_ROUND and not self.game_state.last_round:
                print('________', current_phase, self.game_state.current_round, '________')

            if current_phase != GamePhase.NEXT_ROUND:
                print('\n[', current_phase, 'phase ]')
            current_phase = phases[current_phase]()

    def roll_dice_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        player_type = self.player_types[current_player.name]

        print(f'current player: {current_player.name}')

        match player_type.choose_roll():

            case Action.ROLL:
                player_type.inform_dice_is_roll(current_player)
                self.game_state.roll_dice()
                self.game_state.draw_dice(self.game_state.remaining_dice, self.game_state.chosen_dice)
                return GamePhase.CHOOSE

            case _:
                return GamePhase.ROLL

    def reroll_dice_phase(self):

        if not self.game_state.several_winner:
            self.game_state.draw_dice(self.game_state.remaining_dice, self.game_state.chosen_dice)
        current_player = self.game_state.current_player()
        player_type = self.player_types[current_player.name]

        if self.game_state.remaining_dice:
            match player_type.choose_continue():
                case Action.REROLL:

                    player_type.inform_dice_is_reroll(current_player)
                    self.game_state.reroll_dice()
                    self.game_state.draw_dice(self.game_state.remaining_dice, self.game_state.chosen_dice)

                    if self.game_state.several_winner:
                        for _ in range(self.game_state.remaining_dice.count(Dice.RAY)):
                            current_player.score += 1
                        if self.game_state.current_player_index != len(self.game_state.players)-1:
                            return GamePhase.GAME_MOVE_END
                        else:
                            return GamePhase.DECLARE_WINNER

                    for dice in self.game_state.remaining_dice:
                        if dice not in self.game_state.chosen_dice or dice == Dice.RAY:
                            return GamePhase.CHOOSE
                    return GamePhase.GAME_MOVE_END

                case Action.END_GAME_MOVE:
                    player_type.inform_end_game_move(current_player)
                    return GamePhase.GAME_MOVE_END
                case _:
                    return GamePhase.REROLL
        else:
            return GamePhase.GAME_MOVE_END

    def chose_dice_phase(self):
        current_player = self.game_state.current_player()
        player_type = self.player_types[current_player.name]

        match player_type.choose_dices(self.game_state.remaining_dice, self.game_state.chosen_dice):

            case Action.CHOOSE_RAY:
                player_type.inform_player_choose_ray(current_player)
                for _ in range(self.game_state.remaining_dice.count(Dice.RAY)):
                    self.game_state.choose_dice(Dice.RAY)
                if not self.game_state.remaining_dice:
                    return GamePhase.GAME_MOVE_END
                return GamePhase.REROLL

            case Action.CHOOSE_HUMAN:
                player_type.inform_player_choose_human(current_player)
                for _ in range(self.game_state.remaining_dice.count(Dice.HUMAN)):
                    self.game_state.choose_dice(Dice.HUMAN)
                if not self.game_state.remaining_dice:
                    return GamePhase.GAME_MOVE_END
                return GamePhase.REROLL

            case Action.CHOOSE_COW:
                player_type.inform_player_choose_cow(current_player)
                for _ in range(self.game_state.remaining_dice.count(Dice.COW)):
                    self.game_state.choose_dice(Dice.COW)
                if not self.game_state.remaining_dice:
                    return GamePhase.GAME_MOVE_END
                return GamePhase.REROLL

            case Action.CHOOSE_CHICKEN:
                player_type.inform_player_choose_chicken(current_player)
                for _ in range(self.game_state.remaining_dice.count(Dice.CHICKEN)):
                    self.game_state.choose_dice(Dice.CHICKEN)
                if not self.game_state.remaining_dice:
                    return GamePhase.GAME_MOVE_END
                return GamePhase.REROLL

            case _:
                return GamePhase.CHOOSE

    def end_game_move_phase(self):

        self.game_state.add_score()
        self.game_state.return_dice()
        print(self.game_state)

        if self.game_state.several_winner:
            if self.game_state.current_player_index != len(self.game_state.players)-1:
                self.game_state.next_player()
                return GamePhase.REROLL

        if self.game_state.players[self.game_state.current_player_index].score >= 25:
            if self.game_state.current_player_index == len(self.game_state.players)-1:
                return GamePhase.DECLARE_WINNER
            else:
                self.game_state.return_dice()
                return GamePhase.LAST_ROUND
        else:
            self.game_state.next_player()

            if self.game_state.current_player_index == 0:

                self.game_state.return_dice()
                return GamePhase.NEXT_ROUND

            self.game_state.return_dice()
            return GamePhase.ROLL

    def next_round_phase(self):
        if not self.game_state.last_round:
            self.game_state.current_round += 1
            return GamePhase.ROLL
        else:
            return GamePhase.DECLARE_WINNER

    def last_round_phase(self):
        self.game_state.last_round = True
        if self.game_state.current_player_index == 0:
            self.game_state.next_player()
            return GamePhase.ROLL
        else:
            return GamePhase.DECLARE_WINNER

    def declare_winner_phase(self) -> GamePhase:

        score = self.game_state.score()
        all_score = [val for val in score.values()]
        max_score = max(all_score)

        if all_score.count(max_score) >= 2:

            for p in self.game_state.players:
                if p.score != max_score:
                    self.game_state.end_play_players.append(p)
            for p in self.game_state.end_play_players:
                if p in self.game_state.players:
                    self.game_state.players.remove(p)

            self.game_state.several_winner = True
            self.game_state.last_round = False

            if self.game_state.players:
                return GamePhase.UNDECIDED_WINNER

        else:
            while self.game_state.players:
                self.game_state.end_play_players.append(self.game_state.players.pop())

            # for p in self.game_state.players:
            #     self.game_state.end_play_players.append(p)
            # for p in self.game_state.end_play_players:
            #     self.game_state.players.remove(p)
            #
            # if self.game_state.several_winner:
            #     if self.game_state.current_player_index == len(self.game_state.players)-1:
            #         for _ in range(len(self.game_state.players)):
            #             self.game_state.end_play_players.append(self.game_state.players.pop())

        score = self.game_state.score()

        player = max(score, key=lambda k: score[k])
        print(' Score:')
        for key in score:
            print(f"""      {key}: {score[key]} points""")
        print(' Winner:')
        print(f"""      {player}: {score[player]} points""")
        return GamePhase.GAME_END

    def decide_winner_phase(self):
        self.game_state.current_player_index = 0
        self.game_state.remaining_dice.clear()
        for _ in range(6):
            self.game_state.remaining_dice.append(Dice.RAY)
        return GamePhase.REROLL

    def end_game_phase(self):
        return GamePhase.GAME_END

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("How many players? - "))
                if 2 <= player_count <= 100:
                    return player_count
            except ValueError:
                pass
            print("Please input a number between 2 and 100")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        """Возвращает имя и тип игрока."""

        """Разрешенные типы игроков из PlayerInteraction."""
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("How to call a player? - ")
            if name.isalpha():
                break
            print("Name must be a single word, alphabetic characters only")

        while True:
            try:
                kind = input(
                    f"What kind of player is it ({player_types_as_str})? - ")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f"Allowed player types are: {player_types_as_str}")
        return name, kind


def __main__():
    load_from_file = True
    if load_from_file:
        server = GameServer.load_game(GameServer.SAVE_FILE)
    else:
        server = GameServer.new_game(GameServer.get_players())
        server.save(GameServer.SAVE_FILE)
    server.run()


if __name__ == "__main__":
    __main__()
