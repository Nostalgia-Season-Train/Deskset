import os
from pathlib import Path
from send2trash import send2trash, TrashPermissionError

from deskset.core.locale import _t
from deskset.core.config import config
from deskset.core.standard import DesksetError

ERR_PATH_NOT_EXIST     = DesksetError(code=2000, message=_t('路径 {} 不存在'))
ERR_FILE_NOT_EXIST     = DesksetError(code=2001, message=_t('根路径 {} 下文件 {} 不存在'))
ERR_FILE_ALREADY_EXIST = DesksetError(code=2002, message=_t('根路径 {} 下文件 {} 已存在'))
ERR_NEED_UPDATE = DesksetError(code=2003, message=_t('根路径 {} 内存与硬盘中条目不一致，需要更新'))
ERR_CANT_FIND_NOR_CREATE_TRASH = DesksetError(code=2004, message=_t('根路径 {} 不能找到或创建回收站'))


# 根路径（根目录）
# 作用：将一个路径（目录）视作根路径（根目录）进行操作
class RootPath:
    def __init__(self, root: str, excludes: list[str] = []) -> None:
        self._encoding = config.encoding

        if not os.path.isdir(root):
            raise ERR_PATH_NOT_EXIST.insert(root)

        self._root = Path(root)
        self._folders: list[Path] = []
        self._files:   list[dict] = []
        self._excludes = excludes  # 需要排除的条目

        self.update()

    def __get_entrys(self, relpath: Path) -> tuple[list, list]:
        folders: list[Path] = []
        files:   list[dict] = []

        with os.scandir(self._root / relpath) as entrys:
            for entry in entrys:
                if entry.name in self._excludes:
                    continue
                if entry.is_dir():
                    folders.append(relpath / entry.name)
                    # 子条目下的文件夹和文件
                    folders_in_entry, files_in_entry = self.__get_entrys(relpath / entry.name)
                    files.extend(files_in_entry)
                    folders.extend(folders_in_entry)
                else:
                    meta = entry.stat()
                    files.append({
                        'relpath': relpath / entry.name,
                        'name': entry.name,
                        'size': meta.st_size,
                        'ctime': meta.st_ctime,
                        'mtime': meta.st_mtime
                    })

        return folders, files

    def update(self) -> None:
        folders, files = self.__get_entrys(Path(''))

        self._folders = folders
        self._files = files

    def get_folders(self) -> list[str]:
        return list(map(str, self._folders))

    def get_files(self) -> list[dict]:
        return self._files

    def get_files_relpath(self) -> list[str]:
        return [str(file['relpath']) for file in self._files]

    def get_abspath(self, relpath: str) -> str:
        for file in self._files:
            if Path(relpath) == file['relpath']:
                return str(self._root / relpath)
        raise ERR_FILE_NOT_EXIST.insert(self._root, relpath)

    # 直接计算绝对路径，不去检查文件是否存在
    def calc_abspath(self, relpath: str) -> str:
        return str(self._root / relpath)

    # 去掉创建和删除文件，以后用 SQLite 管理根目录
