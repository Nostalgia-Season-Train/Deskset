from __future__ import annotations
from typing import Any, TypedDict



# ==== ==== 异步事件迭代器 ==== ====
from asyncio import Queue

class AsyncEventIterator:
    def __init__(self) -> None:
        self._queue: Queue[Any] = Queue()
        self._sentinel: object = object()

    def __aiter__(self) -> AsyncEventIterator:
        return self

    async def __anext__(self) -> Any:
        event = await self._queue.get()
        if event is self._sentinel:
            raise StopAsyncIteration
        return event

    async def send(self, event: Any) -> None:
        await self._queue.put(event)

    # 主动关闭迭代器，适用于服务器退出的情况
    async def close(self) -> None:
        await self._queue.put(self._sentinel)



# ==== ==== NoteAPI ==== ====
from asyncio import Future, get_event_loop
from asyncio import Event

from deskset.core.config import config
from deskset.core.standard import DesksetError
from deskset.router._unify.access import access, router_access

from fastapi import WebSocket, WebSocketDisconnect, HTTPException

from ._rpc import RpcClient


class NoteAPI:
    _rpc: RpcClient | None
    _event: dict[str, list[Future]]
    _event_iters: set[AsyncEventIterator]  # 当作数组使用，复数命名

    def __init__(self) -> None:
        self._rpc = None
        self._event = {
            'active-leaf-change': [],
            'dataview:metadata-change': []
        }
        self.event_onoffline = Event()
        self._event_iters = set()


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

    # 触发上下线事件
    async def trigger_onoffline_event(self) -> None:
        self.event_onoffline.set()
        self.event_onoffline.clear()

    async def trigger_online_event(self)-> None:
        await self._send({ 'event': 'online', 'value': True })

    async def trigger_offline_event(self)-> None:
        await self._send({ 'event': 'offline', 'value': False })


    # ==== 发布/订阅事件流（事件迭代器） ====
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def subscribe(self):
        event_iter = AsyncEventIterator()
        # - [ ] 架构待讨论：初始化时，放入上下线事件，方便 stream 直接从 for 开始轮询
        if self.is_online():
            await event_iter.send({ 'event': 'online', 'value': True })
        else:
            await event_iter.send({ 'event': 'offline', 'value': False })
        self._event_iters.add(event_iter)
        try:
            yield event_iter
        finally:
            self._event_iters.remove(event_iter)

    async def _send(self, event):
        for event_iter in self._event_iters:
            await event_iter.send(event)


    # ==== 事件 Event ====
    # 例：接收 active-leaf-change 触发 self._event_active_leaf_change 事件
    async def _trigger_event(self, response: dict) -> None:
        event = response.get('event', None)
        value = response.get('value', None)
        await self._send({ 'event': event, 'value': value })
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
        if not self.is_online():
            return  # 没有上线，不等待
        future = get_event_loop().create_future()
        self._event['active-leaf-change'].append(future)  # type: ignore
        return await future

    async def event_dataview_metadata_change(self):
        if not self.is_online():
            return
        future = get_event_loop().create_future()
        self._event['dataview:metadata-change'].append(future)  # type: ignore
        return await future


    # ==== 远程调用 RPC ====

    # --- 仓库 ---
    async def get_vault_metainfo(self):
        self.check_online()
        return await self._rpc.call_remote_procedure('get_vault_metainfo', [])  # type: ignore
    class VaultStatus(TypedDict):
        note_num: int    # 笔记总数
        attach_num: int  # 附件总数
        useday_num: int  # 使用天数
        tag_num: int     # 标签总数
        task_num: int    # 任务总数
    async def get_vault_status(self) -> NoteAPI.VaultStatus:
        self.check_online()
        return await self._rpc.call_remote_procedure('get_vault_status', [])  # type: ignore

    async def get_heatmap(self, start_day, end_day) -> dict[str, int]:
        self.check_online()
        return await self._rpc.call_remote_procedure('get_heatmap', [start_day, end_day])  # type: ignore

    async def get_active_file(self) -> str:
        self.check_online()
        return await self._rpc.call_remote_procedure('get_active_file', [])  # type: ignore

    # --- 查询建议 ---
    class SuggestFile(TypedDict):
        name: str  # 文件主名
        type: str  # 文件扩展名
        path: str  # 文件相对仓库的路径
    async def suggest_by_switcher(self, query: str) -> list[NoteAPI.SuggestFile]:
        self.check_online()
        return await self._rpc.call_remote_procedure('suggest_by_switcher', [query])  # type: ignore

    # --- 数据分析 ---
    async def filter_frontmatter(self, filter_group: object):
        self.check_online()
        return await self._rpc.call_remote_procedure('filter_frontmatter', [filter_group])  # type: ignore

    # --- 日记 Diary ---
    class DiarySetting(TypedDict):
        format: str    # 日记目录/日记主名的日期格式（比如 YYYY年/MM月/YYYY年MM月DD日-dddd）
        folder: str    # 日记父文件夹
        template: str  # 日记模板
    async def get_diary_setting(self) -> NoteAPI.DiarySetting:
        self.check_online()
        return await self._rpc.call_remote_procedure('get_diary_setting', [])  # type: ignore
    async def list_diaryprops_in_month(self, month: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('list_diaryprops_in_month', [month])  # type: ignore
    async def read_diary(self, day: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('read_diary', [day])  # type: ignore
    async def create_diary(self, day: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('create_diary', [day])  # type: ignore
    async def edit_diary(self, day: str, newText: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('edit_diary', [day, newText])  # type: ignore
    async def insert_diary(self, day: str, line: int | None, insertData: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('insert_diary', [day, line, insertData])  # type: ignore
    async def write_diary(self, day: str, newData: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('write_diary', [day, newData])  # type: ignore
    async def delete_diary(self, day: str):
        self.check_online()
        return await self._rpc.call_remote_procedure('delete_diary', [day])  # type: ignore

    # --- 任务 Task ---
    class Task(TypedDict):
        # - [x] 这是一个任务
        line: int    # 任务在第 line 行
        status: str  # 任务状态 'x'
        text: str    # 任务文本 '这是一个任务'
    async def list_tasks(self, path: str) -> NoteAPI.Task:
        self.check_online()
        return await self._rpc.call_remote_procedure('list_tasks', [path])  # type: ignore
    async def create_task(
        self,
        path: str,
        line: int | None,
        status: str | None,
        text: str | None
    ):
        self.check_online()
        return await self._rpc.call_remote_procedure('create_task', [path, line, status, text])  # type: ignore
    async def edit_task(
        self,
        path: str,
        line: int,
        newStatus: str | None,
        newText: str | None
    ):
        self.check_online()
        return await self._rpc.call_remote_procedure('edit_task', [path, line, newStatus, newText])  # type: ignore
    async def toggle_task(self, path: str, line: int):
        self.check_online()
        return await self._rpc.call_remote_procedure('toggle_task', [path, line])  # type: ignore
    async def delete_task(self, path: str, line: int):
        self.check_online()
        return await self._rpc.call_remote_procedure('delete_task', [path, line])  # type: ignore

    # --- 命令 Command ---
    class Command(TypedDict):
        id: str    # 命令 ID
        name: str  # 命令名称
    async def list_commands(self) -> NoteAPI.Command:
        self.check_online()
        return await self._rpc.call_remote_procedure('list_commands', [])  # type: ignore
    async def execute_command(self, id: str) -> Any:
        self.check_online()
        return await self._rpc.call_remote_procedure('execute_command', [id])  # type: ignore

    # --- 窗口页面 Winpage ---
    async def open_on_obsidian(self) -> bool:
        self.check_online()
        return await self._rpc.call_remote_procedure('open_on_obsidian', [])  # type: ignore
    async def open_file_on_obsidian(self, path: str) -> bool:
        self.check_online()
        return await self._rpc.call_remote_procedure('open_file_on_obsidian', [path])  # type: ignore


noteapi = NoteAPI()



# ==== ==== 端点 Endpoint ==== ====
from deskset.router._unify.access import router_access


# ==== 全双工通信 Websocket ====
  # websocket 注入 check_token 会引发以下异常
  # OAuth2PasswordBearer.__call__() missing 1 required positional argument: 'request'
  # 2026/02/25：不用管 ws_handler 弃用警告 DeprecationWarning
    # 相关讨论：https://github.com/Kludex/uvicorn/discussions/2476
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


# ==== 登录 Access ====
  # - [ ] 改进：连接步骤 = http 登录 + websocket 上线/下线
    # 1、http 访问 login：身份认证和初始信息，生成本次 wstoken 及 { wstoken: 初始信息 }
    # 2、websocket 访问 rpc：检查 wstoken 后取回初始信息，创建 RpcClient(ws, init)
from deskset.core.config import DESKSET_NOTEAPI_VERSION
from fastapi import Request, Form

@router_access.post('/note/obsidian/login')
def login(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    version: str = Form()
):
    # Sec- 开头的请求标头，无法从浏览器发出
      # 目标：确保请求来源 NodeJS，而不是浏览器
      # 原因：阻止恶意网站利用浏览器进行 CSRF 攻击（私有网络攻击）
    if request.headers.get('Sec-Deskset-NoteAPI', None) != 'PNA':
        from deskset.core.log import logging
        logging.error(f'Website {request.headers.get('Referer')} try to login Deskset')
        raise HTTPException(status_code=400, detail='Invalid client')

    # 输入和输出：username、password，access_token、token_type 都不需要自己指定键名
    if username != config.username:
        raise HTTPException(status_code=400, detail='Invalid username')
    if password != config.password:
        raise HTTPException(status_code=400, detail='Invalid password')
    if version != DESKSET_NOTEAPI_VERSION:
        raise HTTPException(status_code=400, detail=f'Require NoteAPI {DESKSET_NOTEAPI_VERSION} version')
    if not noteapi._rpc is None:
        raise HTTPException(status_code=400, detail='Another NoteAPI is online')

    return access.notetoken
