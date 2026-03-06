from fastapi import APIRouter, Body
from ._api import noteapi

router_winpage = APIRouter(prefix='/winpage')

@router_winpage.get('/open_vault')
async def open_vault():
    return await noteapi.open_vault_on_obsidian()
@router_winpage.post('/open_file')
async def open_file(path: str = Body(...)):
    return await noteapi.open_file_on_obsidian(path)
