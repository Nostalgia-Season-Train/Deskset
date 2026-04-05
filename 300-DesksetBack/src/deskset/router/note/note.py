from fastapi import APIRouter, Form, Query
from ._api import noteapi

router_note = APIRouter(prefix='/note', tags=['Note'])

@router_note.get('/list')
async def list_notepaths(directory: str = Query('')):
    return await noteapi.list_notepaths(directory)

@router_note.post('/create')
async def create_note(
    path: str = Form(),
    content: str = Form('')
):
    return await noteapi.create_note(path, content)

@router_note.post('/read')
async def read_note(path: str = Form()):
    return await noteapi.read_note(path)

@router_note.post('/insert')
async def insert_note(
    path: str = Form(),
    line: int | None = Form(None),
    data: str = Form()
):
    return await noteapi.insert_note(path, line, data)
