from http import HTTPStatus
from pydantic import BaseModel

class DesksetErrorNew(Exception):
    http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR
    code: int = 1
    message: str = 'Deskset Error'

class DesksetErrorNewResponseModel(BaseModel):
    code: int
    message: str

deskset_error_new_response_schema = DesksetErrorNewResponseModel.model_json_schema()


# ==== 其他错误 ====
class UnknownSystemError(DesksetErrorNew):
    http_status: int = HTTPStatus.NOT_IMPLEMENTED
    message: str = 'Unknown System'

class ObsidianNotConnectedError(DesksetErrorNew):
    http_status: int = HTTPStatus.SERVICE_UNAVAILABLE
    message: str = 'Obsidian Not Connected'


# ==== 验证错误 ====
class InvalidDayFormatError(DesksetErrorNew):
    http_status: int = HTTPStatus.BAD_REQUEST
    def __init__(self, day: str):
        # 格式错了，比如 2026-04-12 不是 YYYYMMDD 格式
        self.message = f'Error! Day {day} date format is incorrect! Should be YYYYMMDD'

class InvalidDayError(DesksetErrorNew):
    http_status: int = HTTPStatus.BAD_REQUEST
    def __init__(self, day: str):
        # 日期错了，比如 2026-04-31 没有 31 号
        self.message = f'Error! Day {day} date is invalid!'

class InvalidMonthFormatError(DesksetErrorNew):
    http_status: int = HTTPStatus.BAD_REQUEST
    def __init__(self, month: str):
        # 格式错了，比如 2026-04 不是 YYYYMM 格式
        self.message = f'Error! Month {month} date format is incorrect! Should be YYYYMM'

class InvalidMonthError(DesksetErrorNew):
    http_status: int = HTTPStatus.BAD_REQUEST
    def __init__(self, month: str):
        # 月份错了，比如 2026-13 没有 13 月
        self.message = f'Error! Month {month} date is invalid!'

class InvalidDateRangeError(DesksetErrorNew):
    http_status: int = HTTPStatus.BAD_REQUEST
    def __init__(self, start_day: str, end_day: str):
        # 起始日晚于结束日，比如 2026-04-30 到 2026-04-01
        self.message = f'Error! Start day {start_day} cannot be earlier than end day {end_day}'
