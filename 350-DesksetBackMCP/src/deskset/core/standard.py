from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from deskset.core.log import logging

class DesksetError(Exception):
    def __init__(
            self,
            code:    int = 1,
            message: str = 'Fail',
            data:    Any = None
        ) -> None:
        self.code    = code
        self.message = message
        self.data    = data

    def insert(self, *args: str) -> DesksetError:
        """动态注释：注释初值包含占位符 {}，抛出异常时，动态插入错误信息"""
        # 1、初值
        #   yaml 文件：'This is a placeholder: {}': '这是一个占位符：{}'
        #   _t() 翻译：'This is a placeholder: {}'=>'这是一个占位符：{}'
        # 2、插入
        #   '这是一个占位符：{}'.format('dynamic') => '这是一个占位符：dynamic'
        #   注：对 self.message 中 {} 插入替换，因此 *arg 可以包含 {}
        try:
            return DesksetError(code=self.code, message=self.message.format(*args))
        except IndexError:  # 翻译前或翻译后，当占位符 {} 多于参数 args 时报错
            log_error = ''
            log_error += 'DesksetError Dynamic Message! Extra Placeholder: '
            log_error += f'\'{self.message}\'.format{args}'
            logging.error(log_error)

            # 报错后，不替换占位符，返回原字符串
            return DesksetError(code=self.code, message=self.message)
