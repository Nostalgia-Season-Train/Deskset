from typing import Optional

from pathlib import Path

# 检查文件、文件后缀
  # - [ ] 后面换成 DesksetException
def check_file(path: str, extn: Optional[str] = None) -> None:
    if Path(path).is_file() == False:
        raise FileNotFoundError
    if extn != None and path.endswith(extn) == False:
        raise TypeError
