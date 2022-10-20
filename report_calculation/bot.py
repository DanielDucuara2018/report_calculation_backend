from config import logger, telegram_app
from calculate import total_crypto_usd, total_crypto_euros, total_usd, total_euros, profit_usd, profit_euros, invested_usd, invested_euros, update, read, create, delete
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)

# telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

async def hello(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Testing hello message")
    await update_handler.message.reply_text(f'Hello {update.effective_user.first_name}')

# Total money on cryptos

async def get_total_crypto_usd(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total crypto money in usd")
    await update_handler.message.reply_text(f"Total crypto money: {total_crypto_usd()} usd")


async def get_total_crypto_euros(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total crypto money in euros")
    await update_handler.message.reply_text(f"Total crypto money: {total_crypto_euros()} euros")

# Total money (total money on cryptos + bank savings)

async def get_total_usd(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total money in usd (total crypto money + bank savings)")
    await update_handler.message.reply_text(f"Total money: {total_usd()} usd")


async def get_total_euros(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total money in euros (total crypto money + bank savings)")
    await update_handler.message.reply_text(f"Total money: {total_euros()} euros")

# Total profit (total money on cryptos - investment)

async def get_profit_usd(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total profit in usd (total crypto money - investment)")
    await update_handler.message.reply_text(f"Total profit: {profit_usd()} usd")


async def get_profit_euros(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Calculating total profit in euros (total crypto money - investment)")
    await update_handler.message.reply_text(f"Total profit: {profit_euros()} euros")

# Total invested money

async def get_investment_usd(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Total invested money in usd")
    await update_handler.message.reply_text(f"Total money: {invested_usd()} usd")

async def get_investment_euros(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_handler.message.reply_text("Total invested money in euros")
    await update_handler.message.reply_text(f"Total money: {invested_euros()} euros")

# update crypto data

async def update_crypto(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        await update_handler.message.reply_text(f"Updating {context.args[0]} with value {context.args[1]}")
        await update_handler.message.reply_text(f"Updated {update(context.args[0], context.args[1])}")
    else:
        await update_handler.message.reply_text(f"Please introduce symbol and quantity as arguments")

# get crypto data

async def read_crypto(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        await update_handler.message.reply_text(f"Reading {context.args[0]} data")
        await update_handler.message.reply_text(f"Result {read(context.args[0])}")
    else:
        await update_handler.message.reply_text(f"Please introduce symbol as arguments")

# add new crypto in database

async def create_crypto(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        await update_handler.message.reply_text(f"Adding {context.args[0]} with value {context.args[1]}")
        await update_handler.message.reply_text(f"Added {create(context.args[0], context.args[1])}")
    else:
        await update_handler.message.reply_text(f"Please introduce symbol and quantity as arguments")

# delete existing from db

async def delete_crypto(update_handler: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        await update_handler.message.reply_text(f"Deleting {context.args[0]} data")
        await update_handler.message.reply_text(f"Deleted {delete(context.args[0])}")
    else:
        await update_handler.message.reply_text(f"Please introduce symbol as arguments")

telegram_app.add_handler(CommandHandler("total_crypto_usd", get_total_crypto_usd))
telegram_app.add_handler(CommandHandler("total_crypto_euros", get_total_crypto_euros))
telegram_app.add_handler(CommandHandler("total_usd", get_total_usd))
telegram_app.add_handler(CommandHandler("total_euros", get_total_euros))
telegram_app.add_handler(CommandHandler("profit_usd", get_profit_usd))
telegram_app.add_handler(CommandHandler("profit_euros", get_profit_euros))
telegram_app.add_handler(CommandHandler("investment_usd", get_investment_usd))
telegram_app.add_handler(CommandHandler("investment_euros", get_investment_euros))
telegram_app.add_handler(CommandHandler("update", update_crypto))
telegram_app.add_handler(CommandHandler("get", read_crypto))
telegram_app.add_handler(CommandHandler("add", create_crypto))
telegram_app.add_handler(CommandHandler("delete", delete_crypto))
