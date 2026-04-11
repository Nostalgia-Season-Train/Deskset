from fastapi import APIRouter

router = APIRouter()

@router.get('/hello')
def hello():
    return 'Hello from sample'
