from fastapi import APIRouter, Query
from ._manager import API, api as noteapi

router_search = APIRouter(prefix='/search')

cache_notes: list[API.SuggestFile] = []
@router_search.get('/note')
async def find_note(query: str = Query(None)):
    global cache_notes
    # /note 传入 None，/note?query= 传入 ''。两者均代表结束查询
    if query == None or query == '':
        cache_notes = []
    else:
        if cache_notes == []:
            cache_notes = await noteapi.suggest_by_switcher(query)
        return [note for note in cache_notes if query.lower() in note['name'].lower()]
