from fastapi import APIRouter, Depends

from deskset.feature.note import apscheduler
from deskset.router.unify import DesksetRepJSON

from .obsidian._noteapi import noteapi

router_apscheduler = APIRouter(
    prefix='/apscheduler', tags=['Apscheduler'],
    default_response_class=DesksetRepJSON
)

@router_apscheduler.get('/add-hello-task')
async def hello_task():
    async def hello():
        import asyncio
        asyncio.create_task(noteapi.get('/obsidian/hello'))
    apscheduler.add_job(hello, 'interval', seconds=5)
    return '添加 hello task 成功'
