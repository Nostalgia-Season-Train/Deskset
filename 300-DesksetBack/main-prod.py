# === PyStand 环境：避免多进程无限循环创建 ===
import sys
import multiprocessing

if not hasattr(sys, 'frozen'):
    sys.frozen = True  # type: ignore

multiprocessing.freeze_support()


# === 检查参数 ===
args = sys.argv
DEVELOP_ENV = True if '-dev' in args else False


# === 运行程序 ===
if __name__ == '__main__':
    if DEVELOP_ENV:
        import uvicorn
        from deskset.core.config import config
        uvicorn.run(
            'deskset.main:app',
            host=config.server_host,
            port=config.server_port,
            reload=True,
            use_colors=False  # use_colors=False：cmd.exe 不支持打印颜色，显示乱码
        )
    else:
        # -dev 启动，虽然经过判断，但是下面的代码仍会执行，导致默认端口 6527 重复占用
          # 暂时不处理
        from deskset import main
        main()
