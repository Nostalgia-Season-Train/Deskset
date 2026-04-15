# ==== 服务器运行状态 ====
from deskset.shared.utils import generate_token

# 基地址、端口号、令牌
from deskset.shared.constant import DEFAUKT_SERVER_HOST, DEFAUKT_SERVER_PORT
from .args import SERVER_PORT, SERVER_TOKEN
server_host = DEFAUKT_SERVER_HOST
server_port = SERVER_PORT if SERVER_PORT is not None else DEFAUKT_SERVER_PORT
server_token = SERVER_TOKEN if SERVER_TOKEN is not None else generate_token()

# 是否启用开发模式、是否禁用认证
from .args import DEVELOP_ENV, DISABLE_ACCESS
develop_mode = DEVELOP_ENV
disable_access = DISABLE_ACCESS

# 强制关闭超时时间
from deskset.shared.constant import SHUTDOWN_TIMEOUT
shutdown_timeout = SHUTDOWN_TIMEOUT
