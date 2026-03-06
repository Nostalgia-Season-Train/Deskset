from fastapi import APIRouter, Form
from ._api import noteapi

router_task = APIRouter(prefix='/task', tags=['Note Task'])

@router_task.post('/list')
async def get_all_tasks(path: str = Form()):
    return await noteapi.list_tasks(path)
@router_task.post('/create')
async def create_task(path: str = Form(), text: str = Form(), line: int | None = Form(None)):
    return await noteapi.create_task(path, text, line)
@router_task.post('/edit')
async def edit_task(path: str = Form(), line: int = Form(), newText: str = Form()):
    return await noteapi.edit_task(path, line, newText)
@router_task.post('/toggle')
async def toggle_task(path: str = Form(), line: int = Form()):
    return await noteapi.toggle_task(path, line)
@router_task.post('/delete')
async def delete_task(path: str = Form(), line: int = Form()):
    return await noteapi.delete_task(path, line)
