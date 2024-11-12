from src.redis import client


class CacheService:
    @classmethod
    async def get_or_add(cls, key: str, value: str) -> str:
        current_value: str = await client.get(key)
        if current_value:
            return current_value
        await client.set(key, value)
        return value

    @classmethod
    async def get_or_update(cls, key: str, value: str) -> str:
        current_value: str = await client.get(key)
        if current_value != value:
            await client.set(key, value)
        return value

    @classmethod
    async def set(cls, key: str, value: str, expires_in: int = 3600) -> str:
        print(client)
        await client.set(key, value, ex=expires_in)
        print(value)
        return value

    @classmethod
    async def get(cls, key: str) -> str | None:
        current_value = await client.get(key)
        return current_value

    @classmethod
    async def delete(cls, key: str) -> str:
        await client.delete(key)
        return key
