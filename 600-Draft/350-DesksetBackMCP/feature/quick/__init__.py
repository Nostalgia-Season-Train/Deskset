# ==== 快速启动 ====

# 打开
from .open import open_default      # 效果等于鼠标左键文件
from .open import open_app_by_path  # 打开程序
from .open import open_web_by_url   # 打开网页
from .open import open_recycle      # 打开回收站


# 应用行为
from .app import open_folder_by_vscode  # 通过 vscode 打开文件夹

# 文件信息
from .fileinfo import get_lnk_target
from .fileinfo import get_exe_icon
