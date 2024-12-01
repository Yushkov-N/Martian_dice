from src.dice import Dice

from src.player_interaction import PlayerInteraction
from src.player_interaction import Action


class Human(PlayerInteraction):

    @classmethod
    def choose_roll(cls):
        while True:
            action = input('Choose action: ')
            match  action:
                case 'r':
                    cls.inform_dice_is_roll()
                    return Action.ROLL
                case _:
                     print("""   Please type:
        "r" for roll dice(s) """)

    @classmethod
    def choose_continue(cls):
        while True:
            action = input('Choose action: ')
            match action:
                case 're':
                    cls.inform_dice_is_reroll()
                    return Action.REROLL
                case 'e':
                    cls.inform_end_game_move()
                    return Action.END_GAME_MOVE
                case _:
                    print("""Please type: 
            "re" for reroll dice(s) 
            "e" for end game move""")

    @classmethod
    def choose_dices(cls, remaining_dice, chosen_dice):
        while True:
            action = input('Choose action: ')

            match action:
                case 'ray':
                    if Dice.RAY in remaining_dice:
                        # cls.inform_player_choose_ray()
                        return Action.CHOOSE_RAY
                    else:
                        print('Ray not in remaining dice')

                case 'cow':
                    if Dice.COW in remaining_dice:
                        if Dice.COW not in chosen_dice:
                            # cls.inform_player_choose_cow()
                            return Action.CHOOSE_COW
                        else:
                            print('Cow already in chosen dice')
                    else:
                        print('Cow not in remaining dice')

                case 'human':
                    if Dice.HUMAN in remaining_dice:
                        if Dice.HUMAN not in chosen_dice:
                            # cls.inform_player_choose_human()
                            return Action.CHOOSE_HUMAN
                        else:
                            print('Human already in chosen dice')
                    else:
                        print('Human not in remaining dice')

                case 'chick':
                    if Dice.CHICKEN in remaining_dice:
                        if Dice.CHICKEN not in chosen_dice:
                            # cls.inform_player_choose_chicken()
                            return Action.CHOOSE_CHICKEN
                        else:
                            print('Chicken already in chosen dice')
                    else:
                        print('Chicken not in remaining dice')

                case _:
                    print("""   Please type:
            "ray" to choose rays or 
            "human" to choose human or 
            "cow" to choose cow or 
            "chick" to choose chicken or """)
