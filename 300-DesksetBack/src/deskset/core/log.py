import logging

with open('logs/DesksetBack.log', 'w') as file:
    # 清空上次日志
    pass

logging.basicConfig(
    filename='logs/DesksetBack.log',
    # filemode 注释
      # 注 1：目录不存在也会抛出 FileNotFoundError 异常
      # 注 2：用 a 模式写入，w 模式会意外覆盖运行时日志
    filemode='a',
    format='[%(asctime)s] [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    encoding='utf-8'
)
