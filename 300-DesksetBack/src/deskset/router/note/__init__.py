from fastapi import APIRouter, Depends

from deskset.router.unify import check_token

router_note = APIRouter(
    prefix='/v0/note',
    dependencies=[Depends(check_token)]
)


# 注册子路由
from .obsidian._manager import router_obsidian_manager
router_note.include_router(router_obsidian_manager)

from .obsidian import router_obsidian
router_note.include_router(router_obsidian)
