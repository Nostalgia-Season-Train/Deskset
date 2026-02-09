# ==== Device ====
from deskset.core.standard import DesksetError
from deskset.feature.device import device

def check_init() -> None:
    if device is None:
        raise DesksetError(code=2000, message='未知系统，无法读取设备信息')


# ==== 路由 ====
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

router_device = APIRouter(
    prefix='/v0/device', tags=['设备信息'],
    dependencies=[Depends(check_token), Depends(check_init)],
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
