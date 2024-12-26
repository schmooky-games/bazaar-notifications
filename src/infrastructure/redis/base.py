from typing import List

from src.domain.services import AuctionSubscriptionService


class RedisAuctionSubscriptionService(AuctionSubscriptionService):
    def __init__(self, redis_client):
        self.redis = redis_client

    async def subscribe_user(self, auction_id: str, user_id: str) -> None:
        key = f"{auction_id}"
        try:
            await self.redis.sadd(key, user_id)
            subscribers = await self.redis.smembers(key)
        except Exception as e:
            raise

    async def get_subscribers(self, auction_id: str) -> List[str]:
        key = f"{auction_id}"
        try:
            subscribers = await self.redis.smembers(key)
            subscriber_list = [s.decode("utf-8") for s in subscribers]
            return subscriber_list
        except Exception as e:
            return []
