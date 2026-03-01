# 开发时，从这里运行服务器
# - 1、避免循环引用
# - 2、模拟生产环境


# === 检查参数 ===
import sys
args = sys.argv
DEVELOP_ENV = True if '-dev' in args else False


# === 运行程序 ===
if __name__ == '__main__':  # 保护程序入口点，避免热重载时，子进程重复执行
    # if DEVELOP_ENV:
    #     # 1、如果在 src/deskset/main.py 使用，必须手动刷新 vscode git 才会显示仓库变化
    #     # 2、用 deskset.main:app 而不是 src.deskset.main:app（触发循环引用）
    #     import uvicorn
    #     from deskset.core.config import config
    #     uvicorn.run('deskset.main:combined_app', host=config.server_host, port=config.server_port, reload=True)
    # if DEVELOP_ENV:
    #     # 2026/03/01：之前避免 uvicorn 阻塞 vscode git 自动刷新的方法失效了
    #       # 代码很扯淡但非常有效...后面再找 launch.json 使用 uv 命令的方式
    #     from os import system
    #     from deskset.core.config import config
    #     system(f'uv run uvicorn deskset.main:combined_app --host={config.server_host} --port={config.server_port} --reload')
    if DEVELOP_ENV:
        # 2026/03/01 二次更新：构造 uvicorn.Server 实例不会阻塞
        import uvicorn
        from deskset.core.config import config
        uvicorn_config = uvicorn.Config(
            'deskset.main:combined_app',
            host=config.server_host,
            port=config.server_port,
            reload=True,
            reload_dirs=['./src/deskset/']
        )
        uvicorn_server = uvicorn.Server(uvicorn_config)
        from uvicorn.supervisors import ChangeReload
        ChangeReload(uvicorn_config, target=uvicorn_server.run, sockets=[uvicorn_config.bind_socket()]).run()
    else:
        from deskset import main
        main()
        # 注意！不会运行 main 之后的代码，因为 main 执行完时通过 sys.exit() 退出并返回退出码
          # sys.exit() 作用：方便父进程 DesksetFront 捕获子进程 DesksetBack 意外结束的原因，比如端口占用


# 注：如果报错，创建 .env 文件
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__  # 可选，统一缓存位置
