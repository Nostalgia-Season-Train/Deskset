# ==== 类型标注 ====
from __future__ import annotations


# ==== 命令行参数 ====
from deskset.core.args import DEVELOP_ENV


# ==== 确保各模块所需目录存在 ====
from pathlib import Path

Path('./config').mkdir(exist_ok=True)  # 配置 core.config

Path('./scripts').mkdir(exist_ok=True)  # 脚本 feature.quick.open
Path('./plugins').mkdir(exist_ok=True)  # 插件 router.plugin


# ==== 日志 ====
from deskset.core.log import logging

if DEVELOP_ENV:
    logging.info('Running on Development Environment')


# ==== 服务器地址 host 和端口 port ====
from deskset.core.config import config

server_host = config.server_host
server_port = config.server_port
logging.info(f'Server URL is http://{server_host}:{server_port}')


# ==== Lifespan 生命周期 ====
from contextlib import asynccontextmanager

# from deskset.feature.note import apscheduler as note_apscheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 信息传输：DesksetBack = 标准输出流 => DesksetFront
    print(f'{{"url": "{server_host}:{server_port}", "token": "{access._token}"}}', flush=True)

    logging.info('start lifespan')
    # note_apscheduler.start()  # 不用 paused=True 暂停，uvicorn.run 自然启停
    yield
    logging.info('finish lifespan')
    # note_apscheduler.shutdown()


# ==== FastAPI 应用 ====
# ！！！警告，需要身份验证，不然任意桌面应用程序都能访问本服务器！！！
# 一个 CSRF 示例：<img src="http://127.0.0.1:8000/v0/device/cpu"></img>，可在其他 Electron 程序中访问本服务器接口
from fastapi import FastAPI

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)


# ==== FastAPI Router：路由注册 ====
from deskset.router._config import router_config
app.include_router(router_config)

from deskset.router.device import router_device
app.include_router(router_device)

from deskset.router.note import router_note
app.include_router(router_note)

from deskset.router.quick import router_quick
app.include_router(router_quick)


# ==== FastAPI Router：插件注册：/plugin 作为所有插件路由的根路径 ====
from deskset.router._plugin import router_plugin_root
app.include_router(router_plugin_root)


# ==== FastAPI Router：认证接口 ====
  # 移到末尾注册，方便其他模块在 router_access 上挂载 REST 端点
from deskset.router._unify import router_access
app.include_router(router_access)


# ==== FastAPI Router：AI 人工智能 ====
from fastapi import APIRouter, Depends
from deskset.router._unify import check_token
router_ai = APIRouter(
    prefix='/ai', tags=['ai'],
    dependencies=[Depends(check_token)]
)

from fastmcp import Client
@router_ai.get('/mcp-tools')
async def get_mcp_tools():
    tools = []
    async with Client(mcp) as client:
        raw_tools = await client.list_tools()
        tools = [{
            'type': 'function',
            'name': raw_tool.name,
            'description': raw_tool.description,
            'parameters': raw_tool.inputSchema
        } for raw_tool in raw_tools ]
    return tools

from openai import OpenAI
from fastmcp import Client

class AIManager:
    _ai_client: OpenAI | None
    _mcp_client: Client | None
    _messages: list[dict[str, str]]  # { role, content }[]

    def __init__(self):
        self._ai_client = None
        self._mcp_client = None  # mcp 在后面实例化
        self._messages = []

    async def _create_response(self):
        # AI Client
        if self._ai_client is None:
            self._ai_client = OpenAI(
                base_url=config.ai_base_url,
                api_key=config.ai_api_key
            )
        # MCP Client
        if self._mcp_client is None:
            self._mcp_client = Client(mcp)
        # MCP Tools
        mcp_tools = await get_mcp_tools()
        # Response
        response = self._ai_client.responses.create(
            model=config.ai_model,
            input=self._messages,  # type: ignore
            tools=mcp_tools,  # type: ignore
            stream=True,
            extra_body={ 'thinking': { 'type': 'disabled' } }  # 暂时禁用思考模式
        )
        return response

    async def _deal_with_chunk(self, chunk):
        if chunk.type == 'response.output_item.done':
            # 正常对话
            if chunk.item.type == 'message':
                text = ''
                for content in chunk.item.content:
                    text += content.text + '\n'
                # 上下文：添加 AI 消息
                self._messages.append({ 'role': 'assistant', 'content': text })
            # MCP 调用
            if chunk.item.type == 'function_call':
                from json import loads, dumps
                name = chunk.item.name
                arguments = loads(chunk.item.arguments)
                result = None
                async with self._mcp_client:  # type: ignore
                    result = await self._mcp_client.call_tool(name, arguments)  # type: ignore
                # 上下文：添加 MCP 结果
                call_id = chunk.item.call_id
                output = dumps(result.structured_content) if result.structured_content is not None else '{}'
                self._messages.append({ 'type': 'function_call_output', 'call_id': call_id, 'output': output })

    async def stream(self, user_message):
        # 上下文：添加用户消息
        self._messages.append({ 'role': 'user', 'content': user_message })
        response = await self._create_response()
        for chunk in response:
            await self._deal_with_chunk(chunk)
            yield chunk.to_json(indent=None) + '\n'  # indent=None 紧凑格式；结尾加 \n 分割 json
        if self._messages[len(self._messages) - 1].get('type', None) != 'function_call_output':
            return
        # _deal_with_chunk 回填结果，创建最终回复
        response = await self._create_response()
        for chunk in response:
            await self._deal_with_chunk(chunk)
            yield chunk.to_json(indent=None) + '\n'
        return

ai_manager = AIManager()

from fastapi import Body
from fastapi.responses import StreamingResponse
@router_ai.post('/hello')
async def hello(body: str = Body(...)):
    # 模型输入必须非空
    if body == '':
        return
    return StreamingResponse(ai_manager.stream(body), media_type='text/plain')

app.include_router(router_ai)


# ==== FastMCP 服务器 ====
  # 文档：https://gofastmcp.com/integrations/fastapi#offering-an-llm-friendly-api
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import RouteMap, MCPType
from fastmcp.utilities.lifespan import combine_lifespans

mcp = FastMCP.from_fastapi(
    app=app,
    route_maps=[
        RouteMap(tags={'access'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'config'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'device'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'quick'},  mcp_type=MCPType.EXCLUDE),
        RouteMap(pattern=r'^/ai/.*', mcp_type=MCPType.EXCLUDE),
        RouteMap(pattern=r'^/v0/.*', mcp_type=MCPType.EXCLUDE),
    ]
)
mcp_app = mcp.http_app(path='/mcp')

combined_app = FastAPI(
    routes=[*app.routes, *mcp_app.routes],
    lifespan=combine_lifespans(lifespan, mcp_app.lifespan),
    docs_url=None,
    redoc_url=None
)


# ==== FastMCP 客户端 ====
@mcp.tool
def greet_name(name: str) -> str:
    '''Greet a user by name.'''
    print(f'Hello, {name}!')
    return f'Hello, {name}!'

from fastmcp import Client
from asyncio import create_task

async def test_client():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print(f'Tools: {tools}')

# create_task(test_client())


# ==== CombinedApp：中间件 ====
from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from deskset.router._unify.access import access

# 仅允许本机访问
  # 对 http 和 websocket 都生效
class AllowOnly127001tMiddleware:
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

        if headers.get('host', None) != f'{server_host}:{server_port}':
            response = PlainTextResponse('Invalid host header', status_code=400)
            return await response(scope, receive, send)

        # 服务器锁定
        if access.fail_count >= access.Max_Fail_Count:
            response = PlainTextResponse('Server Lock', status_code=400)
            return await response(scope, receive, send)

        return await self.app(scope, receive, send)

combined_app.add_middleware(AllowOnly127001tMiddleware)


# ==== CombinedApp：CORS 跨域请求 ====
  # Vite：http://localhost:1420
  # Tauri：http://tauri.localhost
  # Obsidian：app://obsidian.md
if DEVELOP_ENV:  # 开发时有 Vite Server 需要添加 CORS
    from fastapi.middleware.cors import CORSMiddleware

    combined_app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost:1420',   # 开发环境：Vite 服务器
            'http://tauri.localhost',  # 生产环境：Tauri 自定义协议
            'app://obsidian.md',       # Obsidian
            'http://localhost:5173'    # 数字桌搭演练场 DesksetPlayground
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    logging.info(f'Add http://localhost:1420, http://tauri.localhost, app://obsidian.md, http://localhost:5173 to CORS')

if not DEVELOP_ENV:  # Tauri 构建后用 http://tauri.localhost 通信...
    from fastapi.middleware.cors import CORSMiddleware

    # 会覆盖上面的 CORS，不要一起用
    combined_app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://tauri.localhost', 'app://obsidian.md'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    logging.info(f'Add http://tauri.localhost, app://obsidian.md to CORS')


# ==== CombinedApp：统一问题（错误、异常）处理 ====
from fastapi.requests import Request
from deskset.core.standard import DesksetError
from fastapi.responses import JSONResponse
from deskset.router._unify import DesksetErrorRep
from http import HTTPStatus

@combined_app.exception_handler(DesksetError)
def deskset_error(request: Request, err: DesksetError):
    return DesksetErrorRep(content=err)

@combined_app.exception_handler(Exception)
def deskset_exception(request: Request, exc: Exception):
    logging.exception(exc, exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=str(exc)
    )


# ==== CombinedApp：离线 OpenAPI 文档和演练场 ====
from fastapi.staticfiles import StaticFiles

combined_app.mount('/static', StaticFiles(directory='static'), name='static')

# OpenAPI 文档
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html

@combined_app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + ' - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/docs/swagger-ui-bundle.js',
        swagger_css_url='/static/docs/swagger-ui.css'
    )

@combined_app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

    # 演练场
    # from fastapi.responses import Response

    # @app.get('/playground', include_in_schema=False)
    # async def playground_html():
    #     with open('static/playground/index.html', 'r', encoding='utf-8') as file:
    #         content = file.read()
    #     return Response(content=content, media_type='text/html')


# ==== 启动服务器 ====
import uvicorn
import sys

def main():
    logging.info('==== all modules import completed, execute main function ====')

    logging.info('run uvicorn server')
    try:
        # log_config=None & log_level='error' 作用：日志从控制台改为输出到文件 + 日志级别 error
        uvicorn.run(
            combined_app,
            host=server_host,
            port=server_port,
            timeout_graceful_shutdown=config.shutdown_graceful_timeout,
            log_config=None,
            log_level='error'
        )
    except SystemExit:  # 捕获 uvicorn 异常退出，以便日志记录 OSError 信息
        logging.exception('uvicorn crash!')
        logging.error('end uvicorn server with exception')  # logging.exception 重复打印 SystemExit 堆栈...
        sys.exit(1)  # 退出码 1：异常退出

    logging.info('end uvicorn server')
    sys.exit(0)  # 退出码 0：正常退出

# 在这个文件启用 uvicorn.run(reload=True) 会影响 vscode git 检查
