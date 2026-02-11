from ._abstract import AbstractDevice


class UnknownDevice(AbstractDevice):
    def monitor(self) -> dict:
        raise SystemError('Unknown System')

    def disk(self, is_gb: bool = True) -> list[dict]:
        raise SystemError('Unknown System')

    def battery(self) -> dict:
        raise SystemError('Unknown System')

    def system(self) -> dict:
        raise SystemError('Unknown System')
