from fastapi import APIRouter
from deskset.router.unify import DesksetRepJSON

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

# 问候语
from .greet import router_greet
router_obsidian.include_router(router_greet)
