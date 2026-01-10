# ==== Device ====
from deskset.core.standard import DesksetError

from deskset.feature.device import DeviceFactory

device = DeviceFactory.create_device()

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

# 实时监控
@router_device.get('/realtime')
def get_realtime():
    return device.realtime

# （硬盘）分区信息
@router_device.get('/partitions')
def get_partitions():
    return device.partitions()

# 电池信息
@router_device.get('/battery')
def get_battery():
    return device.battery()

# 系统信息
@router_device.get('/system')
def get_system():
    return device.system()
