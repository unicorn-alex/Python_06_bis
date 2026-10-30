from abc import ABC, abstractmethod


class TransformCapability(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._transformed = False

    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
