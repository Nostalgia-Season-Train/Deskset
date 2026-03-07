from fastapi import APIRouter, Body
from ._api import noteapi

router_winpage = APIRouter(prefix='/winpage')

@router_winpage.get('/open_vault')
async def open_vault():
    '''打开 Obsidian'''
    return await noteapi.open_vault_on_obsidian()
@router_winpage.post('/open_file')
async def open_file(path: str = Body(...)):
    '''
    在 Obsidian 中打开文件
    参数：path 是基于库的相对路径
    注意：打开笔记需要带上 .md 后缀
    '''
    return await noteapi.open_file_on_obsidian(path)
