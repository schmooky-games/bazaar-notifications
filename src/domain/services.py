from typing import List, Protocol

from src.infrastructure.websocket.connection import WebSocketManager


class NotificationService(Protocol):
    async def notify_users(self, auction_id: str, message: dict) -> None:
        pass


class AuctionSubscriptionService(Protocol):
    async def subscribe_user(self, auction_id: str, user_id: str) -> None:
        pass

    async def unsubscribe_user(self, auction_id: str, user_id: str) -> None:
        pass

    async def get_subscribers(self, auction_id: str) -> List[str]:
        pass


class WebSocketNotificationService(NotificationService):
    def __init__(self, manager: WebSocketManager):
        self.manager = manager

    async def notify_users(self, auction_id: str, message: dict) -> None:
        subscribers = self.manager.active_connections.keys()

        for user_id in subscribers:
            try:
                await self.manager.send_message(
                    user_id, {"type": "auction_update", **message}
                )
            except Exception as e:
                continue
