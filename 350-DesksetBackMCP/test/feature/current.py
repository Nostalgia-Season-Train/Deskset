from datetime import datetime
import arrow

from deskset.core.config import config


# 日期时间
class Current:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init') == False:
            self._is_init = True

            self._language = config.language

    # ======== 日期（格式化：数字转字符并补零） ========
    def date_format(self):
        return {
            "year":  str(datetime.now().year ).zfill(4),
            "month": str(datetime.now().month).zfill(2),
            "day":   str(datetime.now().day  ).zfill(2),
            "week":  arrow.now().format('dddd', locale=self._language)
        }

    # ======== 日期（数字） ========
    def date_year(self):
        return datetime.now().year

    def date_month(self):
        return datetime.now().month

    def date_day(self):
        return datetime.now().day

    def date_week(self):
        return datetime.now().weekday()

    # ======== 时间（格式化：数字转字符并补零） ========
    # 时间
    def time_format(self):
        return {
            "hour":   str(datetime.now().hour  ).zfill(2),
            "minute": str(datetime.now().minute).zfill(2),
            "second": str(datetime.now().second).zfill(2)
        }

    # 12 时时间
    def time_hour12_format(self):
        if datetime.now().hour < 12:
            hour = datetime.now().hour
            ampm = "am"
        else:
            hour = datetime.now().hour - 12
            ampm = "pm"

        hour   = str(               hour  ).zfill(2)
        minute = str(datetime.now().minute).zfill(2)
        second = str(datetime.now().second).zfill(2)

        return {
            "hour":     hour,
            "minute": minute,
            "second": second,
            "ampm":     ampm
        }

    # ======== 时间（数字） ========
    def time_hour(self):
        return datetime.now().hour

    def time_minute(self):
        return datetime.now().minute

    def time_second(self):
        return datetime.now().second


current = Current()
