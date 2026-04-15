from fastapi import Response
import orjson

from deskset.shared.standard import DesksetError

# 临时：Deskset 响应模型
from typing import Any
from pydantic import BaseModel

class DesksetRepModel(BaseModel):
    success: bool
    code: int
    message: str
    result: Any


# ==== 返回 JSON ====
class DesksetRepJSON(Response):
    media_type = 'application/json'
    schema: dict = { 'schema': DesksetRepModel.model_json_schema() }

    def render(self, content: object) -> bytes:
        response = {
            'success': True,
            'code': 0,
            'message': 'Success',
            'result': content
        }
        return orjson.dumps(response)


# ==== 返回 DesksetError 错误 ====
class DesksetErrorRep(Response):
    media_type = 'application/json'

    def render(self, error: DesksetError) -> bytes:  # type: ignore
        response = {
            'success': False,
            'code': error.code,
            'message': error.message,
            'result': error.data  # 给用户展示的错误信息
        }
        return orjson.dumps(response)
