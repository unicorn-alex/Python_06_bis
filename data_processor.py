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


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...\n")
    numbers = NumericProcessor()

    print(f" Trying to validate input '42': {numbers.validate(42)}")
    print(f" Trying to validate input 'Hello': {numbers.validate("Hello")}")
    print(f" Trying to validate input [34, 78.0. 92]: {numbers.validate([34, 78.0, 92])}")
    print(f" Trying to validate input [-5, 1245, 73]: {numbers.validate([-5, 1245, 73])}")
    print(f" Trying to validate input [56.0, -35.0, 222.0]: {numbers.validate([56.0, -35.0, 222.0])}")
    print(f" Trying to validate input [45, 'a', 45.0, 23]: {numbers.validate([45, 'a', 45.0, 23])}\n")

    print(" Test invalid ingestion of string 'foo' without prior validation: ")
    numbers.ingest("foo")
    print(" Test invalid ingestion of list [45, 'a', 45.0, 23] without prior validation: ")
    numbers.ingest([45, 'a', 45.0, 23])
    print(" Processing data: [1, 2, 3, 4, 5]\n")
    numbers.ingest([1, 2, 3, 4, 5])

    print(" Extracting 3 values...")
    num_values = numbers.output()
    for i in range(3):
        num_value = next(num_values)
        print(f" Numeric value {num_value[0]}: {num_value[1]}")
    print('\n')


    print("Testing Text Processor...\n")
    text = TextProcessor()

    print(f" Trying to validate input '42': {text.validate(42)}")
    print(f" Trying to validate input [56, 'lol', 'poop']: {text.validate([56, 'lol', 'poop'])}")
    print(f" Trying to validate input 'abrakadabra': {text.validate("abrakadabra")}")
    print(f" Trying to validate input ['Ala', 'ma', 'kota']: {text.validate(['Ala', 'ma', 'kota'])}\n")

    print(" Test invalid ingestion of list '[45, 'a', 45.0, 23]' without prior validation: ")
    text.ingest([45, 'a', 45.0, 23])
    print(" Test invalid ingestion of float '56.0' without prior validation: ")
    text.ingest(56.0)
    print(" Processing data: ['Hello', 'Nexus', 'World']\n")
    text.ingest(['Hello', 'Nexus', 'World'])

    print(" Extracting 1 value...")
    text_values = text.output()
    text_value = next(text_values)
    print(f" Text value {text_value[0]}: {text_value[1]}\n\n")


    print("Testing Log Processor...\n")
    logs = LogProcessor()

    print(f" Trying to validate input 'Hello': {logs.validate("Hello")}")
    print(f" Trying to validate input {{'Hello': 'Obama', 'strucle': 42, 'Jojo': 'hop'}}: {logs.validate({'Hello': 'Obama', 'strucle': 42, 'Jojo': 'hop'})}")
    print(f" Trying to validate input [{{'log_level': 'NOTICE', 'log_message': 'Connection to server'}}, {{'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}}]: {logs.validate([{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}])}\n")

    print(" Test invalid ingestion of str 'Hello' without prior validation: ")
    logs.ingest("Hello")
    print(" Test invalid ingestion of dict '{'Hello': 'Obama', 'strucle': 42, 'Jojo': 'hop'}' without prior validation: ")
    logs.ingest({'Hello': 'Obama', 'strucle': 42, 'Jojo': 'hop'})
    print(" Processing data: [{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level':'ERROR', 'log_message': 'Unauthorized access!!'}]\n")
    logs.ingest([{'log_level': 'NOTICE', 'log_message': 'Connection to server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}])

    print(" Extracting 2 values...")
    log_values = logs.output()
    for i in range(2):
        log_value = next(log_values)
        print(f" Log entry {log_value[0]}: {log_value[1]}")


if __name__ =="__main__":
    main()