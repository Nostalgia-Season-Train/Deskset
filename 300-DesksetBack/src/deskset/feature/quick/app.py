import subprocess

def open_folder_by_vscode(path: str) -> None:
    # 虽然已经添加 vscode 安装目录到 PATH，但不加 shell=True 仍会报错
    subprocess.run(['code', path], shell=True)
