from __future__ import annotations

from pydantic import BaseModel, field_validator, model_validator
from deskset.shared.standard import DesksetError


# ==== 验证日期 ====
import arrow

class DesksetReqDateDay(BaseModel):
    day: str  # 某天，日期格式：YYYYMMDD，比如 20250324

    @field_validator('day')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMMDD')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！某天 {v} 日期格式有误！应为 YYYYMMDD')
        except ValueError:
            raise DesksetError(message=f'错误！某天 {v} 日期无效！')

class DesksetReqDateMonth(BaseModel):
    month: str  # 某月，日期格式：YYYYMM，比如 202503

    @field_validator('month')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMM')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！某月 {v} 日期格式有误！应为 YYYYMM')
        except ValueError:
            raise DesksetError(message=f'错误！某月 {v} 日期无效！')

class DesksetReqDateDayRange(BaseModel):
    start_day: str
    end_day: str

    @field_validator('start_day', 'end_day')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMMDD')
            return v
        except arrow.parser.ParserError:
            raise DesksetError(message=f'错误！某天 {v} 日期格式有误！应为 YYYYMMDD')
        except ValueError:
            raise DesksetError(message=f'错误！某天 {v} 日期无效！')

    @model_validator(mode='after')
    # @classmethod   mode='after' 定义为实例方法
    def check_day_order(self) -> DesksetReqDateDayRange:
        if not int(self.start_day) <= int(self.end_day):
            raise DesksetError(f'错误！起始天 {self.start_day} 不得早于结束天 {self.end_day}')
        return self
