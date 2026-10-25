from abc import ABC, abstractmethod

class BattleStrategy(ABC):

    @abstractmethod
    def act(self):
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

class NormalStrategy(BattleStrategy):

    def act(self, entity):
        ...

    def is_valid(self, entity):
        ...

class AggressiveStrategy(BattleStrategy):

    def act(self, entity):
        ...

    def is_valid(self, entity):
        ...
