from fastapi import APIRouter
from fastapi.responses import FileResponse, Response

# from ._manager import manager

router_profile = APIRouter(prefix='/profile')

# @router_profile.get('/data')
# def get_data():
#     return {
#         'name': manager.conf_profile._confitem_name,
#         'bio': manager.conf_profile._confitem_bio
#     }

# @router_profile.get('/avatar')
# def get_avatar():
#     path_avatar = manager.conf_profile.avatar
#     if path_avatar.is_file():
#         return FileResponse(path=path_avatar, media_type='image/png')
#     else:
#         return Response(content=b'', media_type='image/png')
