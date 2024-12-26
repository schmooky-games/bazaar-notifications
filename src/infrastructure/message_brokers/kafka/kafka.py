import json
from typing import Any

from aiokafka import AIOKafkaConsumer

from src.api.core.logs.logger import get_logger
from src.domain.services import AuctionSubscriptionService, NotificationService
from src.infrastructure.message_brokers.base import (BaseConsumer,
                                                     BaseMessageBroker)

logger = get_logger(__name__)


class KafkaConsumer(BaseConsumer):
    def __init__(
        self,
        bootstrap_servers: str,
        subscription_service: AuctionSubscriptionService,
        notification_service: NotificationService,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.subscription_service = subscription_service
        self.notification_service = notification_service

    async def subscribe(self, topics: list[str]) -> None:
        logger.info(f"Starting Kafka consumer for topics: {topics}")
        self.consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id="notification_service",
            auto_offset_reset="latest",
        )
        await self.consumer.start()

        try:
            async for msg in self.consumer:
                try:
                    event_data = json.loads(msg.value.decode("utf-8"))
                    auction_id = event_data.get("auctionId")

                    if not auction_id:
                        continue
                    if "bidderId" in event_data:
                        bidder_id = event_data["bidderId"]
                        await self.subscription_service.subscribe_user(
                            auction_id, bidder_id
                        )

                    subscribers = await self.subscription_service.get_subscribers(
                        auction_id
                    )
                    if not subscribers:
                        continue

                    await self.notification_service.notify_users(
                        auction_id,
                        {
                            "type": "auction_update",
                            "auctionId": auction_id,
                            "newPrice": event_data.get("newPrice"),
                            "timestamp": event_data.get("timestamp"),
                        },
                    )

                except json.JSONDecodeError as e:
                    logger.error(e)
                    continue
                except Exception as e:
                    logger.error(e)
                    continue
        finally:
            await self.consumer.stop()


class KafkaMessageBroker(BaseMessageBroker):
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer
        self._running = False

    async def start(self) -> None:
        self._running = True

    async def stop(self) -> None:
        self._running = False

    async def start_consuming(self, topics: str) -> Any:
        await self.consumer.subscribe(topics.split(","))

    async def stop_consuming(self, topic: str) -> None:
        if self.consumer.consumer:
            await self.consumer.consumer.stop()
