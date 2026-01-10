import shutil, os

RUNON = 'res/PyStand/PyStand-v1.1.5+Python-v3.12.10_x86-64.zip'
DIST = 'dist/DesksetBack'  # 构建产物的存放路径

def clear(folder):
    shutil.rmtree(f'./{DIST}/{folder}', ignore_errors=True)
def copy(folder):
    shutil.copytree(f'./{folder}', f'./{DIST}/{folder}')


# ==== 预处理 ====

# 清除上次构建
shutil.rmtree(f'./{DIST}', ignore_errors=True)

# 创建运行环境
import zipfile

os.makedirs(f'./{DIST}', exist_ok=True)

with zipfile.ZipFile(f'./{RUNON}', 'r') as file:
    file.extractall(f'./{DIST}')

# 替换入口文件
# os.remove(f'./{DIST}/DesksetBack.py')  # 仅限 PyStand-v1.1.4+Python-v3.9.7.zip
shutil.copyfile(src=f'./main-prod.py', dst=f'./{DIST}/DesksetBack.py')


# ==== 打包 ====

# 下载依赖
# os.system(f'pip install -r requirements.txt -t ./{DIST}/site-packages')
shutil.copytree('./.venv/Lib/site-packages', f'./{DIST}/site-packages')  # 直接复制 uv 环境

# 构建程序
  # 构建失败的解决方案
  # - Error 1104：避免中文路径
# os.system(f'nuitka --module src/deskset --include-package=deskset --output-dir={DIST}/site-packages --remove-output')
shutil.copytree('./src/deskset', f'./{DIST}/site-packages/deskset')  # nuitka 暂不支持 3.12.10...

# 打包 C/C++ 二进制库
os.makedirs(f'./lib', exist_ok=True)  # 创建 lib 二进制库目录，否则 gcc 报错
os.system('cd src-ffi/DiskActiveTime && build.bat')  # 编译 C/C++ 代码
copy('lib')

# 打包 静态文件
copy('static')

# 打包 演练场 Playground
from urllib.request import urlretrieve
from zipfile import ZipFile
from os import mkdir, remove

urlretrieve('https://github.com/Nostalgia-Season-Train/DesksetPlayground/releases/latest/download/DesksetPlayground.zip', 'DesksetPlayground.zip')

with ZipFile('./DesksetPlayground.zip', 'r') as file:
    mkdir(f'./{DIST}/static/playground')
    file.extractall(f'./{DIST}/static/playground')

remove('./DesksetPlayground.zip')

# 打包 翻译
copy('i18n')

# 打包 示例插件
copy('sample_plugin')


# ==== 压缩 ====
shutil.make_archive('./dist/DesksetBack', 'zip', f'./{DIST}')  # 压缩包主名，压缩格式，压缩路径
