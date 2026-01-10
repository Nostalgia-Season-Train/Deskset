# 基础天气：晴天 雨天 多云
WEATHER = ['sunny', 'rainy', 'cloudy']


# === 路由 ===
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

router_weather = APIRouter(
    prefix='/v0/weather', tags=['天气'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)

@router_weather.get('/random')
def random_weather():  # 随机生成并返回天气信息
    import random
    return WEATHER[random.randint(0, len(WEATHER)-1)]
