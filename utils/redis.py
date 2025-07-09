from redis.asyncio import Redis

from ..utils.settings import getSettings

settings = getSettings()

redis: Redis = Redis.from_url(settings.REDIS_URL)
