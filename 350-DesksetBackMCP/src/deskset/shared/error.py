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


# ==== 自定义错误 ====
class UnknownSystemError(DesksetErrorNew):
    http_status: int = HTTPStatus.NOT_IMPLEMENTED
    message: str = 'Unknown System'

class ObsidianNotConnectedError(DesksetErrorNew):
    http_status: int = HTTPStatus.SERVICE_UNAVAILABLE
    message: str = 'Obsidian Not Connected'
