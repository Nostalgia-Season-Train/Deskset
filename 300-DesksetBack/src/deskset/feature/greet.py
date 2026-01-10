from datetime import datetime
import random

from deskset.core.locale import _t


class Greet:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self._instance, '_is_init') == False:
            self._is_init = True

    # 简单问候：根据时间段返回提前写好的问候语，问候语 = 开场白 + 内容
    def greet_simple(self):
        current_hour = datetime.now().hour
        # 数组偏移 0 是开场白，偏移 1 开始是内容
        morning   = [_t('早上好'),
                     _t('今天也是元气满满的一天！')]
        afternoon = [_t('下午好'),
                     _t('一杯绿茶如何？')]
        evening   = [_t('晚上好'),
                     _t('是时候休息了')]
        midnight  = [_t('夜深了'),
                     _t('忘记工作，睡觉去吧~')]

        # 开场白（早中晚）
        def greet_open():
            if    6 <= current_hour < 12: return   morning[0]
            elif 12 <= current_hour < 18: return afternoon[0]
            elif 18 <= current_hour < 24: return   evening[0]
            else                        : return  midnight[0]

        # 内容（随机句子）
        def greet_content():
            if    6 <= current_hour < 12: return   morning[random.randint(1, len(  morning)-1)]
            elif 12 <= current_hour < 18: return afternoon[random.randint(1, len(afternoon)-1)]
            elif 18 <= current_hour < 24: return   evening[random.randint(1, len(  evening)-1)]
            else                        : return  midnight[random.randint(1, len( midnight)-1)]

        greeting_open    = greet_open()
        greeting_content = greet_content()

        return {
            "greeting": greeting_open + "，" + greeting_content,
            "open":     greeting_open,
            "content":  greeting_content
        }

    def greet(self):
        pass

    def greet_ai(self):
        pass


greet = Greet()
