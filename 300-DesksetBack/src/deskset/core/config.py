from __future__ import annotations
from deskset.core.log import logging

CONFIG_MAIN_PATH = './config/desksetback.yaml'
CONFIG_MAIN_ENCODE = 'utf-8'

from locale import getdefaultlocale
lang, _ = getdefaultlocale()
DEFAULT_LANGUAGE = 'zh-cn' if lang is not None and lang.startswith('zh') else 'en'


# ==== 读写 config/desksetback.yaml 中的配置 ====
from pydantic import BaseModel, field_validator
from random import choices, randint
import yaml

VALID_LANGUAGE_LIST = ['zh-cn', 'en']
VALID_ENCODING_LIST = ['utf-8']

CHARS_STR = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789' + '-'


class ValidateConfig(
    BaseModel,
    validate_assignment=True,  # 验证属性修改
    validate_default=True      # 验证默认值
):
    language: str = 'en'     # 语言
    encoding: str = 'utf-8'  # 编码

    server_host: str = '127.0.0.1'  # 监听 IP
    server_port: int = 6527         # 监听端口

    # username 和 password 每次都随机生成，读取配置文件成功再被覆盖
    username: str = 'deskset-user' + ''.join(choices(CHARS_STR, k=randint(5, 10)))   # 用户名
    password: str = 'deskset-pswd' + ''.join(choices(CHARS_STR, k=randint(10, 20)))  # 密码

    @field_validator('language')
    @classmethod
    def check_language(cls, v: str) -> str:
        if v not in VALID_LANGUAGE_LIST:
            raise ValueError(f'Invalid language\nvalid choice = {VALID_LANGUAGE_LIST}')
        return v

    @field_validator('encoding')
    @classmethod
    def check_encoding(cls, v: str) -> str:
        if v not in VALID_ENCODING_LIST:
            raise ValueError(f'Invalid encoding\nvalid choice = {VALID_ENCODING_LIST}')
        return v

    @field_validator('server_host')
    @classmethod
    def check_server_host(cls, v: str) -> str:
        if v != '127.0.0.1':  # 后续改进，暂时限定仅监听 127.0.0.1 IP
            raise ValueError(f'Invalid server-host\nonly allow 127.0.0.1')
        return v

    @field_validator('server_port')
    @classmethod
    def check_server_port(cls, v: int) -> int:
        if not (1024 <= v <= 65535):
            raise ValueError(f'Invalid server-port.\nport between 1024 ~ 65535')
        return v

    @field_validator('username')
    @classmethod
    def check_username(cls, v: str) -> str:
        if len(v) == 0:
            raise ValueError('Invalid username, username cannot be empty string')
        if not all(char in CHARS_STR for char in v):
            raise ValueError(f'Invalid username.\nchar range = \'{CHARS_STR}\'')
        return v

    @field_validator('password')
    @classmethod
    def check_password(cls, v: str) -> str:
        if len(v) == 0:
            raise ValueError('Invalid password, password cannot be empty string')
        if not all(char in CHARS_STR for char in v):
            raise ValueError(f'Invalid password.\nchar range = \'{CHARS_STR}\'')
        return v


class Config:
    def __init__(self) -> None:
        # --- 1、设置默认值 ---
        self._validate_config = ValidateConfig()

        # --- 2、先读再写，覆盖无效配置项 ---
        self.__load_config(self._validate_config)
        self.__save_config(self._validate_config)

        # --- 3、记录运行时配置 ---
          # runtime 代表运行时属性，是程序当前生效的属性值
          # storage 代表持久化属性，是配置文件保存的属性值
        self._language_runtime = self._validate_config.language
        self._server_port_runtime = self._validate_config.server_port

    @classmethod
    def __load_config(cls, instance: object) -> None:
        try:
            with open(CONFIG_MAIN_PATH, 'r', encoding=CONFIG_MAIN_ENCODE) as file:
                data: dict = yaml.safe_load(file)
                # 配置文件内容为空，读取的 data 为 None
                if data is None:
                    raise TypeError('data is None')

                for attr_key, attr_value in list(instance.__dict__.items()):  # list 创建副本后修改 self 属性
                    # 不是私有成员属性
                    if attr_key.startswith('_'):
                        continue

                    # 修改属性。注：setattr 不会丢掉类型检查
                    value = data.get(attr_key)
                    try:
                        setattr(instance, attr_key, value)
                    except ValueError as value_error:
                        logging.warning(f'Validate \'{attr_key}\' fail on reading {CONFIG_MAIN_PATH[2:]}\n{value_error}')
        except FileNotFoundError:
            logging.warning(f'{CONFIG_MAIN_PATH} not found')
        except TypeError as type_error:
            logging.warning(f'{CONFIG_MAIN_PATH} is empty. Error message: {type_error}')
        except yaml.YAMLError:
            logging.warning(f'{CONFIG_MAIN_PATH} decode failed')

    @classmethod
    def __save_config(cls, instance: object, yaml_key: str | None = None, yaml_value: object | None = None) -> None:
        # 检查属性
          # 注：如果在写入文件时抛出异常，会使文件内容清空
        if yaml_key is not None and yaml_value is not None:
            getattr(instance, 'check_' + yaml_key)(yaml_value)

        with open(CONFIG_MAIN_PATH, 'w', encoding=CONFIG_MAIN_ENCODE) as file:
            data: dict = {
                key: value for key, value in instance.__dict__.items() if not key.startswith('_')
            }
            # 先写入文件，再修改属性
            if yaml_key is not None and yaml_value is not None and data.get(yaml_key, None) is not None:
                data[yaml_key] = yaml_value                                 # 修改 data 属性，新值更新旧值
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)  # 写入文件
                setattr(instance, yaml_key, yaml_value)   # 修改 instance 属性；预期行为：触发二次检查
            # 直接写入文件
            else:
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)

    @property
    def language(self) -> str:
        if self._language_runtime:
            return self._language_runtime
        return self._validate_config.language
    @property
    def language_storage(self) -> str:
        return self._validate_config.language
    @language.setter
    def language(self, language: str) -> None:
        self.__save_config(self._validate_config, 'language', language)

    @property
    def encoding(self) -> str:
        return self._validate_config.encoding

    @property
    def server_host(self) -> str:
        return self._validate_config.server_host

    @property
    def server_port(self) -> int:
        if self._server_port_runtime:
            return self._server_port_runtime
        return self._validate_config.server_port
    @property
    def server_port_storage(self) -> int:
        return self._validate_config.server_port
    @server_port.setter
    def server_port(self, server_port: int) -> None:
        self.__save_config(self._validate_config, 'server_port', server_port)

    @property
    def username(self) -> str:
        return self._validate_config.username
    @username.setter
    def username(self, username: str) -> None:
        self.__save_config(self._validate_config, 'username', username)

    @property
    def password(self) -> str:
        return self._validate_config.password
    @password.setter
    def password(self, password: str) -> None:
        self.__save_config(self._validate_config, 'password', password)


config = Config()
