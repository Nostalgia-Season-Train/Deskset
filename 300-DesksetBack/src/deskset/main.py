# ==== 类型标注 ====
from __future__ import annotations


# ==== 命令行参数 ====
from argparse import ArgumentParser

parser = ArgumentParser(description='数字桌搭后端命令行参数')
parser.add_argument('-dev', action='store_true', help='以开发者环境启动')
args, _ = parser.parse_known_args()  # 忽略 uvicorn 热重载传入的参数

DEVELOP_ENV = args.dev
DEBUG_MODE  = False  # 调试模式


# ==== 确保各模块所需目录存在 ====
from pathlib import Path

Path('./config').mkdir(exist_ok=True)  # 配置 core.config
Path('./logs').mkdir(exist_ok=True)    # 日志 core.log

Path('./i18n').mkdir(exist_ok=True)  # 翻译 core.locale

Path('./scripts').mkdir(exist_ok=True)  # 脚本 feature.quick.open
Path('./plugins').mkdir(exist_ok=True)  # 插件 router.plugin


# ==== 日志 ====
from deskset.core.log import logging

if DEVELOP_ENV:
    logging.info('Running on Development Environment')
if DEBUG_MODE:
    logging.info('Open Debug Mode')


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


# ==== FastAPI：中间件 ====
from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from deskset.router.unify.access import access

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

app.add_middleware(AllowOnly127001tMiddleware)


# ==== FastAPI：CORS 跨域请求 ====
  # Vite：http://localhost:1420
  # Tauri：http://tauri.localhost
  # Obsidian：app://obsidian.md
if DEVELOP_ENV:  # 开发时有 Vite Server 需要添加 CORS
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://tauri.localhost', 'app://obsidian.md'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    logging.info(f'Add http://tauri.localhost, app://obsidian.md to CORS')


# ==== FastAPI：统一错误（异常）处理 ====
from fastapi.requests import Request
from deskset.core.standard import DesksetError
from fastapi.responses import JSONResponse
from deskset.router.unify import DesksetErrorRep
from http import HTTPStatus

@app.exception_handler(DesksetError)
def deskset_error(request: Request, err: DesksetError):
    return DesksetErrorRep(content=err)

@app.exception_handler(Exception)
def deskset_exception(request: Request, exc: Exception):
    logging.exception(exc, exc_info=exc)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=str(exc)
    )


# ==== FastAPI：离线 OpenAPI 文档和演练场 ====
if DEVELOP_ENV:
    from fastapi.staticfiles import StaticFiles

    app.mount('/static', StaticFiles(directory='static'), name='static')

    # OpenAPI 文档
    from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html

    @app.get('/docs', include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,  # type: ignore
            title=app.title + ' - Swagger UI',
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url='/static/docs/swagger-ui-bundle.js',
            swagger_css_url='/static/docs/swagger-ui.css'
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)  # type: ignore
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    # 演练场
    from fastapi.responses import Response

    @app.get('/playground', include_in_schema=False)
    async def playground_html():
        with open('static/playground/index.html', 'r', encoding='utf-8') as file:
            content = file.read()
        return Response(content=content, media_type='text/html')


# ==== FastAPI Router：调试接口 ====
if DEBUG_MODE:
    from deskset.router.debug import router_debug
    app.include_router(router_debug)


# ==== FastAPI Router：路由注册 ====
from deskset.router.config import router_config
app.include_router(router_config)

from deskset.router.device import router_device
app.include_router(router_device)

from deskset.router.note import router_note
app.include_router(router_note)

from deskset.router.profile import router_profile
app.include_router(router_profile)

from deskset.router.greet import router_greet
app.include_router(router_greet)

# from deskset.router.current import router_datetime
# app.include_router(router_datetime)

# from deskset.router.cloud import router_cloud
# app.include_router(router_cloud)

from deskset.router.quick import router_quick
app.include_router(router_quick)

from deskset.router.weather import router_weather
app.include_router(router_weather)


# ==== FastAPI Router：插件注册：/plugin 作为所有插件路由的根路径 ====
from deskset.router.plugin import router_plugin_root
app.include_router(router_plugin_root)


# ==== FastAPI Router：认证接口 ====
  # 移到末尾注册，方便其他模块在 router_access 上挂载 REST 端点
from deskset.router.unify import router_access
app.include_router(router_access)


# 启动服务器
import uvicorn
import sys

def main():
    logging.info('==== all modules import completed, execute main function ====')

    logging.info('run uvicorn server')
    try:
        # log_config=None & log_level='error' 作用：日志从控制台改为输出到文件 + 日志级别 error
        uvicorn.run(app, host=server_host, port=server_port, log_config=None, log_level='error')
    except SystemExit:  # 捕获 uvicorn 异常退出，以便日志记录 OSError 信息
        logging.exception('uvicorn crash!')
        logging.error('end uvicorn server with exception')  # logging.exception 重复打印 SystemExit 堆栈...
        sys.exit(1)  # 退出码 1：异常退出

    logging.info('end uvicorn server')
    sys.exit(0)  # 退出码 0：正常退出

# 在这个文件启用 uvicorn.run(reload=True) 会影响 vscode git 检查
