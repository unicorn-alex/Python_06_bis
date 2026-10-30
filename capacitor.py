from ex3 import TransformCreatureFactory


def main() -> None:
    print("Testing Creature with transform capability")
    transform_creature_factory = TransformCreatureFactory()

    print(" base:")
    base_entity = transform_creature_factory.create_base()
    print(base_entity.describe())
    print(base_entity.attack())
    print(base_entity.transform())
    print(base_entity.attack())
    print(base_entity.revert())

    print(" evolved:")
    evolved_entity = transform_creature_factory.create_evolved()
    print(evolved_entity.describe())
    print(evolved_entity.attack())
    print(evolved_entity.transform())
    print(evolved_entity.attack())
    print(evolved_entity.revert())


if __name__ == "__main__":
    main()
