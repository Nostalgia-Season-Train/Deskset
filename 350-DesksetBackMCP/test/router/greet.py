from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

from deskset.feature.greet import greet

router_greet = APIRouter(
    prefix='/v0/greet', tags=['问候'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


# 简单问候
@router_greet.get('/simple')
async def get_simple_greet():
    return greet.greet_simple()
