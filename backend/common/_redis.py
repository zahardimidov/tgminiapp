from config import REDIS_HOST, REDIS_PORT
from redis.asyncio import from_url


class redis:
    url = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

    @staticmethod
    async def set(key, value, ex = None):
        async with from_url(redis.url) as async_redis:
            return await async_redis.set(key, value, ex=ex)

    @staticmethod
    async def get(key) -> bytes:
        async with from_url(redis.url) as async_redis:
            return await async_redis.get(key)

    @staticmethod
    async def delete(key):
        async with from_url(redis.url) as async_redis:
            return await async_redis.delete(key)