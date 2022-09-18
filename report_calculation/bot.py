from config import logger, telegram_app
from calculate import total_crypto_usd, total_crypto_euros, total_usd, total_euros, profit_usd, profit_euros, invested_usd, invested_euros
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)

# telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Testing hello message")
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# Total money on cryptos

async def get_total_crypto_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total crypto money in usd")
    await update.message.reply_text(f"Total crypto money: {total_crypto_usd()} usd")


async def get_total_crypto_euros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total crypto money in euros")
    await update.message.reply_text(f"Total crypto money: {total_crypto_euros()} euros")

# Total money (total money on cryptos + bank savings)

async def get_total_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total money in usd (total crypto money + bank savings)")
    await update.message.reply_text(f"Total money: {total_usd()} usd")


async def get_total_euros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total money in euros (total crypto money + bank savings)")
    await update.message.reply_text(f"Total money: {total_euros()} euros")

# Total profit (total money on cryptos - investment)

async def get_profit_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total profit in usd (total crypto money - investment)")
    await update.message.reply_text(f"Total profit: {profit_usd()} usd")


async def get_profit_euros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Calculating total profit in euros (total crypto money - investment)")
    await update.message.reply_text(f"Total profit: {profit_euros()} euros")

# Total invested money

async def get_investment_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Total invested money in usd")
    await update.message.reply_text(f"Total money: {invested_usd()} usd")

async def get_investment_euros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Total invested money in euros")
    await update.message.reply_text(f"Total money: {invested_euros()} euros")


telegram_app.add_handler(CommandHandler("total_crypto_usd", get_total_crypto_usd))
telegram_app.add_handler(CommandHandler("total_crypto_euros", get_total_crypto_euros))
telegram_app.add_handler(CommandHandler("total_usd", get_total_usd))
telegram_app.add_handler(CommandHandler("total_euros", get_total_euros))
telegram_app.add_handler(CommandHandler("profit_usd", get_profit_usd))
telegram_app.add_handler(CommandHandler("profit_euros", get_profit_euros))
telegram_app.add_handler(CommandHandler("investment_usd", get_investment_usd))
telegram_app.add_handler(CommandHandler("investment_euros", get_investment_euros))

