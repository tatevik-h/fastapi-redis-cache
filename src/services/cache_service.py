import aioredis
import json
from config.core import settings

redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_cache(key: str):
    val = await redis.get(key)
    return json.loads(val) if val else None


async def set_cache(key: str, value: dict, expire: int = 300):
    await redis.set(key, json.dumps(value), ex=expire)
