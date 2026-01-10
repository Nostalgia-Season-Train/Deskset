from fastapi import APIRouter

router_debug = APIRouter(prefix='/v0/debug', tags=['调试'])


@router_debug.get('/exception:no-define')
def trigger_exception_nodefine():
    # print(no_define)
    pass
