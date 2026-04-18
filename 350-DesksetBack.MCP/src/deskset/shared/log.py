from .constant import LOG_DIR, LOG_STEM_PREFIX, LOG_STEM_FORMAT, LOG_EXTN
import arrow

log_file = f'{LOG_STEM_PREFIX}{arrow.now().format(LOG_STEM_FORMAT)}.{LOG_EXTN}'


from pathlib import Path

Path(f'./{LOG_DIR}').mkdir(exist_ok=True)             # 创建日志目录，存在则跳过
Path(f'./{LOG_DIR}/{log_file}').touch(exist_ok=True)  # 创建日志文件，存在则跳过
# open(f'./{LOG_DIR}/{LOG_FILE}', 'w').close()          # 清空（上次）日志文件


import logging

logging.basicConfig(
    filename=f'./{LOG_DIR}/{log_file}',
    # filemode 注释
      # 注 1：目录不存在也会抛出 FileNotFoundError 异常
      # 注 2：用 a 模式写入，w 模式会意外覆盖运行时日志
    filemode='a',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)
