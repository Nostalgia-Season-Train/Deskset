from argparse import ArgumentParser

parser = ArgumentParser(description='DesksetBack command-line arguments')
parser.add_argument('-dev', action='store_true', help='Enable development environment')
parser.add_argument('-no-access', action='store_true', help='Turn off authentication')
args, _ = parser.parse_known_args()  # _ 忽略 uvicorn 热重载传入的参数

DEVELOP_ENV    = args.dev        # True 开发环境；False 生产环境
DISABLE_ACCESS = args.no_access  # True 禁用认证；False 启用认证
