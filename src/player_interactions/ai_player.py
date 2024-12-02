from abc import ABC

from src.dice import Dice
from src.player_interaction import PlayerInteraction
import random

from src.player_interaction import Action


class Bot(PlayerInteraction, ABC):
    actions = [act for act in Action]
    action_continue = [Action.REROLL, Action.REROLL, Action.REROLL, Action.REROLL, Action.REROLL, Action.END_GAME_MOVE]
    action_chosen_dice = [Action.CHOOSE_RAY, Action.CHOOSE_COW, Action.CHOOSE_HUMAN, Action.CHOOSE_CHICKEN]

    @classmethod
    def choose_roll(cls):
        return Action.ROLL

    @classmethod
    def choose_continue(cls):
        action = random.choice(cls.action_continue)
        return action

    @classmethod
    def choose_dices(cls, remaining_dice, chosen_dice):
        while True:

            action = random.choice(cls.action_chosen_dice)

            if action == Action.CHOOSE_RAY and Dice.RAY in remaining_dice:
                return action

            if (action == Action.CHOOSE_COW and
                    Dice.COW in remaining_dice and
                    Dice.COW not in chosen_dice):
                return action

            if (action == Action.CHOOSE_HUMAN and
                    Dice.HUMAN in remaining_dice and
                    Dice.HUMAN not in chosen_dice):
                return action

            if (action == Action.CHOOSE_CHICKEN and
                    Dice.CHICKEN in remaining_dice and
                    Dice.CHICKEN not in chosen_dice):
                return action
