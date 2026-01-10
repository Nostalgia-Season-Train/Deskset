# ==== Router ====
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

router_config = APIRouter(
    prefix='/v0/config', tags=['配置'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


# ==== URL ====
from fastapi import Form
from deskset.core.config import config
from deskset.core.standard import DesksetError

@router_config.get('/language')
def get_language():
    return config.language_in_yaml

@router_config.post('/language')
def post_language(language: str = Form()):
    try:
        config.language = language
        return config.language_in_yaml
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.language_in_yaml)

@router_config.get('/server-port')
def get_server_port():
    return config.server_port_in_yaml

@router_config.post('/server-port')
def post_server_port(server_port: int = Form()):
    try:
        config.server_port = server_port
        return config.server_port_in_yaml
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=config.server_port_in_yaml)

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
