from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    # ======== 设备监控 ========
    """
    函数注释代表功能需求

    数据类型：
    - int：Byte
    - float：%
    - str：默认
    - list：[]{}

    附：vsc 采用 md 格式渲染注释，加 \</br\> 换行；加 \&nbsp\; 空格
    """
    @abstractmethod
    def cpu(self):
        """
        CPU：占用率 %
        """
        pass

    @abstractmethod
    def memory(self):
        """
        内存：容量 Byte、已用 Byte、占用率 %
        """
        pass

    @abstractmethod
    def disk_partitions(self):
        """
        硬盘分区：[分区]{根路径 Byte、容量 Byte、已用 Byte、占用率 %}
        """
        pass

    @abstractmethod
    def _refresh_network(self) -> None:
        pass

    @abstractmethod
    def battery(self):
        """
        电池：是否充电 bool、剩余电量 %
        """
        pass

    @abstractmethod
    def system(self):
        """
        系统：系统类型、系统版本、设备名称、芯片架构
        """
        pass

    # ======== 设备控制 ========
    # @abstractmethod
    # def volume(self):
    #     """
    #     音量
    #     """
    #     pass
