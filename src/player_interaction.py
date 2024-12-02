from abc import ABC, abstractmethod

from src.dice import Dice
from src.player import Player
import enum


class Action(enum.StrEnum):

    CHOOSE_RAY = 'choose_ray'
    CHOOSE_TANK = 'choose_tank'
    CHOOSE_HUMAN = 'choose_human'
    CHOOSE_COW = 'choose_cow'
    CHOOSE_CHICKEN = 'choose_chicken'
    ROLL = 'roll'
    REROLL = 'reroll'
    END_GAME_MOVE = 'end game move'


class PlayerInteraction(ABC):

    @classmethod
    @abstractmethod
    def choose_action(cls) -> Dice:
        """
        Игрок выбирает отложить кубик или бросить кубик, или закончить ход
        """
        pass

    @classmethod
    def inform_player_choose_ray(cls, player: Player):
        """
        Сообщает, что игрок выбрал кубик(и).
        """
        print(f'\n{player.name}({cls.__name__}): choose ray')

    @classmethod
    def inform_player_choose_human(cls, player: Player):
        """
        Сообщает, что игрок выбрал кубик(и).
        """
        print(f'\n{player.name}({cls.__name__}): choose human')

    @classmethod
    def inform_player_choose_cow(cls, player: Player):
        """
        Сообщает, что игрок выбрал кубик(и).
        """
        print(f'\n{player.name}({cls.__name__}): choose cow')

    @classmethod
    def inform_player_choose_chicken(cls, player: Player):
        """
        Сообщает, что игрок выбрал кубик(и).
        """
        print(f'\n{player.name}({cls.__name__}): choose chicken')

    @classmethod
    def inform_dice_is_roll(cls, player: Player):
        """
        Сообщает, что игрок кинул кубики.
        """
        print(f'\n{player.name}({cls.__name__}): roll dice')

    @classmethod
    def inform_dice_is_reroll(cls, player: Player):
        """
        Сообщает, что игрок перекинул кубики.
        """
        print(f'\n{player.name}({cls.__name__}): reroll dice(s)')

    @classmethod
    def inform_end_game_move(cls, player: Player):
        """
        Сообщает, что игрок закончил игровой ход.
        """
        print(f'\n{player.name}({cls.__name__}): end game move')
