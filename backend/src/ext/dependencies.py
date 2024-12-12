import base64
from typing import Annotated

from database.requests import get_user
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.ext.validation import validate_qsl_init_data
from src.users.models import User

auth_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    decoded_bytes = base64.b64decode(token.credentials)
    decoded_string = decoded_bytes.decode('utf-8')

    user_data = validate_qsl_init_data(decoded_string)
    if not user_data:
        raise HTTPException(
            status_code=400, detail='Invalid auth data provided')

    user = await get_user(user_data.get('id'))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user

WebAppUser = Annotated[User, Depends(get_current_user)]
