import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL")
    KAFKA_TOPICS: str = os.getenv("KAFKA_TOPICS")
    KAFKA_CONSUMER_GROUP: str = os.getenv("KAFKA_CONSUMER_GROUP")
    REDIS_URL: str = os.getenv("REDIS_URL")

    class Config:
        env_file = ".env"


settings = Settings()
