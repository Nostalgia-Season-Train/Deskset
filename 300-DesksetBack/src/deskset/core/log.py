LOG_DIR  = 'logs'                   # 日志目录
LOG_FILE = 'DesksetBackLatest.log'  # 日志文件


from pathlib import Path

Path(f'./{LOG_DIR}').mkdir(exist_ok=True)             # 创建日志目录，存在则跳过
Path(f'./{LOG_DIR}/{LOG_FILE}').touch(exist_ok=True)  # 创建日志文件，存在则跳过
open(f'./{LOG_DIR}/{LOG_FILE}', 'w').close()          # 清空（上次）日志文件


import logging

logging.basicConfig(
    filename=f'./{LOG_DIR}/{LOG_FILE}',
    # filemode 注释
      # 注 1：目录不存在也会抛出 FileNotFoundError 异常
      # 注 2：用 a 模式写入，w 模式会意外覆盖运行时日志
    filemode='a',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)
