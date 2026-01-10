# ==== 数字桌搭在自身目录下存放的配置 ====
from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod

from deskset.core.log import logging
from deskset.core.standard import DesksetError
from deskset.core.config import write_conf_file, read_conf_file


class ConfVault:
    _confitem_path: Optional[str]

    def __init__(self):
        self._observers: list[ConfVaultObserver] = []
        self._confpath = 'note/obsidian/vault'
        self._confitem_path = ''  # 仓库路径
        try:
            read_conf_file(self)
        except DesksetError as err:
            logging.error(err.message)
        finally:
            write_conf_file(self)

    def attach(self, observer: ConfVaultObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: ConfVaultObserver) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    # 获取和设置 _confitem_path 仓库路径
    @property
    def path(self) -> str:
        return self._confitem_path

    @path.setter
    def path(self, path: str) -> None:
        if self._confitem_path == path:  # 路径没有改变，直接返回
            return
        self._confitem_path = path
        write_conf_file(self)
        self.notify()


class ConfVaultObserver(ABC):
    @abstractmethod
    def update(self, conf_vault: ConfVault) -> None:
        pass
