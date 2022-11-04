from bot import telegram_app
from config import logger


def main():
    logger.info("Initialising App")
    telegram_app.run_polling()


if __name__ == "__main__":
    main()
