from fastapi import APIRouter, Body
from ._api import noteapi

router_winpage = APIRouter(prefix='/winpage')

@router_winpage.get('/open_vault_on_obsidian')
async def open_vault_on_obsidian():
    return await noteapi.open_vault_on_obsidian()
@router_winpage.post('/open_file_on_obsidian')
async def open_file_on_obsidian(path: str = Body(...)):
    return await noteapi.open_file_on_obsidian(path)
