# ==== Device ====
from deskset.feature.device import device


# ==== 路由 ====
from fastapi import APIRouter, Depends
from deskset.router._unify import check_token, DesksetRepJSON

router_device = APIRouter(
    prefix='/v0/device', tags=['device'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)

# 硬件监控
@router_device.get('/monitor')
def monitor():
    return device.monitor()

# 硬盘存储值
@router_device.get('/disk')
def disk():
    return device.disk()

# 电池电量
@router_device.get('/battery')
def battery():
    return device.battery()

# 系统信息
@router_device.get('/system')
def system():
    return device.system()
