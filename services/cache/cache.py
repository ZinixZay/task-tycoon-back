from redis import client


class Cache:
    @staticmethod
    async def get_or_add(key: str, value: str) -> str:
        current_value: str = await client.get(key)
        if current_value:
            return current_value
        await client.set(key, value)
        return value
    
    @staticmethod
    async def get_or_update(key: str, value: str) -> str:
        current_value: str = await client.get(key)
        if current_value != value:
            await client.set(key, value)
        return value

    @staticmethod
    async def set(key: str, value: str, expires_in: int = 3600) -> str:
        await client.set(key, value, ex=expires_in)
        return value
    
    @staticmethod
    async def get(key: str) -> str | None:
        current_value = await client.get(key)
        return current_value 
    
    @staticmethod
    async def delete(key: str) -> str:
        await client.delete(key)
        return key
    