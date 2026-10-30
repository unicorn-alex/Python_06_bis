from abc import ABC, abstractmethod
from typing import Any


class BattleStrategy(ABC):

    @abstractmethod
    def act(self, entity: Any) -> None:
        pass

    @abstractmethod
    def is_valid(self, entity: Any) -> bool:
        pass


class NormalStrategy(BattleStrategy):

    def act(self, entity: Any) -> None:
        print(entity.attack())

    def is_valid(self, entity: Any) -> bool:
        has_attack = callable(getattr(entity, "attack", None))
        return has_attack


class AggressiveStrategy(BattleStrategy):

    def act(self, entity: Any) -> None:
        print(entity.transform())
        print(entity.attack())
        print(entity.revert())

    def is_valid(self, entity: Any) -> bool:
        has_attack = callable(getattr(entity, "attack", None))
        has_transform = callable(getattr(entity, "transform", None))
        has_revert = callable(getattr(entity, "revert", None))
        return has_attack and has_transform and has_revert
