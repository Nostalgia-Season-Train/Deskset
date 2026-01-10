from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from ._manager import api as noteapi

router_common = APIRouter(prefix='/common')

@router_common.get('/active-file')
async def get_active_file():
    async def stream():
        # 检查是否上线，流式响应无法处理 DesksetError
        if noteapi.is_offline:
            return
        # 初始化
        yield await noteapi.get_active_file()
        # 轮询等待 active-leaf-change 事件
        while True:
            await noteapi.event_active_leaf_change()
            if noteapi.is_offline:
                break  # 判断 event_active_leaf_change 是否由下线触发
            yield await noteapi.get_active_file()
        return

    return StreamingResponse(stream(), media_type='text/plain')

@router_common.get('/open-vault')
async def open_vault():
    return await noteapi.open_vault()

@router_common.get('/open-in-obsidian')
async def open_in_obsidian(path: str = Query()):
    return await noteapi.open_in_obsidian(path)
