import logging
import os
from typing import Optional

from binance import AsyncClient
from binance.client import Client

binance_api_key: Optional[str] = os.environ.get("binance_api_key")
binance_secret_key: Optional[str] = os.environ.get("binance_secret_key")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def init_binance_connection() -> Client:
    logger.info("Initialising Binance connection")
    return Client(binance_api_key, binance_secret_key)


async def init_binance_connection_async() -> AsyncClient:
    logger.info("Initialising Binance async connection")
    return await AsyncClient.create(binance_api_key, binance_secret_key)


binance_client: Client = init_binance_connection()
