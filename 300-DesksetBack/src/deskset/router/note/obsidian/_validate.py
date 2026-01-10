from __future__ import annotations
from typing import ClassVar

from pydantic import BaseModel, field_validator
from asyncer import asyncify

from deskset.core.standard import DesksetError


# ==== NoteAPI data.json 设置 ====
class Setting(BaseModel):
    host: str
    port: int
    username: str
    password: str

    profile: Profile
    greets: list[Greet]  # 允许空数组

    @field_validator('greets')
    @classmethod
    def check_greets(cls, greets: list[Greet]) -> list[Greet]:
        greets_filter: list[Greet] = []

        for greet in greets:
            if len(greet.id) != 20:
                continue  # id 长度错误
            try:
                arrow.get(greet.start, Greet.format)
                arrow.get(greet.end, Greet.format)
            except arrow.ParserError:
                continue  # 时间格式错误
            except ValueError:
                continue  # 时间错误（比如 2500、1265 这种不可能的时间）

            greets_filter.append(greet)

        return greets_filter

# ID 标识符
  # 与其他模型组合以附加 id 属性
class ID(BaseModel):
    id: str  # 标识符 = YYYYMMDDHHmmss(创建日期时间) + 000000(同一时刻生成顺序)

# 个性资料
class Profile(BaseModel):
    avatar: str
    name: str
    bio: str

# 问候语
import arrow

class GreetRaw(BaseModel):
    start: str  # 开始时间 HHmm
    end: str    # 结束时间 HHmm
    open: str     # 开场白（例：早上好）
    content: str  # 问候内容（例：今天也是元气满满的一天！）

    format: ClassVar[str] = 'HHmm'  # 时间格式 HHmm。ClassVar 让 Pydantic 正确识别类变量

    # 当前时间 HHmm
    @classmethod
    async def current(cls) -> str:
        now = await asyncify(arrow.now)()
        current = await asyncify(now.format)(cls.format)
        return current

class Greet(GreetRaw, ID):
    pass
