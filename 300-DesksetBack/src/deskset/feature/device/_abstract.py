from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    @abstractmethod
    def monitor(self) -> dict:
        pass

    @abstractmethod
    def disk(self, is_gb: bool = True) -> list[dict]:
        pass

    @abstractmethod
    def battery(self) -> dict:
        pass

    @abstractmethod
    def system(self) -> dict:
        pass
