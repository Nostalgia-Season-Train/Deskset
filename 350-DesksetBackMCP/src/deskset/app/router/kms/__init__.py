from fastapi import APIRouter
# from deskset.app.router._unify import DesksetRepJSON

router_kms = APIRouter(
    prefix='/kms',
)


# ==== Obsidian ====

# RPC 连接
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from deskset.feature.kms.api import RpcClient
from deskset.feature.kms.api import noteapi
@router_kms.websocket('/rpc')
async def rpc(websocket: WebSocket):
    # 检查重复连接
    if not noteapi._rpc == None:
        raise HTTPException(status_code=400, detail='Another NoteAPI is online')

    await websocket.accept('Authorization')  # 前后端都要有 Authorization 子协议，否则无法建立连接

    # 上线 > 轮询接收 > 下线
    noteapi._rpc = RpcClient(websocket)
    await noteapi.trigger_online_event()
    try:
        while True:
            response = await websocket.receive_json()
            if response.get('datetime'):  # 单向事件：Obsidian > Deskset
                await noteapi._trigger_event(response)
            if response.get('id'):        # RPC 调用：Deskset > Obsidian > Deskset
                await noteapi._rpc.on_receive(response)
    except WebSocketDisconnect:
        pass
    await noteapi.trigger_offline_event()
    noteapi._rpc = None

    # 断开 Websocket 连接 + api._rpc = None 之后，触发下线事件
    await noteapi._trigger_offline()

# 上下线事件
@router_kms.get('/is_online')
async def is_online():
    from fastapi.responses import StreamingResponse
    from deskset.feature.kms.api import noteapi
    async def stream():
        try:
            while True:
                if noteapi.is_online():
                    yield 'online'
                else:
                    yield 'offline'
                await noteapi.event_onoffline.wait()
        except Exception:
            pass
        finally:
            return
    return StreamingResponse(stream(), media_type='text/plain')

# 通用
from .common import router_common
router_kms.include_router(router_common)
# 个性资料
from .profile import router_profile
router_kms.include_router(router_profile)
# 日记
from .diary import router_diary
router_kms.include_router(router_diary)
# 任务
from .task import router_task
router_kms.include_router(router_task)
# 数据统计
from .stats import router_stats
router_kms.include_router(router_stats)
# 搜索
from .search import router_search
router_kms.include_router(router_search)
# 命令 Command
from .command import router_command
router_kms.include_router(router_command)
# 窗口页面 Winpage
from .winpage import router_winpage
router_kms.include_router(router_winpage)
# 笔记 Note
from .note import router_note as router_notes
router_kms.include_router(router_notes)
