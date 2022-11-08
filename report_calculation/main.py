from report_calculation.bot import telegram_app
from report_calculation.config import logger


def main():
    logger.info("Initialising App")
    telegram_app.run_polling()


if __name__ == "__main__":
    main()
