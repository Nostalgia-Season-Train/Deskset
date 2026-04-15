# ==== 验证路径、文件或文件夹（绝对路径） ====
import os

class DesksetReqPath(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_path(cls, v: str) -> str:
        if os.path.isfile(v) != True and os.path.isdir(v) != True:
            raise DesksetError(message=f'错误！路径 {v} 不存在！')
        return v

class DesksetReqFile(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_file(cls, v: str) -> str:
        if os.path.isfile(v) != True:
            raise DesksetError(message=f'错误！文件 {v} 不存在！')
        return v

class DesksetReqFolder(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_folder(cls, v: str) -> str:
        if not os.path.isdir(v):
            raise DesksetError(message=f'错误！{v} 不是文件夹！')
        return v

class DesksetReqApp(BaseModel):
    path: str

    @field_validator('path')
    @classmethod
    def check_app(cls, v: str) -> str:
        # Linux 下可执行文件没有后缀，需要其他检查手段
        if os.path.isfile(v) != True or os.path.splitext(v)[1] != '.exe':
            raise DesksetError(message=f'错误！{v} 不是应用！')
        return v


# ==== 验证网址 ====
from urllib.parse import urlparse

class DesksetReqURL(BaseModel):
    url: str

    @field_validator('url')
    @classmethod
    def check_folder(cls, v: str) -> str:
        parsed_url = urlparse(v)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        # 检查网络协议
        if scheme != 'http' and scheme != 'https':
            raise DesksetError(message=f'错误！网络协议 {scheme} 无效！')
        # 检查网络位置
        if not netloc:
            raise DesksetError(message=f'错误！网络位置 {netloc} 无效！')
        return v


# ==== 验证数字 ====
class DesksetReqNumberInt(BaseModel):
    num: int

    @field_validator('num')
    @classmethod
    def check_num(cls, v: int) -> int:  # Pydantic 自动验证 int 类型
        return v
