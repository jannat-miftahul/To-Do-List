from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get('/auth')
def authentication():
    return {'user' : 'authenticated'}
