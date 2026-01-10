""" 标准化：统一请求响应 """

# ==== 身份认证 ====
from .access import router_access
from .access import check_token


# ==== 标准请求 ====

# 日期请求
from .request import DesksetReqDateDay    # 日份 验证 YYYYMMDD 格式
from .request import DesksetReqDateMonth  # 月份 验证 YYYYMM 格式

# 路径、文件或文件夹请求
from .request import DesksetReqPath
from .request import DesksetReqFile
from .request import DesksetReqFolder
from .request import DesksetReqApp

# 网址请求
from .request import DesksetReqURL

# 数字请求
from .request import DesksetReqNumberInt


# ==== 标准响应 ====

# JSON 响应
from .response import DesksetRepJSON

# DesksetError 错误响应
from .response import DesksetErrorRep
