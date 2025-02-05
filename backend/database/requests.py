from .models import *
from .session import async_session
from sqlalchemy import delete, select


async def get_one_by_id(id, model):
    async with async_session() as session:
        item = await session.scalar(select(model).where(model.id == id))
        return item


async def get_one_by_jwt_id(jwt_id, model):
    async with async_session() as session:
        item = await session.scalar(select(model).where(model.jwt_id == jwt_id))
        return item


async def get_all(model, limit=None, offset=None):
    async with async_session() as session:
        items = await session.scalars(select(model).limit(limit).offset(offset))
        return items.all()


async def create_one(model, **kwargs):
    async with async_session() as session:
        item = model(**kwargs)
        session.add(item)

        await session.commit()
        await session.refresh(item)

        return item


async def update_one(id, model, **kwargs):
    async with async_session() as session:
        item = await session.scalar(select(model).where(model.id == id))

        if not item:
            raise Exception('Item not found')

        for k, v in kwargs.items():
            setattr(item, k, v)

        await session.commit()
        await session.refresh(item)

        return item


async def delete_one_by_id(id, model):
    async with async_session() as session:
        await session.execute(delete(model).where(model.id == id))
        await session.commit()


async def get_user_by_email(email) -> User:
    async with async_session() as session:
        item = await session.scalar(select(User).where(User.email == email))
        return item


async def create_user(**kwargs) -> User:
    return await create_one(User, **kwargs)

async def get_user_by_id(user_id) -> User:
    return await get_one_by_id(user_id, User)
