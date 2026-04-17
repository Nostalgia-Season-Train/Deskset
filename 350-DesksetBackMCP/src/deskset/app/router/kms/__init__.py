from fastapi import APIRouter
# from deskset.app.router._unify import DesksetRepJSON

router_kms = APIRouter(
    prefix='/kms',
)


# ==== Obsidian ====

# 上下线事件
@router_kms.get('/is_online')
async def is_online():
    from fastapi.responses import StreamingResponse
    from deskset.feature.kms.api import noteapi
    async def stream():
        try:
            while True:
                if noteapi.is_online():
                    yield 'online'
                else:
                    yield 'offline'
                await noteapi.event_onoffline.wait()
        except Exception:
            pass
        finally:
            return
    return StreamingResponse(stream(), media_type='text/plain')

# 通用
from .common import router_common
router_kms.include_router(router_common)
# 个性资料
from .profile import router_profile
router_kms.include_router(router_profile)
# 日记
from .diary import router_diary
router_kms.include_router(router_diary)
# 任务
from .task import router_task
router_kms.include_router(router_task)
# 数据统计
from .stats import router_stats
router_kms.include_router(router_stats)
# 搜索
from .search import router_search
router_kms.include_router(router_search)
# 命令 Command
from .command import router_command
router_kms.include_router(router_command)
# 窗口页面 Winpage
from .winpage import router_winpage
router_kms.include_router(router_winpage)
# 笔记 Note
from .note import router_note as router_notes
router_kms.include_router(router_notes)
