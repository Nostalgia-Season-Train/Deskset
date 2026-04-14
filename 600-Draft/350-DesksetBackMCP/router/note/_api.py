# ==== 登录 Access ====
  # - [ ] 改进：连接步骤 = http 登录 + websocket 上线/下线
    # 1、http 访问 login：身份认证和初始信息，生成本次 wstoken 及 { wstoken: 初始信息 }
    # 2、websocket 访问 rpc：检查 wstoken 后取回初始信息，创建 RpcClient(ws, init)
from deskset.shared.config import DESKSET_NOTEAPI_VERSION
from fastapi import Request, Form

@router_access.post('/obsidian/login')
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
        from deskset.shared.log import logging
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
