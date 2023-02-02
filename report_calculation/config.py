import logging
import os
from typing import Optional

from binance import AsyncClient
from binance.client import Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram.ext import Application, PicklePersistence

binance_api_key: Optional[str] = os.environ.get("binance_api_key")
binance_secret_key: Optional[str] = os.environ.get("binance_secret_key")
telegram_bot_token: Optional[str] = os.environ.get("telegram_bot_token")

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


def init_telegram_bot_application() -> Application:
    logger.info("Initialising Telegram bot connection ")
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    # Create the Application and pass it your bot's token.
    return (
        Application.builder()
        .token(telegram_bot_token)
        .persistence(PicklePersistence(filepath="arbitrarycallbackdatabot"))
        .arbitrary_callback_data(True)
        .build()
    )


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

binance_client: Client = init_binance_connection()
telegram_app: Application = init_telegram_bot_application()
