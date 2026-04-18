from deskset.shared.error import UnknownSystemError
from ._abstract import AbstractDevice


class UnknownDevice(AbstractDevice):
    def monitor(self) -> dict:
        raise UnknownSystemError()

    def disk(self, is_gb: bool = True) -> list[dict]:
        raise UnknownSystemError()

    def battery(self) -> dict:
        raise UnknownSystemError()

    def system(self) -> dict:
        raise UnknownSystemError()
