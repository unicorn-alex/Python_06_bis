import abc
from typing import Any, Generator


class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self._storage: list[Any] = []

    def get_storage(self) -> list[Any]:
        return self._storage

    def set_storage(self, data: list[Any]) -> None:
        self._storage = data

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> Generator[tuple[int, str], None, None]:
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

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
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
                    log = ""
                    for value in item.values():
                        log += value + ": "
                    self._storage.append(log.rstrip(": "))
            else:
                raise ValueError
        except ValueError:
            print(" Got exception: Improper log data")
            return


class DataStream():

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._processed_data: dict[DataProcessor, int] = {}

    def get_processors(self) -> list[DataProcessor]:
        return self._processors

    def set_processors(self, data: list[DataProcessor]) -> None:
        self._processors = data

    def get_processed_data(self) -> dict[DataProcessor, int]:
        return self._processed_data

    def set__processed_data(self, data: dict[DataProcessor, int]) -> None:
        self._processed_data = data

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)
        self._processed_data.update({proc: 0})

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            data_matching = False
            for proc in self._processors:
                if proc.validate(data) is True:
                    data_matching = True
                    break
            if data_matching is True:
                before_ingestion = len(proc.get_storage())
                proc.ingest(data)
                self._processed_data[proc] += (
                    len(proc.get_storage()) - before_ingestion)
            else:
                print("DataStream error - Can't process element in stream:",
                      data)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if self._processors == []:
            print("No processor found, no data\n")
            return
        for proc in self._processors:
            if type(proc) is NumericProcessor:
                print(f"Numeric Processor: total {self._processed_data[proc]}",
                      f"items processed, remaining {len(proc.get_storage())}",
                      "on processor")
            if type(proc) is TextProcessor:
                print(f"Text Processor: total {self._processed_data[proc]}",
                      f"items processed, remaining {len(proc.get_storage())}",
                      "on processor")
            if type(proc) is LogProcessor:
                print(f"Log Processor: total {self._processed_data[proc]}",
                      f"items processed, remaining {len(proc.get_storage())}",
                      "on processor")


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    data_stream = DataStream()
    data_stream.print_processors_stats()

    print("Registering Numeric Processor\n")
    numbers = NumericProcessor()
    data_stream.register_processor(numbers)

    print("Send first batch of data on stream: ['Hello world',",
          "[3.14, -1, 2.71], [{'log_level': 'WARNING',",
          "'log_message': 'Telnet access! Use ssh instead'},",
          "{'log_level': 'INFO', 'log_message': 'User wil is connected'}],",
          "42, ['Hi', 'five']]")
    stream = ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING',
              'log_message': 'Telnet access! Use ssh instead'}, {
              'log_level': 'INFO', 'log_message': 'User wil is connected'}],
              42, ['Hi', 'five']]
    data_stream.process_stream(stream)
    data_stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    data_stream.register_processor(text)
    logs = LogProcessor()
    data_stream.register_processor(logs)
    print("Send the same batch again")
    data_stream.process_stream(stream)
    data_stream.print_processors_stats()

    print("\nConsume some elements from the data processors:",
          "Numeric 3, Text 2, Log 1")
    num_consumer = numbers.output()
    text_consumer = text.output()
    log_consumer = logs.output()
    for i in range(3):
        next(num_consumer)
    for i in range(2):
        next(text_consumer)
    next(log_consumer)

    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
