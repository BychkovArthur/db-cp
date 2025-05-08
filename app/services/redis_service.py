from typing import Optional, List, Callable, Dict
import json
from redis import Redis
from app.settings import settings
from app.schemas.user import UserOut
import asyncio
import logging

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        self.handlers: Dict[str, List[Callable]] = {}
        
    async def store_token(self, email: str, token: str) -> None:
        """Store token in Redis with TTL"""
        key = f"auth_token:{email}"
        self.redis_client.setex(
            key,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert minutes to seconds
            token
        )
    
    async def get_token(self, email: str) -> Optional[str]:
        """Get token from Redis"""
        key = f"auth_token:{email}"
        return self.redis_client.get(key)
    
    async def invalidate_token(self, email: str) -> None:
        """Remove token from Redis"""
        key = f"auth_token:{email}"
        self.redis_client.delete(key)
    
    async def is_token_valid(self, email: str, token: str) -> bool:
        """Check if token is valid and exists in Redis"""
        stored_token = await self.get_token(email)
        return stored_token == token if stored_token else False

    # Новые методы для кэширования списка пользователей
    async def store_users_list(self, current_user_id: int, users: List[UserOut]) -> None:
        """Store list of users in Redis"""
        key = f"users_list:{current_user_id}"
        # Преобразуем список пользователей в JSON
        users_json = json.dumps([user.model_dump() for user in users])
        # Устанавливаем TTL в 5 минут
        self.redis_client.setex(key, 300, users_json)

    async def get_users_list(self, current_user_id: int) -> Optional[List[UserOut]]:
        """Get list of users from Redis"""
        key = f"users_list:{current_user_id}"
        users_json = self.redis_client.get(key)
        if users_json:
            # Преобразуем JSON обратно в список объектов UserOut
            users_data = json.loads(users_json)
            return [UserOut(**user_data) for user_data in users_data]
        return None

    async def invalidate_users_list(self, current_user_id: int) -> None:
        """Remove users list from Redis"""
        key = f"users_list:{current_user_id}"
        self.redis_client.delete(key)

    async def invalidate_all_users_lists(self) -> None:
        """Remove all users lists from Redis"""
        keys = self.redis_client.keys("users_list:*")
        if keys:
            self.redis_client.delete(*keys)

    async def publish_event(self, channel: str, data: dict) -> None:
        """Publish event to Redis channel"""
        self.redis_client.publish(channel, json.dumps(data))

    async def subscribe(self, channel: str, handler: Callable) -> None:
        """Subscribe to Redis channel with handler"""
        if channel not in self.handlers:
            self.handlers[channel] = []
            self.pubsub.subscribe(channel)
        self.handlers[channel].append(handler)

    async def start_listening(self) -> None:
        """Start listening for messages"""
        while True:
            try:
                message = self.pubsub.get_message(ignore_subscribe_messages=True)
                if message and message['type'] == 'message':
                    channel = message['channel']
                    if isinstance(channel, bytes):
                        channel = channel.decode('utf-8')
                    data = json.loads(message['data'])
                    if channel in self.handlers:
                        for handler in self.handlers[channel]:
                            try:
                                await handler(data)
                            except Exception as e:
                                logger.error(f"Error in handler for channel {channel}: {e}")
                await asyncio.sleep(0.1)  # Add small delay to prevent CPU overuse
            except Exception as e:
                logger.error(f"Error in Redis listener: {e}")
                await asyncio.sleep(1)  # Wait before retrying

redis_service = RedisService() 