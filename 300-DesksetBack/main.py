# 开发时，从这里运行服务器
# - 1、避免循环引用
# - 2、模拟生产环境


# === 检查参数 ===
import sys
args = sys.argv
DEVELOP_ENV = True if '-dev' in args else False


# === 运行程序 ===
if __name__ == '__main__':  # 保护程序入口点，避免热重载时，子进程重复执行
    if DEVELOP_ENV:
        # 1、如果在 src/deskset/main.py 使用，必须手动刷新 vscode git 才会显示仓库变化
        # 2、用 deskset.main:app 而不是 src.deskset.main:app（触发循环引用）
        import uvicorn
        from deskset.core.config import config
        uvicorn.run('deskset.main:app', host=config.server_host, port=config.server_port, reload=True)
    else:
        from deskset import main
        main()
        # 注意！不会运行 main 之后的代码，因为 main 执行完时通过 sys.exit() 退出并返回退出码
          # sys.exit() 作用：方便父进程 DesksetFront 捕获子进程 DesksetBack 意外结束的原因，比如端口占用


# 注：如果报错，创建 .env 文件
# PYTHONPATH=./src
# PYTHONPYCACHEPREFIX=./__pycache__  # 可选，统一缓存位置
