from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .store import server_host, server_port, server_token, disable_access

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

        # 如果禁用认证，直接放行
        if disable_access:
            return await self.app(scope, receive, send)

        # 解析标头
        headers = Headers(scope=scope)

        if headers.get('host', None) != f'{server_host}:{server_port}':
            response = PlainTextResponse('Invalid host header', status_code=400)
            return await response(scope, receive, send)

        # 验证令牌
        if not await self._is_authorized(scope, headers):
            # HTTP 请求
            if scope['type'] == 'http':
                response = PlainTextResponse('Unauthorized', status_code=401)
            # WebSocket 连接
            if scope['type'] == 'websocket':
                response = PlainTextResponse('Unauthorized', status_code=401, headers={ 'Sec-WebSocket-Protocol': 'Authorization' })
            else:
                response = PlainTextResponse('Unauthorized', status_code=401)
            return await response(scope, receive, send)

        # 服务器锁定
        # if access.fail_count >= access.Max_Fail_Count:
        #     response = PlainTextResponse('Server Lock', status_code=400)
        #     return await response(scope, receive, send)

        return await self.app(scope, receive, send)

    async def _is_authorized(self, scope: Scope, headers: Headers) -> bool:
        """验证令牌是否有效"""
        if scope['type'] == 'http':
            return await self._verify_http_bearer(headers)
        elif scope['type'] == 'websocket':
            return await self._verify_websocket_protocol(headers)
        return False

    async def _verify_http_bearer(self, headers: Headers) -> bool:
        """验证 HTTP Bearer token 令牌"""
        authorization = headers.get('Authorization', '')
        if not authorization.startswith('Bearer '):
            return False

        token = authorization[len('Bearer '):]
        return token == server_token

    async def _verify_websocket_protocol(self, headers: Headers) -> bool:
        """验证 WebSocket Sec-WebSocket-Protocol 中的 Authorization, Bearer-token 令牌"""
        raw_protocol = headers.get('Sec-WebSocket-Protocol', '')
        if not raw_protocol:
            return False

        protocols = [p.strip() for p in raw_protocol.split(',')]
        if len(protocols) != 2:
            return False
        if protocols[0] != 'Authorization':
            return False
        if protocols[1] != f'Bearer-{server_token}':
            return False

        return False
