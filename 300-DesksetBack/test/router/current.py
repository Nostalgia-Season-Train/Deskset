from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

from deskset.feature.current import current

router_datetime = APIRouter(
    prefix='/v0/datetime', tags=['日期时间'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


@router_datetime.get('/date')
async def get_date():
    return current.date_format()

@router_datetime.get('/week')
async def get_week():
    return current.date_format()

@router_datetime.get('/time')
async def get_time():
    return current.time_format()

@router_datetime.get('/time12')
async def get_time12():
    return current.time_hour12_format()
