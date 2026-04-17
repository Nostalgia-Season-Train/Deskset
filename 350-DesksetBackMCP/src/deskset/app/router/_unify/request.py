from __future__ import annotations

from pydantic import BaseModel, field_validator, model_validator
from deskset.shared.error import (
    InvalidDayFormatError,
    InvalidDayError,
    InvalidMonthFormatError,
    InvalidMonthError,
    InvalidDateRangeError
)


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
            raise InvalidDayFormatError(v)
        except ValueError:
            raise InvalidDayError(v)

class DesksetReqDateMonth(BaseModel):
    month: str  # 某月，日期格式：YYYYMM，比如 202503

    @field_validator('month')
    @classmethod
    def check(cls, v: str) -> str:
        try:
            arrow.get(v, 'YYYYMM')
            return v
        except arrow.parser.ParserError:
            raise InvalidMonthFormatError(v)
        except ValueError:
            raise InvalidMonthError(v)

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
            raise InvalidDayFormatError(v)
        except ValueError:
            raise InvalidDayError(v)

    @model_validator(mode='after')
    # @classmethod   mode='after' 定义为实例方法
    def check_day_order(self) -> DesksetReqDateDayRange:
        if not int(self.start_day) <= int(self.end_day):
            raise InvalidDateRangeError(self.start_day, self.end_day)
        return self
