import mimetypes
from fastapi import APIRouter
from fastapi.responses import FileResponse

from deskset.core.root_path import RootPath

router_cloud = APIRouter(prefix='/v0/cloud', tags=['在线文件'])

# folder：根文件夹？名称
# relpath：根文件夹下相对路径
@router_cloud.get('/{folder}/{relpath:path}')
async def get_date(folder: str, relpath: str):
    root = RootPath('folder_abspath')  # 开发中

    file_path = root.get_abspath(relpath)
    file_type, _ = mimetypes.guess_type(file_path)  # 判断文件类型

    return FileResponse(path=file_path, media_type=file_type)
