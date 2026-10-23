import abc
from typing import Any, Generator

#generatory chyba ne ,prawda (sprawdzic w module 3 generatory i typing dla dict)

# czy uzywali do czegos self w validate
# dlaczego w case int() musza byc nawiasy, a w if juz nie moga
# czy mam racje, ze w output potrzebny jest generator

class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self._storage: list[Any] = []

    def get_storage(self) -> list[Any]:
        return self._storage

    def set_storage(self, data: Any) -> None:
        self._storage = data

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) ->  Generator[tuple[int, str], None, None]:
        rank = 0
        while self._storage != []:
            element = self._storage[0]
            self._storage.remove(element)
            yield rank, element
            rank += 1



class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        match data:
            case int():
                return True
            case float():
                return True
            case list():
                for element in data:
                    if type(element) is not int and type(element) is not float:
                        return False
                return True
            case _:
                return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        try:
            if type(data) is list:
                for element in data:
                    if type(element) is not int and type(element) is not float:
                        raise ValueError
                for element in data:
                    self._storage.append(str(element))
            elif type(data) is int or type(data) is float:
                    self._storage.append(str(data))
            else:
                raise ValueError
        except ValueError:
                    print(" Got exception: Improper numeric data")
                    return

class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        match data:
            case str():
                return True
            case list():
                for element in data:
                    if type(element) is not str:
                        return False
                return True
            case _:
                return False

    def ingest(self, data: str | list[str]) -> None:
        try:
            if type(data) is list:
                for element in data:
                    if type(element) is not str:
                        raise ValueError
                self._storage.extend(data)
            elif type(data) is str:
                    self._storage.append(data)
            else:
                raise ValueError
        except ValueError:
            print(" Got exception: Improper text data")
            return


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        match data:
            case dict():
                for key, value in data.items():
                    if type(key) is not str or type(value) is not str:
                        return False
                return True
            case list():
                for item in data:
                    if type(item) is not dict:
                        return False
                    for key, value in item.items():
                        if type(key) is not str or type(value) is not str:
                            return False
                return True
            case _:
                return False

    def ingest(self, data: dict[str, str] | list[dict[str,str]]) -> None:
        try:
            if type(data) is dict:
                for key, value in data.items():
                    if type(key) is not str or type(value) is not str:
                        raise ValueError
                for key, value in data.items():
                    self._storage.append(key + ': ' + value)
            elif type(data) is list:
                for item in data:
                    if type(item) is not dict:
                        raise ValueError
                    for key, value in item.items():
                        if type(key) is not str or type(value) is not str:
                            raise ValueError
                    for key, value in item.items():
                        self._storage.append(key + ': ' + value)
            else:
                raise ValueError
        except ValueError:
            print(" Got exception: Improper log data")
            return