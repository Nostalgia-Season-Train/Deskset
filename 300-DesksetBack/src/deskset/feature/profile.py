from typing import Any, get_type_hints, get_args
from yaml import safe_load as yaml_load, dump as yaml_dump
from deskset.core.log import logging

CONF_PROFILE_PATH = './config/profile.yaml'
CONF_PROFILE_ENCODE = 'utf-8'
CONF_PROFILE_ITEM_PREFIX = '_item_'  # 如果本行 PREFIX 发生改动，记得重命名 Profile 成员变量的前缀



# 术语
  # conf = { key1: value1, key2: value2 }, { key: value } as item
  # key = example_name
  # attr_key = prefix_example_name
class ConfProfile:
    _item_name: str
    _item_bio: str

    def __init__(self) -> None:
        self._item_name = '数字桌搭'
        self._item_bio = '数字桌搭，桌面美化与笔记应用的完美互动'
        # 先读再写，覆盖无效配置项
        self.__load_conf()
        self.__save_conf()


    # ==== attr_key/key 转换 ====
    def __attr_key_to_key(self, attr_key: str) -> str:
        return attr_key.replace(CONF_PROFILE_ITEM_PREFIX, '', 1)

    def __key_to_attr_key(self, key: str) -> str:
        return CONF_PROFILE_ITEM_PREFIX + key


    # ==== 获取/修改配置 ====
    def __get_conf(self) -> dict[str, Any]:
        conf = {}
        for attr_key, attr_value in list(self.__dict__.items()):
            if not attr_key.startswith(CONF_PROFILE_ITEM_PREFIX):
                continue
            key = self.__attr_key_to_key(attr_key)
            value = attr_value
            conf[key] = value
        return conf

    def __set_conf(self, conf: dict[str, Any]) -> None:
        for attr_key, _ in list(self.__dict__.items()):
            if not attr_key.startswith(CONF_PROFILE_ITEM_PREFIX):
                continue
            key = self.__attr_key_to_key(attr_key)
            value = conf.get(key)
            try:  # error 级问题，跳过校验失败的配置项，继续循环
                setattr(self, key, value)
            except TypeError as type_error:
                logging.error(type_error)
            except ValueError as value_error:
                logging.error(value_error)


    # ==== 加载/保存文件 ====
    def __load_conf(self):
        try:
            conf = {}
            with open(CONF_PROFILE_PATH, 'r', encoding=CONF_PROFILE_ENCODE) as file:
                conf = yaml_load(file)

            self.__set_conf(conf)

        except Exception as exc:
            logging.exception(exc, exc_info=exc)

    def __save_conf(self):
        try:
            conf = self.__get_conf()

            from pathlib import Path
            Path(CONF_PROFILE_PATH).parent.mkdir(parents=True, exist_ok=True)  # open 不会创建目录，用 Path 提前创建
            with open(CONF_PROFILE_PATH, 'w', encoding=CONF_PROFILE_ENCODE) as file:
                yaml_dump(conf, file, allow_unicode=True, sort_keys=False)

        except Exception as exc:
            logging.exception(exc, exc_info=exc)


    # ==== 配置项 ====
    def __check_type(self, key: str, value: Any) -> None:
        attr_key = self.__key_to_attr_key(key)
        attr_value_types = get_args(get_type_hints(type(self)).get(attr_key))
        if len(attr_value_types) == 0:
            attr_value_types = [get_type_hints(type(self)).get(attr_key)]

        if type(value) not in attr_value_types:
            raise TypeError(f'{CONF_PROFILE_PATH} config item {key} expect {attr_value_types} types, got {type(value)}')

    def conf(self) -> dict[str, Any]:
        return self.__get_conf()

    @property
    def name(self) -> str:
        return self._item_name
    @name.setter
    def name(self, name: str) -> None:
        self.__check_type('name', name)
        if name == '':
            raise ValueError(f'{CONF_PROFILE_PATH} config item name cannot be empty string')
        self._item_name = name
        self.__save_conf()

    @property
    def bio(self) -> str:
        return self._item_bio
    @bio.setter
    def bio(self, bio: str) -> None:
        self.__check_type('bio', bio)
        self._item_bio = bio
        self.__save_conf()



profile = ConfProfile()
