# ==== Router ====
from fastapi import APIRouter, Depends
from deskset.router.unify import check_token, DesksetRepJSON

router_profile = APIRouter(
    prefix='/v0/profile', tags=['个性资料'],
    dependencies=[Depends(check_token)],
    default_response_class=DesksetRepJSON
)


# ==== REST API ====
from fastapi import Form
from deskset.core.standard import DesksetError
from deskset.feature.profile import profile

@router_profile.get('')
def get():
    return profile.conf()

@router_profile.post('/name')
def post_name(name: str = Form()):
    try:
        profile.name = name
        return profile.name
    except TypeError as type_error:
        raise DesksetError(message=str(type_error), data=profile.name)
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=profile.name)

@router_profile.post('/bio')
def post_bio(bio: str = Form()):
    try:
        profile.bio = bio
        return profile.bio
    except TypeError as type_error:
        raise DesksetError(message=str(type_error), data=profile.bio)
    except ValueError as value_error:
        raise DesksetError(message=str(value_error), data=profile.bio)
