from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    registered_at: datetime

    class Config:
        extra = 'ignore'
        json_encoders = {
            datetime: lambda v: v.strftime('%d/%m/%Y %H:%M:%S')
        }


class CreateUser(UserBase):
    ...


class AllUsersResponse(BaseModel):
    users: List[UserBase]


class RefLinkResponse(BaseModel):
    link: str