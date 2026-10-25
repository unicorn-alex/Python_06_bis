from ex3 import FlameFactory, TransformCreatureFactory, CreatureFactory
from ex4 import NormalStrategy, AggressiveStrategy, BattleStrategy

def main():
    flame_factory = FlameFactory()
    transform_creature_factory = TransformCreatureFactory()
    normal_strategy = NormalStrategy()
    aggresive_strategy = AggressiveStrategy()

    print('''Tournament 0 (basic)
 [ (Flameling+Normal), (Shiftling+Aggressive) ]
*** Tournament ***
2 opponents involved''')
    battle([(flame_factory, normal_strategy), (transform_creature_factory, aggressive_strategy)])
    


def battle(opponets: list[tuple[CreatureFactory, BattleStrategy]]):
    ...


if __name__ == "__main__":
    main()