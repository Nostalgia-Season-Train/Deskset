import platform

from deskset.feature.device.win32 import Win32Device


class DeviceFactory:
    _device = None

    @staticmethod
    def create_device():
        if DeviceFactory._device is None:
            if platform.system() == 'Windows':
                DeviceFactory._device = Win32Device()
            else:
                DeviceFactory._device = None

        return DeviceFactory._device
