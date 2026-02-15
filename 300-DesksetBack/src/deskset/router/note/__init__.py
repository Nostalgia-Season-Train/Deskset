from fastapi import APIRouter, Depends
from deskset.router._unify import check_token, DesksetRepJSON

router_note = APIRouter(
    prefix='/v0/note',
    dependencies=[Depends(check_token)]
)


# ==== ObsidianManager ====
from ._manager import router_obsidian_manager

router_note.include_router(router_obsidian_manager)


# ==== Obsidian ====
router_obsidian = APIRouter(
    prefix='/obsidian', tags=['Obsidian'],
    default_response_class=DesksetRepJSON
)

# 通用
from .common import router_common
router_obsidian.include_router(router_common)
# 个性资料
from .profile import router_profile
router_obsidian.include_router(router_profile)
# 日记
from .diary import router_diary
router_obsidian.include_router(router_diary)
# 数据统计
from .stats import router_stats
router_obsidian.include_router(router_stats)
# 搜索
from .search import router_search
router_obsidian.include_router(router_search)

router_note.include_router(router_obsidian)
