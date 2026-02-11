import platform
from ._abstract import AbstractDevice
from ._unknown import UnknownDevice
from .win32 import Win32Device

device: AbstractDevice = UnknownDevice()

if platform.system() == 'Windows':
    device = Win32Device()
