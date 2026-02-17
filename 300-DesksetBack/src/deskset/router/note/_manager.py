from __future__ import annotations
from typing import TypedDict



# ==== ==== Router ==== ====
from fastapi import APIRouter
from deskset.router._unify import DesksetRepJSON

router_obsidian_manager = APIRouter(
    prefix='/obsidian-manager', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)



# ==== ==== NoteAPI ==== ====
from asyncio import Future, get_event_loop

from deskset.core.config import config
from deskset.core.standard import DesksetError
from deskset.router._unify.access import access, router_access

from fastapi import WebSocket, WebSocketDisconnect, HTTPException

from ._rpc import RpcClient


class API:
    _rpc: RpcClient | None
    _event = dict[str, list[Future]]

    def __init__(self) -> None:
        self._rpc = None
        self._event = {
            'active-leaf-change': [],
            'dataview:metadata-change': []
        }


    # ==== 状态 Status ====

    # 不在线返回 False
    def is_online(self) -> bool:
        if self._rpc is None:
            return False
        return True

    # 不在线抛出 Error
    def check_online(self) -> None:
        if self._rpc is None:
            raise DesksetError(message='Obsidian not online')
        return


    # ==== 事件 Event ====
    # 例：接收 active-leaf-change 触发 self._event_active_leaf_change 事件
    async def _trigger_event(self, response: dict) -> None:
        event = response.get('event', None)
        value = response.get('value', None)
        if event == 'active-leaf-change':
            for future in self._event['active-leaf-change']:  # type: ignore  # Pylance 无法识别键，原因未知
                future.set_result(value)
            self._event['active-leaf-change'] = []  # type: ignore
        if event == 'dataview:metadata-change':
            for future in self._event['dataview:metadata-change']:  # type: ignore
                future.set_result(value)
            self._event['dataview:metadata-change'] = []  # type: ignore

    async def _trigger_offline(self) -> None:
        for _, futures in self._event.items():
            for future in futures:
                if future.done():
                    continue
                future.set_exception(ConnectionError())

    async def event_active_leaf_change(self):
        if not await self.is_online():
            return  # 没有上线，不等待
        future = get_event_loop().create_future()
        self._event['active-leaf-change'].append(future)  # type: ignore
        return await future

    async def event_dataview_metadata_change(self):
        if not await self.is_online():
            return
        future = get_event_loop().create_future()
        self._event['dataview:metadata-change'].append(future)  # type: ignore
        return await future


    # ==== 远程调用 RPC ====

    # --- 仓库 ---
    class VaultStatus(TypedDict):
        note_num: int    # 笔记总数
        attach_num: int  # 附件总数
        useday_num: int  # 使用天数
        tag_num: int     # 标签总数
        task_num: int    # 任务总数
    async def get_vault_status(self) -> API.VaultStatus:
        await self.check_online()
        return await self._rpc.call_remote_procedure('get_vault_status', [])

    class Heat(TypedDict):
        date: str
        number: int
    async def get_heatmap(self, weeknum: int) -> list[API.Heat]:
        await self.check_online()
        return await self._rpc.call_remote_procedure('get_heatmap', [weeknum])

    async def get_active_file(self) -> str:
        await self.check_online()
        return await self._rpc.call_remote_procedure('get_active_file', [])

    # --- 查询建议 ---
    class SuggestFile(TypedDict):
        name: str  # 文件主名
        type: str  # 文件扩展名
        path: str  # 文件相对仓库的路径
    async def suggest_by_switcher(self, query: str) -> list[API.SuggestFile]:
        await self.check_online()
        return await self._rpc.call_remote_procedure('suggest_by_switcher', [query])

    # --- 日记 ---
    async def read_diary(self, dayid: str):
        await self.check_online()
        return await self._rpc.call_remote_procedure('read_diary', [dayid])

    async def list_diarys_in_a_month(self, monthid: str):
        await self.check_online()
        return await self._rpc.call_remote_procedure('list_diarys_in_a_month', [monthid])

    # --- Obsidian 窗口 ---
    async def open_vault(self):
        await self.check_online()
        return await self._rpc.call_remote_procedure('open_vault', [])

    async def open_in_obsidian(self, path: str):
        await self.check_online()
        return await self._rpc.call_remote_procedure('open_in_obsidian', [path])

    # --- 数据分析 ---
    async def filter_frontmatter(self, filter_group: object):
        await self.check_online()
        return await self._rpc.call_remote_procedure('filter_frontmatter', [filter_group])

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
                await api._trigger_event(response)
            if response.get('id'):        # RPC 调用：Deskset > Obsidian > Deskset
                await api._rpc.on_receive(response)
    except WebSocketDisconnect:
        pass

    api._rpc = None
    # 断开 Websocket 连接 + api._rpc = None 之后，触发下线事件
    await api._trigger_offline()


# ==== 登录 ====
  # - [ ] 改进：连接步骤 = http 登录 + websocket 上线/下线
    # 1、http 访问 login：身份认证和初始信息，生成本次 wstoken 及 { wstoken: 初始信息 }
    # 2、websocket 访问 rpc：检查 wstoken 后取回初始信息，创建 RpcClient(ws, init)
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from deskset.router._unify.access import router_access

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
