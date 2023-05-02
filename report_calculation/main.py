from report_calculation.bot import telegram_app
from report_calculation.config import logger
from report_calculation.db import initialize


def main():
    logger.info("Initialising App")
    initialize(True)
    telegram_app.run_polling()


if __name__ == "__main__":
    main()
