from enum import Enum, unique

@unique  # 保证没有重复值
class Phase(Enum):  # 枚举时间段
    outrange = 0
    start    = 1
    inrange  = 2
    end      = 3

async def which_phase(start: int, end: int, current: int) -> Phase:
    if start == end:
        return Phase.inrange

    if start == current:
        return Phase.start
    if end == current:
        return Phase.end

    if start < end and start < current < end:
        return Phase.inrange
    if start > end and (start < current or current < end):  # current 范围隐含对 00:00 和 24:00 的判断
        return Phase.inrange

    return Phase.outrange


# ==== 路由 Router ====
from fastapi import APIRouter

from ._noteapi import noteapi
from ._validate import Greet

router_greet = APIRouter(prefix='/greet')

@router_greet.get('')
async def greet():
    greets = await noteapi.get_greets()
    current = int(await Greet.current())  # 现在时间
    start_inrange_greets: list[Greet] = []
    end_greets: list[Greet] = []

    for greet in greets:
        phase = await which_phase(int(greet.start), int(greet.end), current)
        if phase in [Phase.start, Phase.inrange]:
            start_inrange_greets.append(greet)
        if phase is Phase.end:
            end_greets.append(greet)

    # 优先返回处于开始 start 和在时间段中 inrange 阶段的问候语
    from random import choice
    if start_inrange_greets:
        greet = choice(start_inrange_greets)
        return {
            'open': greet.open,
            'content': greet.content
        }
    if end_greets:
        greet = choice(end_greets)
        return {
            'open': greet.open,
            'content': greet.content
        }

    # - [ ] 改进思考：如果没有配置，是否返回默认问候语
    from deskset.core.standard import DesksetError
    raise DesksetError(message='没有配置问候语')
