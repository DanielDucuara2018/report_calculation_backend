import logging
from dataclasses import dataclass
from typing import Optional

import click
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)

from report_calculation.actions.calculate import (
    invested_euros,
    invested_usd,
    profit_euros,
    profit_usd,
    total_crypto_euros,
    total_crypto_usd,
    total_euros,
    total_usd,
)
from report_calculation.actions.currency import create, delete, read, update
from report_calculation.db import initialize
from report_calculation.errors import NoUserFound
from report_calculation.model import User as ModelUser

logger = logging.getLogger(__name__)


def _get_user(
    bot_info: User,
) -> Optional[ModelUser]:  # TODO add <class 'telegram._user.User'> typing
    users = ModelUser.find(telegram_id=str(bot_info.id))
    if users:
        return users[-1]
    return None


@dataclass
class TelegramBot:

    telegram_id: str
    telegram_bot_token: str
    telegram_app: Optional[Application] = None

    def __post_init__(self):
        self.telegram_app = self.init_telegram_bot_application(self.telegram_bot_token)

    def run(self):
        logger.info("Running app handlers")
        self.telegram_app.add_handler(CommandHandler("start", self.start))
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_total_crypto_usd, pattern="total_crypto_usd")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(
                self.get_total_crypto_euros, pattern="total_crypto_euros"
            )
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_total_usd, pattern="total_usd")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_total_euros, pattern="total_euros")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_profit_usd, pattern="profit_usd")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_profit_euros, pattern="profit_euros")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_investment_usd, pattern="investment_usd")
        )
        self.telegram_app.add_handler(
            CallbackQueryHandler(self.get_investment_euros, pattern="investment_euros")
        )
        self.telegram_app.add_handler(CommandHandler("help", self.help_command))
        self.telegram_app.add_handler(CommandHandler("update", self.update_currency))
        self.telegram_app.add_handler(CommandHandler("get", self.read_currency))
        self.telegram_app.add_handler(CommandHandler("add", self.create_currency))
        self.telegram_app.add_handler(CommandHandler("delete", self.delete_currency))
        self.telegram_app.add_handler(CommandHandler("bot", self.bot_info))
        self.telegram_app.add_error_handler(self.error_handler)
        self.telegram_app.run_polling()

    def init_telegram_bot_application(self, telegram_bot_token: str) -> Application:
        logger.info("Initialising Telegram bot connection")
        # We use persistence to demonstrate how buttons can still work after the bot was restarted
        # Create the Application and pass it your bot's token.
        return (
            Application.builder()
            .token(telegram_bot_token)
            .persistence(
                PicklePersistence(
                    filepath=f"arbitrarycallbackdatabot_{self.telegram_id}"
                )
            )
            .arbitrary_callback_data(True)
            .build()
        )

    async def start(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Sends a message with three inline buttons attached."""
        logger.info(f"Launching keyboard buttons")
        keyboard = [
            [
                InlineKeyboardButton("total usd", callback_data="total_usd"),
                InlineKeyboardButton("total euros", callback_data="total_euros"),
            ],
            [
                InlineKeyboardButton(
                    "total crypto usd", callback_data="total_crypto_usd"
                ),
                InlineKeyboardButton(
                    "total crypto euros", callback_data="total_crypto_euros"
                ),
            ],
            [
                InlineKeyboardButton("profit usd", callback_data="profit_usd"),
                InlineKeyboardButton("profit euros", callback_data="profit_euros"),
            ],
            [
                InlineKeyboardButton("investment usd", callback_data="investment_usd"),
                InlineKeyboardButton(
                    "investment euros", callback_data="investment_euros"
                ),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update_handler.message.reply_text(
            "Please choose:", reply_markup=reply_markup
        )

    async def help_command(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Displays info on how to use the bot."""
        logger.info(f"Launching help command")
        await update_handler.message.reply_text("Use /start to test this bot.")

    # Total money on cryptos

    async def get_total_crypto_usd(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_total_crypto_usd")
        await update_handler.callback_query.edit_message_text(
            "Calculating total crypto money in usd"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total crypto money: {await total_crypto_usd(_get_user(await context.bot.get_me()))} usd"
        )

    async def get_total_crypto_euros(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_total_crypto_euros")
        await update_handler.callback_query.edit_message_text(
            "Calculating total crypto money in euros"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total crypto money: {await total_crypto_euros(_get_user(await context.bot.get_me()))} euros"
        )

    # Total money (total money on cryptos + bank savings)

    async def get_total_usd(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_total_usd")
        await update_handler.callback_query.edit_message_text(
            "Calculating total money in usd (total crypto money + bank savings)"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total money: {await total_usd(_get_user(await context.bot.get_me()))} usd"
        )

    async def get_total_euros(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_total_euros")
        await update_handler.callback_query.edit_message_text(
            "Calculating total money in euros (total crypto money + bank savings)"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total money: {await total_euros(_get_user(await context.bot.get_me()))} euros"
        )

    # Total profit (total money on cryptos - investment)

    async def get_profit_usd(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_profit_usd")
        await update_handler.callback_query.edit_message_text(
            "Calculating total profit in usd (total crypto money - investment)"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total profit: {await profit_usd(_get_user(await context.bot.get_me()))} usd"
        )

    async def get_profit_euros(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_profit_euros")
        await update_handler.callback_query.edit_message_text(
            "Calculating total profit in euros (total crypto money - investment)"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total profit: {await profit_euros(_get_user(await context.bot.get_me()))} euros"
        )

    # Total invested money

    async def get_investment_usd(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_investment_usd")
        await update_handler.callback_query.edit_message_text(
            "Total invested money in usd"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total money: {await invested_usd(_get_user(await context.bot.get_me()))} usd"
        )

    async def get_investment_euros(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running get_investment_euros")
        await update_handler.callback_query.edit_message_text(
            "Total invested money in euros"
        )
        await update_handler.callback_query.message.reply_text(
            f"Total money: {await invested_euros(_get_user(await context.bot.get_me()))} euros"
        )

    ## CRUD handlers
    # add new crypto in database

    async def create_currency(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running create_currency")

        user: ModelUser = _get_user(await context.bot.get_me())
        if not user:
            raise NoUserFound(message="Not user found")

        if context.args:
            await update_handler.message.reply_text(
                f"Adding {context.args[0]} with value {context.args[1]}"
            )
            await update_handler.message.reply_text(
                f"Added {create(user.user_id, context.args[0], context.args[1])}"
            )
        else:
            await update_handler.message.reply_text(
                f"Please introduce symbol and quantity as arguments"
            )

    # get crypto data

    async def read_currency(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running read_currency")

        user: ModelUser = _get_user(await context.bot.get_me())
        if not user:
            raise NoUserFound(message="Not user found")

        if context.args:
            symbol = context.args[0]
            await update_handler.message.reply_text(f"Reading {symbol} data")
            await update_handler.message.reply_text(
                f"Result {read(user.user_id, symbol)}"
            )
        else:
            await update_handler.message.reply_text(f"Reading all data")
            currencies = read(user.user_id)
            message = "Result: \n"
            for currency in currencies:  # type: ignore
                message += f"* <b>{currency.symbol} :</b> {currency.quantity} \n"
            await update_handler.message.reply_text(message, parse_mode=ParseMode.HTML)

    # update crypto data

    async def update_currency(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running update_currency")

        user: ModelUser = _get_user(await context.bot.get_me())
        if not user:
            raise NoUserFound(message="Not user found")

        if context.args:
            await update_handler.message.reply_text(
                f"Updating {context.args[0]} with value {context.args[1]}"
            )
            await update_handler.message.reply_text(
                f"Updated {update(user.user_id, context.args[0], context.args[1])}"
            )
        else:
            await update_handler.message.reply_text(
                f"Please introduce symbol and quantity as arguments"
            )

    # delete existing from db

    async def delete_currency(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Running delete_currency")

        user: ModelUser = _get_user(await context.bot.get_me())
        if not user:
            raise NoUserFound(message="Not user found")

        if context.args:
            await update_handler.message.reply_text(f"Deleting {context.args[0]} data")
            await update_handler.message.reply_text(
                f"Deleted {delete(user.user_id, context.args[0])}"
            )
        else:
            await update_handler.message.reply_text(
                f"Please introduce symbol as arguments"
            )

    # Error handlers

    async def error_handler(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Log the error and send a telegram message to notify the client."""
        logger.error("Error %s", context.error)
        message = (
            f"An exception was raised while handling a command\n"
            f"<pre>{context.error}</pre>"
        )
        await update_handler.message.reply_text(
            message, parse_mode=ParseMode.HTML
        )  # TODO To fix, it is not working

    # get bot_info

    async def bot_info(
        self, update_handler: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        logger.info(f"Geting bot information")
        await update_handler.message.reply_text(
            f"bot information {await context.bot.get_me()}"
        )


@click.command()
@click.option("--telegram-id", required=True, type=str)
@click.option("--telegram-token", required=True, type=str)
def telegram_bot(telegram_id: str, telegram_token: str):
    logger.info("Initialising App")
    initialize(True)
    bot = TelegramBot(telegram_id, telegram_token)
    bot.run()
