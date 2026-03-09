from fastapi import APIRouter, Depends
from deskset.router._unify import DesksetReqDateDay, DesksetReqDateMonth
from ._api import noteapi

router_diary = APIRouter(prefix='/diary')

# 读取日记插件设置
@router_diary.get('/setting')
async def get_diary_setting():
    return await noteapi.get_diary_setting()

# 读取某天日记（日期格式：YYYYMMDD）
@router_diary.post('/read')
async def read_day(date: DesksetReqDateDay):
    return await noteapi.read_diary(date.day)

# 创建、写入、删除某日日记
@router_diary.post('/create')
async def create_diary(param: DesksetReqDateDay):
    return await noteapi.create_diary(param.day)
class WriteDiaryParam(DesksetReqDateDay):
    data: str
@router_diary.post('/write')
async def write_diary(param: WriteDiaryParam):
    return await noteapi.write_diary(param.day, param.data)
@router_diary.post('/delete')
async def delete_diary(param: DesksetReqDateDay):
    return await noteapi.delete_diary(param.day)

# 列出某月中的日记属性（日期格式：YYYYMM）
@router_diary.post('/prop/list-in-month')
async def read_month(date: DesksetReqDateMonth):
    return await noteapi.list_diaryprops_in_a_month(date.month)
