from fastapi import APIRouter, Body
from ._api import noteapi

router_command = APIRouter(prefix='/command')

@router_command.get('/list')
async def list():
    return await noteapi.list_commands()
@router_command.post('/execute')
async def execute(id: str = Body(...)):
    return await noteapi.execute_command(id)
