from __future__ import annotations
from typing import TypedDict

from pathlib import Path

from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from deskset.router.unify import DesksetRepJSON
from deskset.router.unify import DesksetReqFolder

router_obsidian_manager = APIRouter(
    prefix='/obsidian-manager', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)

from httpx import AsyncClient
from deskset.core.config import config
from deskset.router.unify.access import access

from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from deskset.router.unify.access import access
from ._noteapi import noteapi

# - [ ] 临时：RPC 测试
from asyncio import Event
from asyncer import asyncify

from deskset.core.log import logging
from deskset.core.standard import DesksetError
from deskset.router.unify.access import access, router_access

from ._rpc import RpcClient

class API:
    _rpc: RpcClient | None
    _event_active_leaf_change: Event

    def __init__(self) -> None:
        self._rpc = None
        self._event_active_leaf_change = Event()

    # --- 状态 ---
    @property
    def is_offline(self) -> bool:
        return self._rpc is None

    # --- 事件 ---
    # 例：接收 active-leaf-change 触发 self._event_active_leaf_change 事件
    async def trigger_event(self, response: dict) -> None:
        name = response.get('event', None)
        if not isinstance(name, str):
            await asyncify(logging.error)(f'Receive Obsidian event: non-string name {name!r}')
            return

        self_name = f'_event_{name.replace('-', '_')}'
        self_event = self.__dict__.get(self_name)
        if not isinstance(self_event, Event):
            await asyncify(logging.error)(f'Receive Obsidian event: self.{self_name} not a Event {self_event!r}')
            return
        self_event.set()
        self_event.clear()

    async def trigger_all_event(self) -> None:
        for attr_key, attr_value in list(self.__dict__.items()):
            if not attr_key.startswith('_event_'):
                continue
            if not isinstance(attr_value, Event):
                continue
            attr_value.set()
            attr_value.clear()

    async def event_active_leaf_change(self):
        if self._rpc is None:
            return  # 没有上线，不等待
        return await self._event_active_leaf_change.wait()

    # --- RPC ---
    async def get_note_number(self) -> int:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('get_note_number', [])

    async def get_attachment_number(self) -> int:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('get_attachment_number', [])

    async def get_useday_number(self) -> int:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('get_useday_number', [])

    class Heat(TypedDict):
        date: str
        number: int

    async def get_heatmap(self, weeknum: int) -> list[API.Heat]:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('get_heatmap', [weeknum])

    async def get_active_file(self) -> str:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('get_active_file', [])

    class SuggestFile(TypedDict):
        name: str  # 文件主名
        type: str  # 文件扩展名
        path: str  # 文件相对仓库的路径

    async def suggest_by_switcher(self, query: str) -> list[API.SuggestFile]:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('suggest_by_switcher', [query])


    # ==== 日记 ====
    async def read_today_diary(self):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('read_today_diary', [])

    async def read_diary(self, dayid: str):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('read_diary', [dayid])

    async def list_diarys_in_a_month(self, monthid: str):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('list_diarys_in_a_month', [monthid])


    # ==== Obsidian 窗口 ====
    async def open_vault(self):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('open_vault', [])

    async def open_in_obsidian(self, path: str):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('open_in_obsidian', [path])


    # ==== 数据分析 ====
    async def filter_frontmatter(self, filter_group: object):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('filter_frontmatter', [filter_group])

    async def filter_frontmatter_number(self, filter_group: object):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('filter_frontmatter_number', [filter_group])

    async def filter_and_random_open_in_obsidian(self, filter_group: object):
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return await self._rpc.call_remote_procedure('filter_and_random_open_in_obsidian', [filter_group])

api = API()

# router_obsidian_manager 注入 check_token 引发以下异常
  # OAuth2PasswordBearer.__call__() missing 1 required positional argument: 'request'
@router_access.websocket('/note/obsidian/rpc')
async def rpc(websocket: WebSocket):
    async def is_authorized(subprotocols: list[str]):
        if len(subprotocols) != 2:
            return False
        if subprotocols[0] != 'Authorization':
            return False
        if subprotocols[1] != f'bearer-{access.notetoken}':
            return False
        return True

    # 检查 notetoken
    if not await is_authorized(websocket.scope['subprotocols']):
        await access.add_fail_time_async()
        raise HTTPException(status_code=400, detail='Invalid notetoken')

    # 检查重复连接
    if not api._rpc == None:
        raise HTTPException(status_code=400, detail='Another NoteAPI is online')

    await websocket.accept('Authorization')  # 前后端都要有 Authorization 子协议，否则无法建立连接

    # 上线 > 轮询接收 > 下线
    api._rpc = RpcClient(websocket)

    try:
        while True:
            response = await websocket.receive_json()
            if response.get('datetime'):  # 单向事件：Obsidian > Deskset
                await api.trigger_event(response)
            if response.get('id'):        # RPC 调用：Deskset > Obsidian > Deskset
                await api._rpc.on_receive(response)
    except WebSocketDisconnect:
        pass

    api._rpc = None
    # 断开 Websocket 连接 + api._rpc = None 之后，触发所有事件
      # 代替 event_offline 下线事件
      # 这样就不需要 asyncio.wait 和 asyncio.create_task 同时监听两个事件
      # 只等 event_{name} 触发后，判断一次 is_offline 状态即可下线
    await api.trigger_all_event()


# ==== 登录 ====
  # - [ ] 改进：连接步骤 = http 登录 + websocket 上线/下线
    # 1、http 访问 login：身份认证和初始信息，生成本次 wstoken 及 { wstoken: 初始信息 }
    # 2、websocket 访问 rpc：检查 wstoken 后取回初始信息，创建 RpcClient(ws, init)
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from deskset.router.unify.access import router_access

@router_access.post('/note/obsidian/login')
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends()
):
    # Sec- 开头的请求标头，无法从浏览器发出
      # 目标：确保请求来源 NodeJS，而不是浏览器
      # 原因：阻止恶意网站利用浏览器进行 CSRF 攻击（私有网络攻击）
    if request.headers.get('Sec-Deskset-NoteAPI', None) != 'PNA':
        from deskset.core.log import logging
        logging.error(f'Website {request.headers.get('Referer')} try to login Deskset')
        raise HTTPException(status_code=400, detail='Invalid client')

    # 输入和输出：username、password，access_token、token_type 都不需要自己指定键名
    if form.username != config.username:
        raise HTTPException(status_code=400, detail='Invalid username')
    if form.password != config.password:
        raise HTTPException(status_code=400, detail='Invalid password')
    if not api._rpc is None:
        raise HTTPException(status_code=400, detail='Another NoteAPI is online')

    return access.notetoken
