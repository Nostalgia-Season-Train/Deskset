from argparse import ArgumentParser
from deskset.shared.constant import DEFAUKT_SERVER_PORT

parser = ArgumentParser(description='DesksetBack command-line arguments')
parser.add_argument('-dev', action='store_true', help='Enable development environment')
parser.add_argument('-no-access', action='store_true', help='Turn off authentication')
parser.add_argument('-port', type=int, default=None, help='Set off server port')
parser.add_argument('-token', type=str, default=None, help='Set off server token')
args, _ = parser.parse_known_args()  # _ 忽略 uvicorn 热重载传入的参数

DEVELOP_ENV    = args.dev        # True 开发环境；False 生产环境
DISABLE_ACCESS = args.no_access  # True 禁用认证；False 启用认证

# 端口和令牌
SERVER_PORT = args.port
SERVER_TOKEN = args.token

# 打印所有命令行参数
# from sys import argv
# print(argv)
