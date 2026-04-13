# ==== Router ====
from fastapi import APIRouter, Depends
from deskset.router._unify import check_token, DesksetRepJSON

router_config = APIRouter(
    prefix='/v0/config', tags=['config'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


# ==== URL ====
from fastapi import Form
from deskset.shared.config import config
from deskset.shared.standard import DesksetError

@router_config.get('/language')
def get_language():
    return config.language_storage

@router_config.post('/language')
def post_language(language: str = Form()):
    try:
        config.language = language
        return config.language_storage
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.language_storage)

@router_config.get('/server_port')
def get_server_port():
    return config.server_port_storage

@router_config.post('/server_port')
def post_server_port(server_port: int = Form()):
    try:
        config.server_port = server_port
        return config.server_port_storage
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.server_port_storage)

@router_config.get('/username')
def get_username():
    return config.username

@router_config.post('/username')
def post_username(username: str = Form()):
    try:
        config.username = username
        return config.username
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.username)

@router_config.get('/password')
def get_password():
    return config.password

@router_config.post('/password')
def post_password(password: str = Form()):
    try:
        config.password = password
        return config.password
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.password)

@router_config.get('/ai_base_url')
def get_ai_base_url():
    return config.ai_base_url
@router_config.post('/ai_base_url')
def post_ai_base_url(ai_base_url: str = Form()):
    try:
        config.ai_base_url = ai_base_url
        return config.ai_base_url
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.ai_base_url)

@router_config.get('/ai_api_key')
def get_ai_api_key():
    return config.ai_api_key
@router_config.post('/ai_api_key')
def post_ai_api_key(ai_api_key: str = Form()):
    try:
        config.ai_api_key = ai_api_key
        return config.ai_api_key
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.ai_api_key)

@router_config.get('/ai_model')
def get_ai_model():
    return config.ai_model
@router_config.post('/ai_model')
def post_ai_model(ai_model: str = Form()):
    try:
        config.ai_model = ai_model
        return config.ai_model
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.ai_model)
