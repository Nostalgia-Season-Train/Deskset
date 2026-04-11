from typing import Optional
from asyncio import Event

from httpx import AsyncClient, Response
from httpx import ConnectError
from fastapi import WebSocket
from asyncer import asyncify

from deskset.core.log import logging
from deskset.core.standard import DesksetError

from ._validate import Setting
from ._validate import Greet

logging.getLogger('httpx').setLevel(logging.ERROR)  # 禁止 httpx 输出 ERROR 级别以下的日志


class NoteAPI:
    def __init__(self) -> None:
        self._is_online: bool = False
        self._address: Optional[str] = None
        self._token: Optional[str] = None

        # http 或 websocket 通信
        self._httpx: Optional[AsyncClient] = None
        self._websocket: WebSocket | None

        # 仓库信息
        self._vault: Optional[str] = None  # 仓库绝对路径
        self._setting: Setting | None

        # 上线下线事件
        self.online_status = Event()
        self.offline_status = Event()

        self.online_status.clear()
        self.offline_status.set()

    async def set_online(self, address: str, token: str, vault: str, setting: Setting, websocket: WebSocket) -> str:
        if self._is_online == True:
            raise DesksetError(message='NoteAPI in Back is online')

        self._is_online = True
        self._address = address
        self._token = token

        self._httpx = AsyncClient(base_url=f'http://{address}', headers={ 'Authorization': f'Bearer {token}' })
        self._websocket = websocket

        self._vault = vault
        self._setting = await asyncify(Setting.model_validate)(setting)

        self.online_status.set()
        self.offline_status.clear()

        logging.info(f'NoteAPI online, address is {address} and token is {token}')

        return 'Back recevie NoteAPI online'

    async def set_offline(self, address: str, token: str) -> str:
        if self._is_online == False:
            raise DesksetError(message='NoteAPI in Back is offline')
        if self._address != address or self._token != token:
            raise DesksetError(message='Different address or token, Not the same connect')

        self._is_online = False
        self._address = None
        self._token = None

        self._httpx = None
        self._websocket = None

        self._vault = None
        self._setting = None

        self.online_status.clear()
        self.offline_status.set()

        logging.info(f'NoteAPI offline, address is {address} and token is {token}')

        return 'Back recevie NoteAPI offline'

    async def _check_online(self) -> None:
        if self._is_online != True:  # _is_online = True 但 _httpx = None 在预期之外，这里不判断 _httpx 让其自然抛出异常
            raise DesksetError(message='没有打开 Obsidian 仓库')

    async def _check_response(self, response: Response) -> None:
        if response.status_code == 200:  # 200 OK 一切正常
            return
        else:
            raise DesksetError(message=response.text)

    # 在 Obsidian 中打开笔记
      # notepath 以仓库为根目录，笔记在仓库下的相对路径
      # 注：有时 Obsidian 窗口不会跳到前台，原因未知...
        # 2025/06/08：经过测试，Obsidian 处于最小化窗口状态，才会弹出到前台
    async def open(self, notepath = None) -> None:
        await self._check_online()

        from webbrowser import open
        if notepath is None:
            await asyncify(open)(f'obsidian://open?path={ self._vault }')
        else:
            await asyncify(open)(f'obsidian://open?path={ self._vault }/{ notepath }')

    async def get(self, url: str) -> Response:
        await self._check_online()

        try:
            response = await self._httpx.get(url=url)
            await self._check_response(response)
            return response
        except ConnectError:
            logging.info(f'Connect Obsidian Fail while in online state')
            await self.set_offline(self._address, self._token)
            raise DesksetError(message='Obsidian 被意外关闭，切回下线状态')

    async def post(
            self,
            # 参数顺序遵循 REST Client 插件
            url: str,
            headers: Optional[dict] = None,
            data: Optional[object] = None
        ) -> Response:
        await self._check_online()

        try:
            response = await self._httpx.post(
                url=url,
                headers=headers,
                data=data
            )
            await self._check_response(response)
            return response
        except ConnectError:
            logging.info(f'Connect Obsidian Fail while in online state')
            await self.set_offline(self._address, self._token)
            raise DesksetError(message='Obsidian 被意外关闭，切回下线状态')

    # --- 设置读写 ---

    # 问候语
    async def get_greets(self) -> list[Greet]:
        await self._check_online()
        return self._setting.greets


noteapi = NoteAPI()
