# ==== 依赖 ====
import psutil
from deskset.shared.lib import WIN32_ERROR_SUCCESS, dll_win32_performance_counter
from deskset.shared.log import logging
from ._abstract import AbstractDevice


# ==== Win32 设备系统 ====
from threading import Lock, Thread
from time import time, sleep
from dataclasses import dataclass

class Win32Device(AbstractDevice):
    @dataclass
    class Hardware:
        def __init__(self) -> None:
            self.cpu: dict[str, int | float] = {
                'percent': 0.0,  # CPU 利用率：类型 float，单位 %
                'freq': 0.0,     # CPU 频率：类型 float，单位 GHz
                'count': 0,      # CPU（物理）核心数：类型 int，单位 个
            }
            self.ram: dict[str, float] = {
                'percent': 0.0,  # 内存 占用率：类型 float，单位 %
                'used': 0.0,     # 内存 已用空间：类型 float，单位 GB
                'total': 0.0,    # 内存 总共空间：类型 float，单位 GB
            }
            self.disk: dict[str, float] = {
                'percent': 0.0,  # 硬盘 使用率：类型 float，单位 %
            }
            self.network: dict[str, int] = {
                'sent': 0,       # 网络 发送速率：类型 int，单位 Byte/s
                'recv': 0,       # 网络 接收速率：类型 int，单位 Byte/s
            }

            # 获取 CPU 核心数
            cpu_count = psutil.cpu_count(logical=False)
            if cpu_count is not None:
                self.cpu['count'] = cpu_count

    def __init__(self, interval: float = 1.0) -> None:
        self._hardware = Win32Device.Hardware()

        self._interval = interval  # 轮询间隔。每隔 self._interval 执行 self.__loop_refresh 刷新 self._hardware 一次
        self._lock = Lock()
        self._loop = Thread(target=self.__loop_refresh)
        self._loop.daemon = True  # 守护线程，主进程结束时自动退出
        self._loop.start()

    def __loop_refresh(self) -> None:
        # 初始化硬盘统计
        disk_active_time_start_result = dll_win32_performance_counter.start()

        if disk_active_time_start_result != WIN32_ERROR_SUCCESS:
            logging.error(f'DiskActiveTime.dll start fail, error code: 0x{disk_active_time_start_result:04X}')
        else:
            dll_win32_performance_counter.get()  # 刷掉第一次调用的错误

        # 初始化网络统计
        self.__last_net = psutil.net_io_counters()
        self.__last_nettime = time()

        # 轮询
        while True:
            sleep(self._interval)

            # *** 性能计数器 ***
            disk_active_time = dll_win32_performance_counter.get()

            # *** 芯片 ***
            self._hardware.cpu['percent'] = psutil.cpu_percent(interval=0)
            if disk_active_time.errorCpuFreq != WIN32_ERROR_SUCCESS:
                logging.error(f'CpuFreq get fail, error code: 0x{disk_active_time.errorCpuFreq:04X}')
            else:
                self._hardware.cpu['freq'] = round(disk_active_time.resultCpuFreq * psutil.cpu_freq().max, 2)

            # *** 内存 ***
            virtual_memory = psutil.virtual_memory()
            self._hardware.ram['percent'] = virtual_memory.percent
            self._hardware.ram['used'] = round((virtual_memory.used >> 28) / 4 * 10) / 10  # 保留一位小数
            self._hardware.ram['total'] = float(round((virtual_memory.total >> 28) / 4))   # 计算取整，消去保留内存影响，得到实际物理内存

            # *** 硬盘 ***
              # 使用率 percent: float %
                # 注 1：使用率 = 活动时间：单位时间内硬盘使用率，也就是 1s 内读写所用时间 / 1s
                # 注 2：round(, 1) 与 psutil 百分比位数保持一致
            if disk_active_time.errorDiskTime != WIN32_ERROR_SUCCESS:
                logging.error(f'DiskTime get fail, error code: 0x{disk_active_time.errorDiskTime:04X}')
            else:
                self._hardware.disk['percent'] = round(disk_active_time.resultDiskTime, 1)

            # *** 网络 ***
              # 发送 sent: int Byte/s、接收 recv: int Byte/s
                # 注 1：Kbps 中 Kb(1000 bit) != KB(1024 Byte)
                # 注 2：Byte / 125 = Kbp
            net = psutil.net_io_counters()
            netnow = time()
            netlong = round(netnow - self.__last_nettime, 1)
            self._hardware.network['sent'] = int((net.bytes_sent - self.__last_net.bytes_sent) / netlong)
            self._hardware.network['recv'] = int((net.bytes_recv - self.__last_net.bytes_recv) / netlong)
            self.__last_net = net
            self.__last_nettime = netnow

        dll_win32_performance_counter.end()  # - [ ] 暂时无法清理，预期应在 fastAPI 应用结束时执行

    # --- 硬件监控 ---
    def monitor(self) -> dict:
        return {
            'cpu': self._hardware.cpu,
            'ram': self._hardware.ram,
            'disk': self._hardware.disk,
            'network': self._hardware.network
        }

    # --- 硬盘存储值 ---
    def disk(self, is_gb: bool = True) -> list[dict]:
        partitions = []

        for partition in psutil.disk_partitions():
            partition_usage = psutil.disk_usage(partition.device)
            partitions.append({
                'root': partition.device,
                'total': partition_usage.total,
                'free': partition_usage.free,
                'percent': partition_usage.percent
            })

        # 硬盘可用/已用大小单位从 byte 转换为 gb
          # js 不适合对这种大数字进行科学运算...
        def byte_to_gb(num):
            num = (num >> 20) / 1024

            if  100 <= num:
                num = int(num)
            elif 10 <= num < 100:
                num = int(num * 10) / 10
            else:
                num = int(num * 100) / 100

            return num

        if is_gb:
            for partition in partitions:
                partition['total'] = byte_to_gb(partition['total'])
                partition['free'] = byte_to_gb(partition['free'])

        return partitions

    # --- 电池电量 ---
    def battery(self) -> dict:
        battery = psutil.sensors_battery()

        # 设备可能没有电池：台式机、HTPC
          # 直接返回 正在充电 + 电量 100%，省去错误处理
        if battery is None:
            return { 'isplug': True, 'percent': 100 }

        return {
            'isplug': battery.power_plugged,
            'percent': battery.percent
        }

    # --- 系统信息 ---
    def system(self) -> dict:
        import platform  # 只有这个函数要用 platform，单独导入

        return {
            'name': platform.node(),
            'system': platform.system(),
            'version': platform.version(),
            'machine': platform.machine()
        }
