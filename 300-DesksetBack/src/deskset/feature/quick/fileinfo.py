import subprocess
from icoextract import IconExtractor

from ._check import check_file

# 返回快捷方式 .lnk 指向文件
def get_lnk_target(path: str) -> str:
    check_file(path, extn='.lnk')
    command = f'powershell -command "$sh = New-Object -ComObject WScript.Shell; $shortcut = $sh.CreateShortcut(\'{path}\'); $shortcut.TargetPath;"'
    return subprocess.check_output(command, shell=True, text=True).strip()  # strip 去掉结果自带的换行符

# 返回可执行文件 .exe 图标
def get_exe_icon(path: str) -> bytes:
    check_file(path, extn='.exe')
    return IconExtractor(path).get_icon(num=0).getvalue()  # getvalue 从字节流获取字节数据
