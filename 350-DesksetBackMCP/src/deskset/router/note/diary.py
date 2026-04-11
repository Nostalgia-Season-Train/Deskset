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

# 编辑、插入日记
  # 区别于写入覆盖整个日记数据 diary.data，编辑仅处理日记文本 diary.text
class EditDiaryParam(DesksetReqDateDay):
    text: str
@router_diary.post('/edit')
async def edit_diary(param: EditDiaryParam):
    return await noteapi.edit_diary(param.day, param.text)
class InsertDiaryParam(DesksetReqDateDay):
    line: int | None = None
    data: str
@router_diary.post('/insert')
async def insert_diary(param: InsertDiaryParam):
    return await noteapi.insert_diary(param.day, param.line, param.data)

# 列出某月中的日记属性（日期格式：YYYYMM）
@router_diary.post('/prop/list-in-month')
async def read_month(date: DesksetReqDateMonth):
    return await noteapi.list_diaryprops_in_month(date.month)

# AI 的 MCP 工具：读取、创建、写入今日日记
from datetime import datetime
from pydantic import BaseModel
class WriteTodayDiaryParam(BaseModel):
    data: str
class InsertTodayDiaryParam(BaseModel):
    line: int | None = None
    data: str
@router_diary.post('/read-today')
async def read_today_diary():
    '''读取今日日记'''
    day = datetime.now().strftime('%Y%m%d')
    return await noteapi.read_diary(day)
@router_diary.post('/create-today')
async def create_today_diary():
    '''创建今日日记'''
    day = datetime.now().strftime('%Y%m%d')
    return await noteapi.create_diary(day)
@router_diary.post('/insert-today')
async def insert_today_diary(param: InsertTodayDiaryParam):
    '''插入今日日记'''
    day = datetime.now().strftime('%Y%m%d')
    return await noteapi.insert_diary(day, param.line, param.data)
