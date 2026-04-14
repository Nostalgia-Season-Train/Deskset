# ==== FastAPI Router：AI 人工智能 ====

# --- 重建 DesksetError 消息 ---
  # 流程：
    # FastMCP.call_tool：DesksetError 被 ToolError 包装 ToolError from DesksetError
    # ErrorHandlingMiddleware：DesksetError 从 ToolError 中提取 DesksetError from ToolError.__cause__
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware import MiddlewareContext
from deskset.shared.standard import DesksetError
from mcp import McpError
from mcp.types import ErrorData

origin_transform_error = ErrorHandlingMiddleware._transform_error
def custom_transform_error(self, error: Exception, context: MiddlewareContext) -> Exception:
    if isinstance(error.__cause__, DesksetError):
        return McpError(ErrorData(code=200, message=error.__cause__.message))
    return origin_transform_error(self, error, context)
ErrorHandlingMiddleware._transform_error = custom_transform_error

# --- 禁止 FastMCP 打印一般错误 ---
import logging
logging.getLogger('fastmcp').setLevel(logging.CRITICAL)

from fastapi import APIRouter, Depends
from deskset.router._unify import check_token
router_ai = APIRouter(
    prefix='/ai', tags=['ai'],
    dependencies=[Depends(check_token)]
    # 不加 DesksetRepJSON 区分普通 RestAPI 端点
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

from openai import AsyncOpenAI as OpenAI
from fastmcp import Client

class AIManager:
    _ai_client: OpenAI | None
    _mcp_client: Client | None
    _messages: list[dict[str, str]]  # { role, content }[]

    def __init__(self):
        self._ai_client = None
        self._mcp_client = None  # mcp 在后面实例化
        self._messages = []

    async def _load_messages(self):
        try:
            import pathlib
            if not pathlib.Path('./store/latest-chat.yaml').is_file():
                return
            import yaml
            with open('./store/latest-chat.yaml', 'r', encoding='utf-8') as file:
                self._messages = yaml.safe_load(file)['messages']
        except Exception:
            pass

    async def _save_messages(self):
        try:
            import pathlib
            pathlib.Path('./store').mkdir(exist_ok=True)
            pathlib.Path('./store/latest-chat.yaml').touch(exist_ok=True)
            import yaml
            with open('./store/latest-chat.yaml', 'w', encoding='utf-8') as file:
                # - [ ] 后面再找单独对 content 应用 | 换行的方法
                yaml.safe_dump({ 'messages': self._messages }, file, allow_unicode=True, sort_keys=False, default_style='|')
        except Exception:
            pass

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
        response = await self._ai_client.responses.create(
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
                output = None
                async with self._mcp_client:  # type: ignore
                    try:
                        result = await self._mcp_client.call_tool(name, arguments)  # type: ignore
                        output = dumps(result.structured_content) if result.structured_content is not None else '{}'
                    except Exception as exc:
                        output = f'Call Tool Failed, Reason: {exc}'
                # 上下文：添加 MCP 结果
                call_id = chunk.item.call_id
                self._messages.append({ 'type': 'function_call_output', 'call_id': call_id, 'output': output })

    async def stream(self, user_message):
        # 上下文：添加用户消息
        self._messages.append({ 'role': 'user', 'content': user_message })
        response = await self._create_response()
        async for chunk in response:
            await self._deal_with_chunk(chunk)
            yield chunk.to_json(indent=None) + '\n'  # indent=None 紧凑格式；结尾加 \n 分割 json
        # 上一条消息是 MCP 结果，继续回复
        while self._messages[len(self._messages) - 1].get('type', None) == 'function_call_output':
            # _deal_with_chunk 回填结果，创建最终回复
            response = await self._create_response()
            async for chunk in response:
                await self._deal_with_chunk(chunk)
                yield chunk.to_json(indent=None) + '\n'
        return

ai_manager = AIManager()

from fastapi import Body
from fastapi.responses import StreamingResponse
@router_ai.post('/hello')
async def hello(body: str = Body(...)):
    # 模型输入必须非空（包括仅含空格、换行符等字符的情况）
    if body.isspace():
        return
    return StreamingResponse(ai_manager.stream(body), media_type='text/plain')

@router_ai.get('/latest-messages')
async def get_latest_messages():
    return ai_manager._messages

app.include_router(router_ai)
