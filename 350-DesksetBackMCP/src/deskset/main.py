# ==== 类型标注 ====
from __future__ import annotations


# ==== 命令行参数 ====
from deskset.app.args import DEVELOP_ENV


# ==== 确保各模块所需目录存在 ====
from pathlib import Path

Path('./config').mkdir(exist_ok=True)  # 配置 core.config

Path('./scripts').mkdir(exist_ok=True)  # 脚本 feature.quick.open
Path('./plugins').mkdir(exist_ok=True)  # 插件 router.plugin


# ==== 日志 ====
from deskset.shared.log import logging

if DEVELOP_ENV:
    logging.info('Running on Development Environment')


# ==== 服务器地址 host 和端口 port ====
from deskset.app.store import server_host, server_port

logging.info(f'Server URL is http://{server_host}:{server_port}')


# ==== Lifespan 生命周期 ====
from contextlib import asynccontextmanager
# from deskset.app.router._unify.access import access

# from deskset.feature.note import apscheduler as note_apscheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 信息传输：DesksetBack = 标准输出流 => DesksetFront
    # print(f'{{"url": "{server_host}:{server_port}", "token": "{access._token}"}}', flush=True)

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
# from deskset.router._config import router_config
# app.include_router(router_config)

from deskset.app.router.device import router_device
app.include_router(router_device)

from deskset.app.router.note import router_note
app.include_router(router_note)

# from deskset.app.router.quick import router_quick
# app.include_router(router_quick)


# ==== FastAPI Router：插件注册：/plugin 作为所有插件路由的根路径 ====
# from deskset.router._plugin import router_plugin_root
# app.include_router(router_plugin_root)


# ==== FastAPI Router：认证接口 ====
  # 移到末尾注册，方便其他模块在 router_access 上挂载 REST 端点
# from deskset.app.router._unify import router_access
# app.include_router(router_access)


# ==== FastMCP 服务器 ====
  # 文档：https://gofastmcp.com/integrations/fastapi#offering-an-llm-friendly-api
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import RouteMap, MCPType
from fastmcp.utilities.lifespan import combine_lifespans

# 以下代码等同于 validate_output=False，热修复 from_openapi 有但 from_fastapi 没有的参数
# from fastmcp.server.providers.openapi import OpenAPIProvider
# OpenAPIProvider.__init__.__kwdefaults__['validate_output'] = False  # type: ignore

mcp = FastMCP.from_fastapi(
    app=app,
    route_maps=[
        RouteMap(tags={'access'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'config'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'device'}, mcp_type=MCPType.EXCLUDE),
        RouteMap(tags={'quick'},  mcp_type=MCPType.EXCLUDE),
        RouteMap(pattern=r'^/ai/.*', mcp_type=MCPType.EXCLUDE),
        RouteMap(pattern=r'^/v0/note/obsidian/winpage/.*', mcp_type=MCPType.TOOL),
        RouteMap(pattern=r'^/v0/note/obsidian/diary/.*today', mcp_type=MCPType.TOOL),
        RouteMap(pattern=r'^/v0/note/obsidian/note/.*', mcp_type=MCPType.TOOL),
        RouteMap(mcp_type=MCPType.EXCLUDE)  # 排除未明确指定的路由
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
from deskset.app.middle import AuthMiddleware

combined_app.add_middleware(AuthMiddleware)


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
from deskset.shared.standard import DesksetError
from fastapi.responses import JSONResponse
from deskset.app.router._unify import DesksetErrorRep
from http import HTTPStatus

@combined_app.exception_handler(DesksetError)
def deskset_error(request: Request, err: DesksetError):
    return DesksetErrorRep(content=err)

from deskset.shared.error import DesksetErrorNew
@combined_app.exception_handler(DesksetErrorNew)
def deskset_error_new(request: Request, err: DesksetErrorNew):
    return JSONResponse(
        status_code=HTTPStatus.NOT_IMPLEMENTED,
        media_type='application/json',
        content={ 'code': err.code, 'message': err.message }
    )

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
from deskset.shared.constant import SHUTDOWN_TIMEOUT

def main():
    logging.info('==== all modules import completed, execute main function ====')

    logging.info('run uvicorn server')
    try:
        # log_config=None & log_level='error' 作用：日志从控制台改为输出到文件 + 日志级别 error
        uvicorn.run(
            combined_app,
            host=server_host,
            port=server_port,
            timeout_graceful_shutdown=SHUTDOWN_TIMEOUT,
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
