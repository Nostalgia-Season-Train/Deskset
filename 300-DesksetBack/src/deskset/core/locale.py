# 本地化翻译代码
# 自带本地化的库不用翻译，这里列出：
# arrow
from pathlib import Path
import glob, yaml

from deskset.core.config import config

TRANSLATION_FILE_FOLDER   = './i18n'
TRANSLATION_FILE_FORMAT   = 'yaml'
TRANSLATION_FILE_ENCODING = 'utf-8'


class Translation:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, locale='en'):
        if not hasattr(self._instance, '_is_init'):
            self._is_init = True

            self._data   = {}
            self._locale = locale

        # 遍历所有本地化文件
        translations = glob.glob(str(Path(TRANSLATION_FILE_FOLDER) / f'*.{TRANSLATION_FILE_FORMAT}'))

        # 查找目标选项 locale（目标文件）是否存在
        for item in translations:
            if self._locale == str(Path(item).stem):
                with open(item, 'r', encoding=TRANSLATION_FILE_ENCODING) as f:
                    # 如果文件格式 TRANSLATION_FILE_FORMAT 发生变动，请记得将解析方法一并修改
                    self._data = yaml.safe_load(f)
                    return

        # 没有对应本地化文件，后面添上报错日志

    def translate(self, id):
        # 没有对应翻译时，返回 id 本身，id+ 代表没有翻译
        return self._data.get(id, f' t({id}) ')


translator = Translation(locale=config.language)

# 下划线 _ 用于命名不在循环中使用的变量，换成 _t 代表需要翻译的字符串
_t = translator.translate

# 测试：
# locale='language'
# /src/i18n/language.yaml 添加 helloworld: Hello World In Language
# print(_t('helloworld'))
