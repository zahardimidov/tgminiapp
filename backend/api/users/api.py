from api.dependencies import WebAppUser
from api.users.schemas import *
from database.requests import *
from fastapi import APIRouter

router = APIRouter(prefix="/user")


@router.get('/me', response_model=UserResponse, status_code=200)
async def me(user: WebAppUser):
    return dict(
        user_id = user.id,
        username = user.username
    )
