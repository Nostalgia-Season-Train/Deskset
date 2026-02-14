from fastapi import Response
import orjson

from deskset.core.standard import DesksetError


# ==== 返回 JSON ====
class DesksetRepJSON(Response):
    media_type = 'application/json'

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

    def render(self, error: DesksetError) -> bytes:
        response = {
            'success': False,
            'code': error.code,
            'message': error.message,
            'result': error.data  # 给用户展示的错误信息
        }
        return orjson.dumps(response)
