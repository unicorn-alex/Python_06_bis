from ex3 import FlameFactory, TransformCreatureFactory, CreatureFactory
from ex4 import NormalStrategy, AggressiveStrategy, BattleStrategy
from typing import Any


def main() -> None:
    flame_factory = FlameFactory()
    transform_creature_factory = TransformCreatureFactory()
    normal_strategy = NormalStrategy()
    aggressive_strategy = AggressiveStrategy()

    battle([(flame_factory, normal_strategy),
            (transform_creature_factory, aggressive_strategy)])


def encounter(entity_1: Any, entity_2: Any,
              strategy_1: BattleStrategy, strategy_2: BattleStrategy,
              battle_num: int) -> None:
    print(f"Tournament {battle_num}")
    print(f"[ ({entity_1.__class__.__name__}+",
          f"{strategy_1.__class__.__name__})], ",
          f"({entity_2.__class__.__name__}+",
          f"{strategy_2.__class__.__name__}) ]", sep='')
    print("*** Tournament ***")
    print("2 opponents involved\n")

    print("* Battle *")
    print(entity_1.describe())
    print(" vs.")
    print(entity_2.describe())
    print(" now fight!")
    strategy_1.act(entity_1)
    strategy_2.act(entity_2)
    print()


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    battle_num = 0
    if len(opponents) < 2:
        return
    for i in range(len(opponents)):
        first = opponents[i]
        for j in range(len(opponents) - i - 1):
            second = opponents[(len(opponents) - i - 1):][j]
            base_opponent_1 = first[0].create_base()
            base_opponent_2 = second[0].create_base()
            evolved_opponent_1 = first[0].create_evolved()
            evolved_opponent_2 = second[0].create_evolved()
            try:
                encounter(base_opponent_1, base_opponent_2,
                          first[1], second[1], battle_num)
                battle_num += 1
                encounter(evolved_opponent_1, base_opponent_2,
                          first[1], second[1], battle_num)
                battle_num += 1
                encounter(base_opponent_1, evolved_opponent_2,
                          first[1], second[1], battle_num)
                battle_num += 1
                encounter(evolved_opponent_1, evolved_opponent_2,
                          first[1], second[1], battle_num)
            except AttributeError:
                print("Battle error, aborting tournament:",
                      "Some creature uses wrong strategy")


if __name__ == "__main__":
    main()
