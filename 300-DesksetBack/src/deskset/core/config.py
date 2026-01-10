from __future__ import annotations
from typing import Optional

# 为了在 config 目录区分 DesksetBack 和 DesksetFront 配置
import yaml  # DesksetBack 优先配置格式 yaml
import json  # DesksetFront 优先配置格式 json

from deskset.core.log import logging

CONFIG_MAIN_PATH = './config/desksetback.yaml'
CONFIG_MAIN_ENCODE = 'utf-8'

from locale import getdefaultlocale
lang, _ = getdefaultlocale()
DEFAULT_LANGUAGE = 'zh-cn' if lang is not None and lang.startswith('zh') else 'en'


# ==== 读写 config/desksetback.yaml 中的配置 ====
from pydantic import BaseModel, field_validator
from random import choices, randint

VALID_LANGUAGE_LIST = ['zh-cn', 'en']
VALID_ENCODING_LIST = ['utf-8']

CHARS_STR = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789' + '-'


class ValidateConfig(BaseModel, validate_assignment=True):
    language: str = DEFAULT_LANGUAGE  # 语言
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
        if not all(char in CHARS_STR for char in v):
            raise ValueError(f'Invalid username.\nchar range = \'{CHARS_STR}\'')
        return v

    @field_validator('password')
    @classmethod
    def check_password(cls, v: str) -> str:
        if not all(char in CHARS_STR for char in v):
            raise ValueError(f'Invalid password.\nchar range = \'{CHARS_STR}\'')
        return v


class Config:
    def __init__(self) -> None:
        # --- 1、设置默认值 ---
        self._validate_config = ValidateConfig()

        self._runtime_language: str | None = None
        self._runtime_server_port: int | None = None  # 如果 _confitem_server_port 变化，记录服务器当前运行端口

        # --- 2、先读再写，覆盖无效配置项 ---
        self._read_config_file(self._validate_config)
        self._write_config_file(self._validate_config)

    @classmethod
    def _read_config_file(cls, instance: object) -> None:
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

                    # 配置类型跟默认值一致
                    config_key = attr_key.replace('_', '-')
                    config_type = type(attr_value)
                    if type(data.get(config_key)) != config_type:
                        continue

                    # 修改属性。注：setattr 不会丢掉类型检查
                    value = data.get(config_key)
                    try:
                        setattr(instance, attr_key, value)
                    except ValueError as value_error:
                        logging.warning(f'Validate \'{config_key}\' fail on reading {CONFIG_MAIN_PATH[2:]}\n{value_error}')
        except FileNotFoundError:
            logging.warning(f'{CONFIG_MAIN_PATH} not found')
            pass
        except TypeError as type_error:
            logging.warning(f'{CONFIG_MAIN_PATH} is empty. Error message: {type_error}')
            pass
        except yaml.YAMLError:
            logging.warning(f'{CONFIG_MAIN_PATH} decode failed')
            pass

    @classmethod
    def _write_config_file(cls, instance: object, yaml_key: str | None = None, yaml_value: object | None = None) -> None:
        # 检查属性
          # 注：如果在写入文件时抛出异常，会使文件内容清空
        if yaml_key is not None and yaml_value is not None:
            getattr(instance, 'check_' + yaml_key.replace('-', '_'))(yaml_value)

        with open(CONFIG_MAIN_PATH, 'w', encoding=CONFIG_MAIN_ENCODE) as file:
            data: dict = {
                key.replace('_', '-'): value for key, value in instance.__dict__.items() if not key.startswith('_')
            }
            # 先写入文件，再修改属性
            if yaml_key is not None and yaml_value is not None and data.get(yaml_key, None) is not None:
                data[yaml_key] = yaml_value                                 # 修改 data 属性，新值更新旧值
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)  # 写入文件
                setattr(instance, yaml_key.replace('-', '_'), yaml_value)   # 修改 instance 属性；预期行为：触发二次检查
            # 直接写入文件
            else:
                yaml.dump(data, file, allow_unicode=True, sort_keys=False)

    @property
    def language(self) -> str:
        if self._runtime_language:
            return self._runtime_language
        return self._validate_config.language

    @property
    def language_in_yaml(self) -> str:
        return self._validate_config.language

    @language.setter
    def language(self, language: str) -> None:
        if self._runtime_language is None:
            self._runtime_language = self._validate_config.language
        self._write_config_file(self._validate_config, 'language', language)

    @property
    def encoding(self) -> str:
        return self._validate_config.encoding

    @property
    def server_host(self) -> str:
        return self._validate_config.server_host

    @property
    def server_port(self) -> int:
        if self._runtime_server_port:
            return self._runtime_server_port
        return self._validate_config.server_port

    @property
    def server_port_in_yaml(self) -> int:
        return self._validate_config.server_port

    @server_port.setter
    def server_port(self, server_port: int) -> None:
        if self._runtime_server_port is None:
            self._runtime_server_port = self._validate_config.server_port  # 第一次修改，记录当前端口
        self._write_config_file(self._validate_config, 'server-port', server_port)

    @property
    def username(self) -> str:
        return self._validate_config.username

    @username.setter
    def username(self, username: str) -> None:
        if len(username) == 0:
            raise ValueError('username cannot be empty string')
        self._write_config_file(self._validate_config, 'username', username)

    @property
    def password(self) -> str:
        return self._validate_config.password

    @password.setter
    def password(self, password: str) -> None:
        if len(password) == 0:
            raise ValueError('password cannot be empty string')
        self._write_config_file(self._validate_config, 'password', password)


config = Config()


if __name__ == '__main__':
    for attr_key, attr_value in config.__dict__.items():
        print(attr_key, attr_value)


# ==== 配置读写函数 ====
  # 根据实例成员，读写配置
  # _confpath 以 config 作根目录，读写 config/{_confpath}.yaml 文件，编码一律 utf-8
  # _confitem_key = value 对应 key: value 配置项
    # _confitem_custom_prop 下划线将被连字符替换 custom-prop
  # 使用提醒：
    # 成员：self._confXXX（注意 self）
    # 类型提示：class Conf: _confXXX: str（在类中注解）
from pathlib import Path
from typing import get_type_hints, get_args

# 这里存在循环引用 config < standard < locale < config
  # 但是只要 config 在此之前定义，那就没有问题
# 2025/08/02：去掉 standard 对 locale 的导入，以上注释留作说明
from deskset.core.standard import DesksetError

READ_CONFFILE_ERROR = DesksetError(message='配置文件 {} 读取失败：{}！')


def write_conf_file(instance: object) -> None:
    if getattr(instance, '_confpath', None) is None:
        raise ValueError(f'_confpath not exist in {type(instance)} class')
    relpath = Path('./config') / f'{instance._confpath}.yaml'  # type: ignore

    items = {}  # 配置项

    for attr_key, attr_value in list(instance.__dict__.items()):
        if not attr_key.startswith('_confitem_'):
            continue

        key = attr_key[len('_confitem_'):].replace('_', '-')  # [len('_confitem_'):] 去掉 _confitem_
        value = attr_value
        items[key] = value  # Python 3.7+ 开始字典有序

    relpath.parent.mkdir(parents=True, exist_ok=True)  # open 不会创建目录，用 Path 提前创建

    with open(relpath, 'w', encoding='utf-8') as file:
        yaml.dump(items, file, allow_unicode=True, sort_keys=False)  # sort_keys=False 不排序


def read_conf_file(instance: object) -> None:
    if getattr(instance, '_confpath', None) is None:
        raise ValueError(f'_confpath not exist in {type(instance)} class')
    relpath = Path('./config') / f'{instance._confpath}.yaml'  # type: ignore

    # 读取文件，异常由调用方处理
      # 可能异常：文件不存在 FileNotFoundError、yaml 解析失败 yaml.YAMLError、yaml 解析非字典 TypeError
    if not relpath.is_file():
        raise READ_CONFFILE_ERROR.insert(str(relpath), '文件不存在')
    with open(relpath, 'r', encoding='utf-8') as file:
        try:
            items: dict = yaml.safe_load(file)
        except yaml.YAMLError:
            raise READ_CONFFILE_ERROR.insert(str(relpath), 'YAML 解析失败')

        # 没解析成字典，也算异常
        if not isinstance(items, dict):
            raise READ_CONFFILE_ERROR.insert(relpath, '解析结果不是字典')

        # attr_value 作为配置项默认值
        for attr_key, attr_value in list(instance.__dict__.items()):
            if not attr_key.startswith('_confitem_'):
                continue

            value_type = type(attr_value)
            key = attr_key[len('_confitem_'):].replace('_', '-')
            value = items.get(key, None)

            if type(value) != value_type:  # 值类型 != 配置项默认值类型
                continue

            if   value_type == type(10000):
                setattr(instance, attr_key, value)
            elif value_type == type('str'):
                if value != '':
                    setattr(instance, attr_key, value)
                if value == '':  # 类型标注包含 None = 允许空字符串
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, '')


# ==== 配置读写函数（绝对路径） ====
  # 配置路径从绝对路径 _confabspath（包括文件后缀）读取
def write_conf_file_abspath(instance: object, format: str = 'yaml') -> None:
    if getattr(instance, '_confabspath', None) is None:
        raise ValueError(f'_confabspath not exist in {type(instance)} class')
    abspath = Path(instance._confabspath)  # type: ignore

    items = {}  # 配置项

    for attr_key, attr_value in list(instance.__dict__.items()):
        if not attr_key.startswith('_confitem_'):
            continue

        key = attr_key[len('_confitem_'):].replace('_', '-')  # [len('_confitem_'):] 去掉 _confitem_
        value = attr_value
        items[key] = value  # Python 3.7+ 开始字典有序

    abspath.parent.mkdir(parents=True, exist_ok=True)  # open 不会创建目录，用 Path 提前创建

    with open(abspath, 'w', encoding='utf-8') as file:
        if format == 'yaml':
            yaml.dump(items, file, allow_unicode=True, sort_keys=False)  # sort_keys=False 不排序
        if format == 'json':
            json.dump(items, file, ensure_ascii=False, indent=4)


def read_conf_file_abspath(instance: object, format: str = 'yaml') -> None:
    if getattr(instance, '_confabspath', None) is None:
        raise ValueError(f'_confabspath not exist in {type(instance)} class')
    abspath = Path(instance._confabspath)  # type: ignore

    # 读取文件，异常由调用方处理
      # 可能异常：文件不存在 FileNotFoundError、yaml 解析失败 yaml.YAMLError、yaml 解析非字典 TypeError
    if not abspath.is_file():
        raise READ_CONFFILE_ERROR.insert(str(abspath), '文件不存在')
    with open(abspath, 'r', encoding='utf-8') as file:
        if format == 'yaml':
            try:
                items: dict = yaml.safe_load(file)
            except yaml.YAMLError:
                raise READ_CONFFILE_ERROR.insert(str(abspath), 'YAML 解析失败')
        if format == 'json':
            try:
                items: dict = json.load(file)
            except json.JSONDecodeError:
                raise READ_CONFFILE_ERROR.insert(str(abspath), 'JSON 解析失败')

        # 没解析成字典，也算异常
        if not isinstance(items, dict):  # type: ignore 暂时不管...
            raise READ_CONFFILE_ERROR.insert(str(abspath), '解析结果不是字典')

        # attr_value 作为配置项默认值
        for attr_key, attr_value in list(instance.__dict__.items()):
            if not attr_key.startswith('_confitem_'):
                continue

            value_type = type(attr_value)
            key = attr_key[len('_confitem_'):].replace('_', '-')
            value = items.get(key, None)

            if type(value) != value_type:  # 值类型 != 配置项默认值类型
                continue

            if   value_type == type(10000):
                setattr(instance, attr_key, value)
            elif value_type == type('str'):
                if value != '':
                    setattr(instance, attr_key, value)
                if value == '':  # 类型标注包含 None = 允许空字符串
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, '')
            elif value_type == type([]):  # 附：可以解析 list[dict] 类型
                if len(value) != 0:  # type: ignore vscode pyright 无法间接推断 value 类型
                    setattr(instance, attr_key, value)
                if len(value) == 0:  # 同上，包含 None 允许列表为空  # type: ignore 同上
                    annotations = get_type_hints(type(instance))
                    if type(None) in get_args(annotations.get(attr_key)):
                        setattr(instance, attr_key, [])
