# ==== 当前模块绝对路径 ====
import os
module_path = os.path.dirname(__file__)


# ==== Win32 常量 ====
WIN32_ERROR_SUCCESS = 0


# ==== Win32 性能计数器 ====
import ctypes

class Win32PerformanceCounterReturnData(ctypes.Structure):
    _fields_ = [
        ('errorDiskTime', ctypes.c_ulong),
        ('resultDiskTime', ctypes.c_double),
        ('errorCpuFreq', ctypes.c_ulong),
        ('resultCpuFreq', ctypes.c_double),  # CpuFreq * CPU-最大频率 = CPU-当前频率
    ]

dll_win32_performance_counter = ctypes.windll.LoadLibrary(f'{module_path}/Win32PerformanceCounter.dll')
dll_win32_performance_counter.get.restype = Win32PerformanceCounterReturnData
dll_win32_performance_counter.start.restype = ctypes.c_ulong
dll_win32_performance_counter.end.restype = ctypes.c_ulong
