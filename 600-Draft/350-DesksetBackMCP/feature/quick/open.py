import subprocess, os, sys
import webbrowser
from pathlib import Path

import platform

SYSTEM = platform.system()


# 默认打开
def open_default(path: str) -> None:
    if SYSTEM == 'Windows':
        if Path(path).suffix == '.exe':  # 程序用 open_app_by_path 打开
            open_app_by_path(path)
        else:                            # 其他文件用 默认应用 打开
            os.startfile(path)  # 也能打开文件夹

def open_app_by_path(appPath: str):
    # 1、需要设置应用工作路径 cwd = 应用所在目录，否则某些应用无法运行
    # 2、如果应用随程序结束而关闭，这是 vsc 的原因，用命令行运行 .py 即可
    appCwd = Path(appPath).parent
    subprocess.Popen(appPath, cwd=appCwd)

def open_web_by_url(webUrl: str):
    webbrowser.open_new_tab(webUrl)

# 打开回收站
def open_recycle():
    if SYSTEM == 'Windows':
        # subprocess.Popen('explorer shell:RecycleBinFolder', shell=True)  # 回收站在 Tauri 置底窗口下打开...
        # subprocess.Popen('start shell:RecycleBinFolder', shell=True)  # 会使已经打开的回收站消失
        os.system('start shell:RecycleBinFolder')  # 打包后运行会弹出 CMD 窗口

# 执行 Python 脚本
def execute_script(name: str):
    current_python = sys.executable  # 当前 Python 解释器路径
    # - [ ] 改为 importlib 执行
    # - [ ] 加入错误处理
    subprocess.Popen([current_python, f'./scripts/{name}.py'])
