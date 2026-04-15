from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from deskset.feature.kms.api import noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/metainfo')
async def get_metainfo():
    return await noteapi.get_vault_metainfo()

@router_common.get('/active-file')
async def get_active_file():
    return await noteapi.get_active_file()

@router_common.get('/active-file/stream')
async def get_active_file_stream():
    async def stream():
        async with noteapi.subscribe() as event_stream:
            async for event in event_stream:
                if event.get('event') == 'online':
                    yield await noteapi.get_active_file()
                if event.get('event') == 'active-leaf-change':
                    yield await noteapi.get_active_file()
                if event.get('event') == 'offline':
                    yield ''  # 下线：返回占位符
    return StreamingResponse(stream(), media_type='text/plain')
