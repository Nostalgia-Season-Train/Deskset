from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from ._manager import api as noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/active-file')
async def get_active_file():
    async def stream():
        try:
            while True:
                yield await noteapi.get_active_file()
                await noteapi.event_active_leaf_change()
        except ConnectionError:
            pass
        finally:
            return

    if not await noteapi.is_online():
        return
    return StreamingResponse(stream(), media_type='text/plain')

@router_common.get('/open-vault')
async def open_vault():
    return await noteapi.open_vault()

@router_common.get('/open-in-obsidian')
async def open_in_obsidian(path: str = Query()):
    return await noteapi.open_in_obsidian(path)
