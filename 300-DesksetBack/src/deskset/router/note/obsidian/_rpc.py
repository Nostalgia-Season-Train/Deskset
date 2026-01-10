from typing import Any

from asyncio import Future, get_event_loop
from fastapi import WebSocket

from random import choices
from string import digits, ascii_letters

class RpcClient:
    websocket: WebSocket
    waiting: dict[str, Future]

    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.waiting = {}

    async def call_remote_procedure(self, procedure: str, args: list[Any]) -> Any:
        # 生成 id 和 furture，然后在 waiting 中注册
        id = ''.join(choices(digits + ascii_letters, k=16))
        future = get_event_loop().create_future()
        self.waiting[id] = future

        # 发送请求
        await self.websocket.send_json({
            'id': id,
            'procedure': procedure,
            'args': args
        })

        # 返回 furture
        return await future  # ws.send 不是同步函数，没法在同步函数中返回 future

    async def on_receive(self, response: dict) -> None:
        id = response.get('id')

        if id in self.waiting:
            future = self.waiting.pop(id)
            if response.get('error'):
                future.set_exception(Exception(response['error']))
            else:
                future.set_result(response['payload'])
