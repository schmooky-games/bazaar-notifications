import asyncio
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI

from src.domain.services import WebSocketNotificationService

from .api.routes.websocket import ws_manager
from .config.settings import settings
from .infrastructure.message_brokers.kafka.kafka import (KafkaConsumer,
                                                         KafkaMessageBroker)
from .infrastructure.redis.base import RedisAuctionSubscriptionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await redis.from_url(settings.REDIS_URL)

    app.state.subscription_service = RedisAuctionSubscriptionService(app.state.redis)
    app.state.notification_service = WebSocketNotificationService(ws_manager)

    consumer = KafkaConsumer(
        settings.KAFKA_BROKER_URL,
        app.state.subscription_service,
        app.state.notification_service,
    )
    app.state.message_broker = KafkaMessageBroker(consumer)
    await app.state.message_broker.start()

    asyncio.create_task(app.state.message_broker.start_consuming(settings.KAFKA_TOPICS))

    yield

    await app.state.redis.close()
    await app.state.message_broker.stop()
