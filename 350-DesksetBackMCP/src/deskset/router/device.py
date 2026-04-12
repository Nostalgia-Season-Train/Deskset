# ==== Device ====
from deskset.feature.device._abstract import AbstractDevice
from deskset.feature.device import device


# ==== 路由 ====
from fastapi import APIRouter, Depends
from deskset.router._unify import check_token, DesksetRepJSON

router_device = APIRouter(
    prefix='/device', tags=['device'],
    dependencies=[Depends(check_token)],
)

# 硬件监控
@router_device.get('/monitor', response_model=AbstractDevice.Monitor)
def monitor():
    return device.monitor()

# 硬盘存储值
@router_device.get('/disk', response_model=AbstractDevice.Disk)
def disk():
    return device.disk()

# 电池电量
@router_device.get('/battery', response_model=AbstractDevice.Battery)
def battery():
    return device.battery()

# 系统信息
@router_device.get('/system', response_model=AbstractDevice.System)
def system():
    return device.system()
