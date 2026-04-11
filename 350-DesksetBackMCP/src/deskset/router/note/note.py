from fastapi import APIRouter, Form, Query
from pydantic import BaseModel
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

class ReadNoteRequest(BaseModel):
    path: str
@router_note.post('/read')
async def read_note(request: ReadNoteRequest):
    return await noteapi.read_note(request.path)
@router_note.post('/readprop')
async def read_noteprop(request: ReadNoteRequest):
    return await noteapi.read_noteprop(request.path)

class InsertNoteRequest(BaseModel):
    path: str
    line: int | None = None
    data: str
@router_note.post('/insert')
async def insert_note(request: InsertNoteRequest):
    return await noteapi.insert_note(request.path, request.line, request.data)
