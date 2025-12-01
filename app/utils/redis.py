# redis.py
import redis.asyncio as redis
from app.config import config

_redis_client = None

async def get_redis_client():
    """返回全局 Redis 客户端"""
    if _redis_client is None:
        raise RuntimeError("Redis client not initialized. Did you forget to start the app?")
    return _redis_client

async def create_redis_pool():
    global _redis_client
    _redis_client = redis.Redis(
        host=config.get("redis.host"),
        port=config.get("redis.port"),
        db=config.get("redis.db"),
        password=config.get("redis.password"),
        decode_responses=True
    )
    return _redis_client

async def close_redis_pool():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None