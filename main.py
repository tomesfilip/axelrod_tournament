import random
import sys
from AxelrodPlayer import AxelrodPlayer


# Strategy:
# defect == 1
# cooperate == 2

point_rules: dict = {
        (1, 1): 1,  # both defect
        (1, 2): 5,  # win
        (2, 1): 0,  # lost
        (2, 2): 3   # both cooperated
    }


def always_defect(history):
    return 1


def always_cooperate(history):
    return 2


def tit_for_tat(history: list):
    if len(history) == 0:
        return 2
    return history[-1][1]


def random_strategy(history):
    return random.randint(1, 2)


strategies = [always_defect, always_cooperate, tit_for_tat, random_strategy]

for index, strategy in enumerate(strategies):
    for strategy_index, player_two_strategy in enumerate(strategies[index:len(strategies)]):
        moves_history = []
        player_one = AxelrodPlayer(strategy=strategy, points=0)
        player_two = AxelrodPlayer(strategy=player_two_strategy, points=0)

        for i in range(200):
            player_one_choice = player_one.strategy(moves_history)
            player_two_choice = player_two.strategy([i[::-1] for i in moves_history[::1]])

            moves_history.append([player_one_choice, player_two_choice])

            player_one.points += point_rules.get((player_one_choice, player_two_choice))
            player_two.points += point_rules.get((player_two_choice, player_one_choice))

        print(f"#{strategy_index + 1} Game - {player_one.strategy} vs {player_two.strategy}")
        print("Points (player 1): ", player_one.points)
        print("Points (player 2): ", player_two.points)



