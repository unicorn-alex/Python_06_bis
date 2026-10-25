from ex3 import FlameFactory, TransformCreatureFactory, CreatureFactory

# rozkminic dokladniej czy rozumiem ten pattern
# rozkminic czy rozumiem ten init
# rozkminic czy importy sa dobrze
# +problem w factories z typingiem


def main() -> None:
    print("Testing factory")
    flame_factory = FlameFactory()
    describe_entities(flame_factory)

    print("\nTesting factory")
    transform_creature_factory = TransformCreatureFactory()
    describe_entities(transform_creature_factory)

    print("\nTesting battle")
    make_fight(flame_factory, transform_creature_factory)

def describe_entities(factory: CreatureFactory):
    base_entity = factory.create_base()
    print(base_entity.describe())
    print(base_entity.attack())

    evolved_entity = factory.create_evolved()
    print(evolved_entity.describe())
    print(evolved_entity.attack())

def make_fight(factory_1: CreatureFactory, factory_2: CreatureFactory):
    base_entity_1 = factory_1.create_base()
    base_entity_2 = factory_2.create_base()

    print(base_entity_1.describe())
    print(" vs.")
    print(base_entity_2.describe())
    print(base_entity_1.attack())
    print(base_entity_2.attack())


if __name__ == "__main__":
    main()