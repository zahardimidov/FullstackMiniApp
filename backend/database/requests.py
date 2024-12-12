from typing import List
from database.session import async_session
from sqlalchemy import select
from src.users.models import User, UserRef


async def get_user(user_id) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        return user
    
async def get_all_users() -> List[User]:
    async with async_session() as session:
        user = await session.scalars(select(User))

        return user.all()


async def set_user(user_id, **kwargs) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            user = User(id=user_id, **kwargs)
            session.add(user)
        else:
            for k, v in kwargs.items():
                setattr(user, k, v)

        await session.commit()
        await session.refresh(user)

        return user


async def set_referral(referrer_id, referral_id):
    async with async_session() as session:
        ref = UserRef(referral_id=referral_id, referrer_id=referrer_id)
        session.add(ref)
        await session.commit()
        await session.refresh(ref)

        return ref
