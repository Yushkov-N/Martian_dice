from abc import ABC

from src.dice import Dice
from src.player_interaction import PlayerInteraction

from src.player_interaction import Action


class Bot_Perfect(PlayerInteraction, ABC):
    actions = [act for act in Action]
    action_continue = [Action.REROLL, Action.REROLL, Action.REROLL, Action.REROLL, Action.REROLL, Action.END_GAME_MOVE]
    action_chosen_dice = [Action.CHOOSE_RAY, Action.CHOOSE_COW, Action.CHOOSE_HUMAN, Action.CHOOSE_CHICKEN]

    @classmethod
    def choose_roll(cls):
        return Action.ROLL

    @classmethod
    def choose_continue(cls, remaining_dice: list = None, chosen_dice: list = None):

        supposed_score = 0
        for d in chosen_dice:
            if d != Dice.RAY and d != Dice.TANK:
                supposed_score += 1
        if (Dice.COW in chosen_dice) and (Dice.CHICKEN in chosen_dice) and (Dice.HUMAN in chosen_dice):
            print('\n'*10)
            supposed_score += 3
        if supposed_score >= 4:
            return Action.END_GAME_MOVE

        action = Action.REROLL
        return action

    @classmethod
    def choose_dices(cls, remaining_dice: list, chosen_dice: list):
        # value = len(chosen_dice)
        value = 0

        if chosen_dice.count(Dice.RAY) < chosen_dice.count(Dice.TANK) and Dice.RAY in remaining_dice:
            return Action.CHOOSE_RAY

        if 4-value <= remaining_dice.count(Dice.RAY) <= 7-value:
            return Action.CHOOSE_RAY

        else:
            action = [Action.CHOOSE_COW, Action.CHOOSE_CHICKEN, Action.CHOOSE_HUMAN]

            count_cow = (remaining_dice.count(Dice.COW))
            count_chicken = (remaining_dice.count(Dice.CHICKEN))
            count_human = (remaining_dice.count(Dice.HUMAN))

            counts_list = []
            counts = tuple()

            if Dice.COW not in chosen_dice:
                counts_list.append(count_cow)
            else:
                counts_list.append(999)
            if Dice.CHICKEN not in chosen_dice:
                counts_list.append(count_chicken)
            else:
                counts_list.append(999)
            if Dice.HUMAN not in chosen_dice:
                counts_list.append(count_human)
            else:
                counts_list.append(999)

            for item in counts_list:
                if item != 0:
                    counts += item,
                else:
                    counts += 999,

            min_val = min(counts)
            if min_val == 999:
                return Action.CHOOSE_RAY

            action_index = counts_list.index(min_val)
            return action[action_index]

