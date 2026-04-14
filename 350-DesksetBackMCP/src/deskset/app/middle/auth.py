from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from deskset.shared.config import config
from deskset.router._unify.access import access

class AuthMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] not in ('http', 'websocket'):
            return await self.app(scope, receive, send)

        # 限制只能本机（127.0.0.1）访问
        if scope['client'][0] != '127.0.0.1':
            response = PlainTextResponse('Access allowed only from 127.0.0.1', status_code=400)
            return await response(scope, receive, send)

        # 解析标头
        headers = Headers(scope=scope)

        if headers.get('host', None) != f'{config.server_host}:{config.server_port}':
            response = PlainTextResponse('Invalid host header', status_code=400)
            return await response(scope, receive, send)

        # 服务器锁定
        if access.fail_count >= access.Max_Fail_Count:
            response = PlainTextResponse('Server Lock', status_code=400)
            return await response(scope, receive, send)

        return await self.app(scope, receive, send)
