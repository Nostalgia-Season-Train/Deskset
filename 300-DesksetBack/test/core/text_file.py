import difflib
from typing import Callable, Any

from deskset.core.config import config
from deskset.core.locale import _t
from deskset.core.standard import DesksetError

ERR_FILE_NOT_FIND       = DesksetError(code=1002, message=_t('打开失败，文件不存在'))
ERR_FILE_CHANGE_OUTSIDE = DesksetError(code=1003, message=_t('文件被外部修改'))
ERR_FILE_DELETE_OUTSIDE = DesksetError(code=1004, message=_t('文件被外部删除'))


# 撤销/重做管理器
class DoManager:
    def __init__(self) -> None:
        self._history = {
            'undo': [],
            'redo': []
        }
        self._is_undo_or_redo = None

    # 注册撤销/重做事件，以供撤销/重做时调用
    def register(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        if self._is_undo_or_redo is None:
            self._history['undo'].append((func, args, kwargs))
            self._history['redo'] = []
        else:
            kind = 'redo' if self._is_undo_or_redo == 'undo' else 'undo'
            self._history[kind].append((func, args, kwargs))

        self._is_undo_or_redo = None

    def undo(self) -> None:
        func, args, kwargs = self._history['undo'].pop()
        self._is_undo_or_redo = 'undo'
        func(*args, **kwargs)

    def redo(self) -> None:
        func, args, kwargs = self._history['redo'].pop()
        self._is_undo_or_redo = 'redo'
        func(*args, **kwargs)


# 文本
class Text:
    def __init__(self, text: list[str]) -> None:
        self._text = text
        self._do_manager = DoManager()

    # 生成编辑码
    def _generate_edcodes(self, old_text: list[str], new_text: list[str]) -> list[tuple[str, int, int, list[str]]]:
        edcodes: list[tuple[str, int, int, list[str]]] = []

        diff_sequence = difflib.SequenceMatcher(None, old_text, new_text)
        for tag, i1, i2, j1, j2 in diff_sequence.get_opcodes():
            if   tag == 'equal'  : edcodes.append(('equal'  , i1, i2, ['']))
            elif tag == 'replace': edcodes.append(('replace', i1, i2, new_text[j1:j2]))
            elif tag == 'delete' : edcodes.append(('delete' , i1, i2, ['']))
            elif tag == 'insert' : edcodes.append(('insert' , i1, i2, new_text[j1:j2]))

        return edcodes

    # 通过编辑码更新文本
    def _edit(self, edcodes: list[tuple[str, int, int, list[str]]]) -> None:
        # 编辑后文本 text；当前文本 self._text；编辑码 edcodes
        # text = self._text + edcodes
        text: list[str] = []
        for tag, i1, i2, block in edcodes:
            if   tag == 'equal'  : text.extend(self._text[i1:i2])
            elif tag == 'replace': text.extend(block)
            elif tag == 'delete' : pass
            elif tag == 'insert' : text.extend(block)

        # 注册本次编辑的逆
        # inverse_edcodes = text -> self._text
        self._do_manager.register(self._edit, self._generate_edcodes(text, self._text))

        # 更新文本
        self._text = text

    def undo(self) -> None:
        self._do_manager.undo()

    def redo(self) -> None:
        self._do_manager.redo()

    def get(self) -> list[str]:
        return self._text

    def set(self, text: list[str]) -> None:
        # 如果出现问题，换成下列代码以保证每次修改都由 _edit 完成
        # self._edit(self._edit_codes(text, self._text))
        self._do_manager.register(self._edit, self._generate_edcodes(text, self._text))
        self._text = text


# 文本文件
# 作用：处理文本文件，看作文件编辑页面（打开后编辑）
# - 1、打开关闭：打开文件 => 读写文件 => 关闭文件
# - 2、同步读写：确保在读写时，硬盘与内存中的数据一致
# - 3、撤销重做：编辑历史
# 注：创建、删除功能，将由路径相关模块提供
class TextFile:
    def __init__(self, path: str, encode: str = config.encoding) -> None:
        try:
            with open(path, 'r', encoding=encode) as file:
                self._path = path
                self._encode = encode
                self._content = Text(file.readlines())
        except FileNotFoundError:
            raise ERR_FILE_NOT_FIND

    def undo(self) -> None:
        self._content.undo()

    def redo(self) -> None:
        self._content.redo()

    # 检查并同步外部更改
    # - 外部更改：不受 TextFile 控制文件更改。比如通过 vsc 修改文件
    def _check_and_sync_outside_change(self) -> bool:
        try:
            with open(self._path, 'r', encoding=self._encode) as file:
                text = file.readlines()
                if difflib.SequenceMatcher(None, self._content.get(), text).ratio() != 1:
                    self._content.set(text)
                    return True
                else:
                    return False
        except FileNotFoundError:
            raise ERR_FILE_DELETE_OUTSIDE

    def path(self) -> str:
        return self._path

    def encode(self) -> str:
        return self._encode

    def read(self) -> list[str]:
        self._check_and_sync_outside_change()

        return self._content.get()

    def write(self, content: list[str]) -> None:
        if self._check_and_sync_outside_change():
            raise ERR_FILE_CHANGE_OUTSIDE

        try:
            # 确保在写入文件成功的基础上写入内存：先写入文件，再写入内存
            with open(self._path, 'r+', encoding=self._encode) as file:
                file.write(self._content.get())
                self._content.set(content)
        except FileNotFoundError:
            raise ERR_FILE_DELETE_OUTSIDE


# test_textfile = TextFile('')

# while True:
#     get_input = input()
#     if   get_input == '1':
#         print('检查更改：')
#         test_textfile._check_outside_change()
#     elif get_input == '2':
#         print('当前文本：')
#         print(test_textfile._content.get())
#     elif get_input == 'u':
#         print('撤销：')
#         test_textfile.undo()
#     elif get_input == 'r':
#         print('重做：')
#         test_textfile.redo()
#     else:
#         pass
