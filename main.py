import random
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
    return 2 if len(history) == 0 else history[-1][1]


def random_strategy(history):
    return random.randint(1, 2)


def tit_for_two_tat(history):
    if len(history) < 2:
        return 2
    if history[-1][1] == 1 and history[-2][1] == 1:
        return history[-1][1]
    return 2


# Coops first 10 rounds, defects afterwards if an opponent defected
def first_by_davis(history):
    if len(history) < 10:
        return 2
    if 2 in history[::][1]:
        return 1
    return 2


# Coops always - when opponent did a different move in the previous turn then the chance of cooperation is 2/7
def first_by_grofman(history):
    if len(history) == 0 or history[-1][0] == history[-1][1]:
        return 2
    return random.choices(population=[1, 2], weights=[5/7, 2/7])[0]


# Own strategy
def first_by_tomes(history):
    if len(history) % 2 == 0:
        return 2
    return 1


def print_result(p1: AxelrodPlayer, p2: AxelrodPlayer):
    print(f"{player_one.strategy.__name__} vs {player_two.strategy.__name__}")
    if p1.points > p2.points:
        print(f"The winner strategy is {p1.strategy.__name__} with {p1.points} points.\n")
    elif p1.points == p2.points:
        print(f"It's draw. Both {p1.strategy.__name__} and {p2.strategy.__name__} with {p1.points} points.\n")
    else:
        print(f"The winner strategy is {p2.strategy.__name__} with {p2.points} points.\n")


strategies = [always_defect,
              always_cooperate,
              tit_for_tat,
              random_strategy,
              tit_for_two_tat,
              first_by_davis,
              first_by_grofman,
              first_by_tomes]
stats = []

for index, strategy in enumerate(strategies):
    print("\n" + ("-" * 20))
    print(f"Game #{index + 1}")
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

        stats.append(player_one)
        stats.append(player_two)
        print_result(player_one, player_two)


strategy_statistics = {}
for strategy in strategies:
    strategy_statistics[strategy.__name__] = sum(stat.points for stat in stats if stat.strategy == strategy)

print("\n\n")
for strategy_name, strategy_points in strategy_statistics.items():
    print(f"STRATEGY {strategy_name} earned: {strategy_points}")
print(f"\nWinner strategy is '{max(strategy_statistics, key=strategy_statistics.get)}' "
      f"with {max(strategy_statistics.values())} points.\n")
