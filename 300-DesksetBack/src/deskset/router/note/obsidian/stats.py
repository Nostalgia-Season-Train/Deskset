from fastapi import APIRouter, Depends
from pydantic import BaseModel, RootModel
from deskset.router.unify import DesksetReqNumberInt
from ._manager import api as noteapi

router_stats = APIRouter(prefix='/stats')

@router_stats.get('/note-number')
async def note_number():
    return await noteapi.get_note_number()

@router_stats.get('/attachment-number')
async def attachment_number():
    return await noteapi.get_attachment_number()

@router_stats.get('/useday-number')
async def useday_number():
    return await noteapi.get_useday_number()

@router_stats.get('/heatmap/{num}')
async def heatmap(req: DesksetReqNumberInt = Depends()):
    weeknum = req.num  # 统计范围：前 weeknum 周 + 本周
    return await noteapi.get_heatmap(weeknum)

# - [ ] 临时，后面转移到新路由
class Filter(BaseModel):
    type: str = 'contains'  # 比较类型：is、startsWith、endsWith、contains、isEmpty
    isInvert: bool = False  # 是否取反比较结果
    propertyKey: str        # 要比较的属性
    compareValue: str | int # 要比较的值

# 注：OpenAPI 会误将 filters 中的 FilterGroup 识别为 str，实际工作正常
class FilterGroup(BaseModel):
    match: str
    filters: list['Filter | FilterGroup']

# 注 1：filters 若为空数组返回 所有笔记
# 注 2：propertyKey 若为空字符串，该次 filter 返回 false
# 注 3：type 若不为上述五种类型，该次 filter 返回 false
@router_stats.post('/filter-frontmatter')
async def filter_frontmatter(filter_group: FilterGroup):
    return await noteapi.filter_frontmatter(filter_group.model_dump())

@router_stats.post('/filter-frontmatter-number')
async def filter_frontmatter_number(filter_group: FilterGroup):
    return await noteapi.filter_frontmatter_number(filter_group.model_dump())

@router_stats.post('/filter-and-random-open-in-obsidian')
async def filter_and_random_open_in_obsidian(filter_group: FilterGroup):
    return await noteapi.filter_and_random_open_in_obsidian(filter_group.model_dump())
