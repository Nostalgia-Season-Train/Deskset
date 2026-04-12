from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypedDict


class AbstractDevice(ABC):
    class Monitor(TypedDict):
        class Cpu(TypedDict):
            percent: float
            freq: float
            count: int
        class Ram(TypedDict):
            percent: float
            used: float
            total: int
        class Disk(TypedDict):
            percent: float
        class Network(TypedDict):
            sent: float
            recv: float
        cpu: AbstractDevice.Monitor.Cpu
        ram: AbstractDevice.Monitor.Ram
        disk: AbstractDevice.Monitor.Disk
        network: AbstractDevice.Monitor.Network
    @abstractmethod
    def monitor(self) -> AbstractDevice.Monitor:
        pass

    class Disk(TypedDict):
        root: str
        total: int | float
        free: int | float
        percent: float
    @abstractmethod
    def disk(self, is_gb: bool = True) -> AbstractDevice.Disk:
        pass

    class Battery(TypedDict):
        isplug: bool
        percent: int
    @abstractmethod
    def battery(self) -> AbstractDevice.Battery:
        pass

    class System(TypedDict):
        name: str
        system: str
        version: str
        machine: str
    @abstractmethod
    def system(self) -> AbstractDevice.System:
        pass
