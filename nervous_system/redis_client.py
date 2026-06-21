import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._client = None

    async def get_client(self):
        if self._client is None:
            self._client = await redis.from_url(self.redis_url)
        return self._client

    async def publish(self, channel: str, message: str):
        client = await self.get_client()
        await client.publish(channel, message)

    async def subscribe(self, channel: str):
        client = await self.get_client()
        pubsub = client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

    async def set_cache(self, key: str, value: str, ttl: int = 86400): # 24 hours TTL
        client = await self.get_client()
        await client.setex(key, ttl, value)

    async def get_cache(self, key: str):
        client = await self.get_client()
        return await client.get(key)

    async def set_session_state(self, key: str, value: str):
        client = await self.get_client()
        await client.set(key, value)

    async def get_session_state(self, key: str):
        client = await self.get_client()
        return await client.get(key)

    async def acquire_lock(self, lock_name: str, timeout: int = 10) -> bool:
        client = await self.get_client()
        return await client.set(f"lock:{lock_name}", "locked", nx=True, ex=timeout)

    async def release_lock(self, lock_name: str):
        client = await self.get_client()
        await client.delete(f"lock:{lock_name}")

