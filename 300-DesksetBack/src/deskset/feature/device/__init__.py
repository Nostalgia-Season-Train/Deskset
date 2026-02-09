import platform
from deskset.feature.device.win32 import Win32Device

device = None

if platform.system() == 'Windows':
    device = Win32Device()
