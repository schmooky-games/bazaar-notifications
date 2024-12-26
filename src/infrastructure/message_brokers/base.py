from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseConsumer(ABC):
    @abstractmethod
    async def subscribe(self, **kwargs) -> Any:
        pass


@dataclass
class BaseMessageBroker(ABC):
    consumer: BaseConsumer

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def start_consuming(self, topic: str) -> Any:
        pass

    @abstractmethod
    async def stop_consuming(self, topic: str) -> None:
        pass
