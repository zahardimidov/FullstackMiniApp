from fastapi import APIRouter
from database.requests import get_all_users
from src.ext.dependencies import WebAppUser
from src.users.schemas import *
from bot import create_ref_link

router = APIRouter(prefix="/users")


@router.get('/all', response_model=AllUsersResponse)
async def get_all_users_handler():
    users = await get_all_users()

    return AllUsersResponse(
        users=[user.to_dict() for user in users]
    )

@router.get('/ref/link', response_model=RefLinkResponse)
async def get_my_referalls(user: WebAppUser):
    print(user)

    link = await create_ref_link(user_id=user.id)

    return RefLinkResponse(link=link)

