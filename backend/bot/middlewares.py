from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.requests import get_user_by_id, create_user


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str: Any],
    ) -> Any:

        if not event.chat.type == 'private':
            return

        user = await get_user_by_id(user_id=event.from_user.id)

        if not user:
            user = await create_user(id=event.from_user.id, username=event.from_user.username)

        data['user'] = user

        return await handler(event, data)