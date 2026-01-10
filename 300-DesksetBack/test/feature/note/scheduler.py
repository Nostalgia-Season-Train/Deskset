from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from deskset.router.note.noteapi import noteapi  # 测试后移除 feature <=> router 导致循环引用

apscheduler = AsyncIOScheduler(job_defaults={ 'misfire_grace_time': 30 })  # 错过约定时间后，30s 之内仍会执行


# 禁止 apscheduler 输出 ERROR 级别以下的日志
import logging

logging.getLogger('apscheduler').setLevel(logging.ERROR)
