import redis.asyncio as redis
from src.config import config

redis_client = redis.Redis(
    host=config.env_data.REDIS_HOST,
    port=config.env_data.REDIS_PORT,
    db=0,
    decode_responses=True
)