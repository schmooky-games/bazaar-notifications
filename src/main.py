from fastapi import FastAPI

from src.api.core.logs.logger import get_logger, setup_logging

from .api.routes.websocket import router
from .lifespan import lifespan

setup_logging()
logger = get_logger(__name__)

app = FastAPI(lifespan=lifespan)
app.include_router(router)
